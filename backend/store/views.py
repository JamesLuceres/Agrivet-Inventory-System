from decimal import Decimal
from datetime import datetime, time, timedelta
import zoneinfo
from django.shortcuts import render
from django.utils import timezone
from django.db.models import F, Q, Sum
from django.db import transaction as db_transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product, Customer, Transaction, TransactionItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CustomerSerializer,
    TransactionSerializer,
    TransactionItemSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(products__is_active=True).distinct().order_by('name')


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('name')

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        """
        Returns products where total stock falls below the low_stock_threshold.
        Takes unified bulk-to-retail conversion into account.
        """
        active_products = Product.objects.filter(is_active=True).order_by('name')
        low_stock_ids = []
        for p in active_products:
            threshold = Decimal(str(p.low_stock_threshold or 5))
            ratio = Decimal(str(p.units_per_bulk or 1))
            if p.unit_bulk_name and ratio > 1:
                total_bulk = p.stock_sacks + (p.stock_kilos / ratio)
                if total_bulk < threshold:
                    low_stock_ids.append(p.id)
            else:
                if p.stock_kilos < threshold:
                    low_stock_ids.append(p.id)

        low_stock_products = Product.objects.filter(id__in=low_stock_ids).order_by('name')
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='unpack-sack')
    def unpack_sack(self, request, pk=None):
        """
        Breaks down bulk sacks into retail units (kilos/pieces).
        Payload: { sacks: 1, kilos_per_sack: 50 }
        """
        product = self.get_object()
        try:
            sacks_count = float(request.data.get('sacks', 1))
            kilos_per_sack = float(request.data.get('kilos_per_sack', 50))
        except (ValueError, TypeError):
            return Response({'error': 'Invalid number of sacks or conversion factor.'}, status=status.HTTP_400_BAD_REQUEST)

        if sacks_count <= 0 or kilos_per_sack <= 0:
            return Response({'error': 'Values must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)

        if float(product.stock_sacks) < sacks_count:
            return Response({
                'error': f'Insufficient {product.unit_bulk_name or "sack"} stock. Available: {product.stock_sacks}, requested: {sacks_count}'
            }, status=status.HTTP_400_BAD_REQUEST)

        kilos_to_add = sacks_count * kilos_per_sack
        product.stock_sacks = float(product.stock_sacks) - sacks_count
        product.stock_kilos = float(product.stock_kilos) + kilos_to_add
        product.save()

        return Response({
            'message': f'Successfully converted {sacks_count} {product.unit_bulk_name or "sack"}(s) into {kilos_to_add} {product.unit_retail_name or "kilo"}(s).',
            'stock_sacks': float(product.stock_sacks),
            'stock_kilos': float(product.stock_kilos)
        })


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('name')
    serializer_class = CustomerSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Voids / deletes a sale transaction.
        - Restores physical product inventory (sacks and loose kilos).
        - Reverses customer debt (total_utang) if it was on Credit.
        - Restores customer debt if it was a Debt Payment.
        """
        transaction = self.get_object()

        # 1. Reverse customer debt impact if applicable
        if transaction.customer:
            customer = transaction.customer
            if transaction.transaction_type == 'CREDIT':
                unpaid = transaction.total_amount - transaction.amount_paid
                if unpaid > 0:
                    customer.total_utang = max(Decimal('0.00'), customer.total_utang - unpaid)
                    customer.save()
            elif transaction.transaction_type == 'DEBT_PAYMENT':
                customer.total_utang += transaction.total_amount
                customer.save()

        # 2. Restore inventory stock for physical items
        for item in transaction.items.all():
            product = item.product
            if not product:
                continue

            is_service = (
                getattr(product, 'is_service', False) or
                (product.category and product.category.name in ['Services', 'Services & Others', 'GCash']) or
                'gcash' in (product.name or '').lower() or
                'other item' in (product.name or '').lower()
            )
            if is_service:
                continue

            unit_type_upper = (item.unit_type or '').upper()
            bulk_name_upper = (product.unit_bulk_name or 'SACK').upper()
            ratio = product.units_per_bulk or Decimal('1.00')
            has_bulk = bool(product.unit_bulk_name and ratio > 1)

            if has_bulk:
                total_base_qty = (product.stock_sacks * ratio) + product.stock_kilos
                if unit_type_upper == bulk_name_upper or unit_type_upper in ['SACK', 'CASE', 'BOX', 'PACK', 'BULK']:
                    restored_base_qty = Decimal(str(item.quantity)) * ratio
                else:
                    restored_base_qty = Decimal(str(item.quantity))

                new_total_base = total_base_qty + restored_base_qty
                product.stock_sacks = new_total_base // ratio
                product.stock_kilos = new_total_base % ratio
            else:
                product.stock_kilos += Decimal(str(item.quantity))

            product.save()

        # 3. Delete the transaction record
        transaction.delete()
        return Response({'message': 'Transaction deleted and inventory restored.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='daily-summary')
    def daily_summary(self, request):
        """
        Calculates total cash revenue, gcash, debt payments, physical cash drawer, and top-selling products.
        Filters by the Philippine timezone (Asia/Manila) local day boundary.
        """
        tz = zoneinfo.ZoneInfo('Asia/Manila')
        date_param = request.query_params.get('date')
        if date_param:
            try:
                target_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                target_date = timezone.now().astimezone(tz).date()
        else:
            target_date = timezone.now().astimezone(tz).date()

        start_of_day = datetime.combine(target_date, time.min, tzinfo=tz)
        end_of_day = datetime.combine(target_date, time.max, tzinfo=tz)

        today_transactions = Transaction.objects.filter(created_at__range=(start_of_day, end_of_day))

        # 1. Physical Cash Sales from merchandise
        cash_sales = today_transactions.filter(transaction_type='CASH').aggregate(
            total=Sum('total_amount')
        )['total'] or 0.00

        # 2. Digital / GCash Sales
        gcash_sales = today_transactions.filter(transaction_type='GCASH').aggregate(
            total=Sum('total_amount')
        )['total'] or 0.00

        # 3. Debt payments collected today in cash
        debt_payments_collected = today_transactions.filter(transaction_type='DEBT_PAYMENT').aggregate(
            total=Sum('total_amount')
        )['total'] or 0.00

        # 4. Total Physical Cash In Drawer = Cash Sales + Cash Debt Repayments
        total_physical_cash = float(cash_sales) + float(debt_payments_collected)

        # 5. Total Credit Given (unpaid portion of today's credit transactions)
        credit_transactions = today_transactions.filter(transaction_type='CREDIT')
        credit_sales_total = credit_transactions.aggregate(total=Sum('total_amount'))['total'] or 0.00
        credit_paid_down = credit_transactions.aggregate(total=Sum('amount_paid'))['total'] or 0.00
        credit_given = float(credit_sales_total) - float(credit_paid_down)

        # Total Merchandise Revenue (CASH + GCASH + CREDIT Total Sales)
        total_merchandise_revenue = float(cash_sales) + float(gcash_sales) + float(credit_sales_total)

        # Total Cash & Digital Shift Total (CASH + GCASH + DEBT_PAYMENT)
        total_shift_sales = float(cash_sales) + float(gcash_sales) + float(debt_payments_collected)

        # Count merchandise sales transactions
        total_sales_count = today_transactions.exclude(transaction_type='DEBT_PAYMENT').count()

        # Top-selling products today
        top_products = TransactionItem.objects.filter(
            transaction__created_at__range=(start_of_day, end_of_day)
        ).values(
            'product__id', 'product__name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_sales=Sum('subtotal')
        ).order_by('-total_sales')[:5]

        top_products_list = [
            {
                'product_id': item['product__id'],
                'product_name': item['product__name'],
                'total_quantity': float(item['total_quantity']),
                'total_sales': float(item['total_sales'])
            }
            for item in top_products
        ]

        return Response({
            'date': target_date.isoformat(),
            'total_cash_revenue': float(cash_sales),
            'total_gcash_revenue': float(gcash_sales),
            'debt_payments_collected': float(debt_payments_collected),
            'total_physical_cash': float(total_physical_cash),
            'total_merchandise_revenue': float(total_merchandise_revenue),
            'total_shift_sales': float(total_shift_sales),
            'total_credit_given': float(credit_given),
            'total_sales_count': total_sales_count,
            'top_products': top_products_list
        })

    @action(detail=False, methods=['get'], url_path='monthly-summary')
    def monthly_summary(self, request):
        """
        Accepts optional query params ?year=2026&month=7 (defaulting to the current month/year in Asia/Manila).
        Returns total revenue, credit issued, transaction count, and daily breakdown list for that entire month.
        """
        tz = zoneinfo.ZoneInfo('Asia/Manila')
        year_param = request.query_params.get('year')
        month_param = request.query_params.get('month')

        now = timezone.now().astimezone(tz)
        year = int(year_param) if year_param else now.year
        month = int(month_param) if month_param else now.month

        start_of_month = datetime(year, month, 1, 0, 0, 0, tzinfo=tz)
        if month == 12:
            end_of_month = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=tz) - timedelta(microseconds=1)
        else:
            end_of_month = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=tz) - timedelta(microseconds=1)

        month_transactions = Transaction.objects.filter(
            created_at__range=(start_of_month, end_of_month)
        )

        merch_transactions = month_transactions.exclude(transaction_type='DEBT_PAYMENT')
        debt_transactions = month_transactions.filter(transaction_type='DEBT_PAYMENT')

        cash_sales = merch_transactions.filter(transaction_type='CASH').aggregate(total=Sum('total_amount'))['total'] or 0.00
        gcash_sales = merch_transactions.filter(transaction_type='GCASH').aggregate(total=Sum('total_amount'))['total'] or 0.00
        credit_transactions = merch_transactions.filter(transaction_type='CREDIT')
        credit_total = credit_transactions.aggregate(total=Sum('total_amount'))['total'] or 0.00
        credit_paid_down = credit_transactions.aggregate(total=Sum('amount_paid'))['total'] or 0.00
        total_credit_issued = float(credit_total) - float(credit_paid_down)

        total_debt_collected = debt_transactions.aggregate(total=Sum('total_amount'))['total'] or 0.00

        # Total revenue from merchandise
        total_revenue = float(cash_sales) + float(gcash_sales) + float(credit_total)
        transaction_count = merch_transactions.count()

        # Build daily breakdown list
        breakdown_dict = {}
        for tx in month_transactions:
            day_str = tx.created_at.astimezone(tz).date().isoformat()
            if day_str not in breakdown_dict:
                breakdown_dict[day_str] = {
                    'date': day_str,
                    'cash_revenue': 0.00,
                    'gcash_revenue': 0.00,
                    'debt_collected': 0.00,
                    'credit_given': 0.00,
                    'daily_total': 0.00,
                    'sales_count': 0
                }
            
            if tx.transaction_type == 'CASH':
                breakdown_dict[day_str]['cash_revenue'] += float(tx.total_amount)
                breakdown_dict[day_str]['daily_total'] += float(tx.total_amount)
                breakdown_dict[day_str]['sales_count'] += 1
            elif tx.transaction_type == 'GCASH':
                breakdown_dict[day_str]['gcash_revenue'] += float(tx.total_amount)
                breakdown_dict[day_str]['daily_total'] += float(tx.total_amount)
                breakdown_dict[day_str]['sales_count'] += 1
            elif tx.transaction_type == 'CREDIT':
                unpaid = float(tx.total_amount - tx.amount_paid)
                breakdown_dict[day_str]['credit_given'] += unpaid
                breakdown_dict[day_str]['daily_total'] += float(tx.total_amount)
                breakdown_dict[day_str]['sales_count'] += 1
            elif tx.transaction_type == 'DEBT_PAYMENT':
                breakdown_dict[day_str]['debt_collected'] += float(tx.total_amount)

        daily_breakdown = sorted(breakdown_dict.values(), key=lambda x: x['date'])

        return Response({
            'year': year,
            'month': month,
            'total_revenue': float(total_revenue),
            'total_cash_sales': float(cash_sales),
            'total_gcash_sales': float(gcash_sales),
            'total_credit_issued': float(total_credit_issued),
            'total_debt_collected': float(total_debt_collected),
            'transaction_count': transaction_count,
            'daily_breakdown': daily_breakdown
        })


class BackupViewSet(viewsets.ViewSet):
    """
    Handles 1-Click Backup Export and Disaster Recovery Restore for Nichole Agrivet.
    """
    @action(detail=False, methods=['get'], url_path='export')
    def export_backup(self, request):
        categories_data = CategorySerializer(Category.objects.all(), many=True).data
        products_data = ProductSerializer(Product.objects.all(), many=True).data
        customers_data = CustomerSerializer(Customer.objects.all(), many=True).data
        transactions_data = TransactionSerializer(Transaction.objects.all().order_by('id'), many=True).data

        backup_payload = {
            'app': 'Nichole Agrivet POS & Inventory',
            'version': '1.0',
            'exported_at': timezone.now().isoformat(),
            'categories': categories_data,
            'products': products_data,
            'customers': customers_data,
            'transactions': transactions_data
        }
        return Response(backup_payload)

    @action(detail=False, methods=['post'], url_path='restore')
    def restore_backup(self, request):
        data = request.data
        if not isinstance(data, dict):
            return Response({'error': 'Invalid backup format. Expected a JSON object.'}, status=status.HTTP_400_BAD_REQUEST)

        categories = data.get('categories', [])
        products = data.get('products', [])
        customers = data.get('customers', [])
        transactions = data.get('transactions', [])

        try:
            with db_transaction.atomic():
                # 1. Restore/Update Categories
                category_map = {}
                for c in categories:
                    cat, _ = Category.objects.update_or_create(
                        name=c['name'],
                        defaults={'description': c.get('description', '')}
                    )
                    category_map[c.get('id')] = cat

                # 2. Restore/Update Products
                product_map = {}
                for p in products:
                    cat_id = p.get('category')
                    cat = category_map.get(cat_id) or Category.objects.filter(id=cat_id).first()
                    if not cat:
                        cat, _ = Category.objects.get_or_create(name='General Supplies')

                    prod, _ = Product.objects.update_or_create(
                        name=p['name'],
                        defaults={
                            'category': cat,
                            'unit_bulk_name': p.get('unit_bulk_name', 'Sack'),
                            'unit_retail_name': p.get('unit_retail_name', 'Kilo'),
                            'price_per_sack': p.get('price_per_sack'),
                            'price_per_kilo': p.get('price_per_kilo'),
                            'cost_per_sack': p.get('cost_per_sack'),
                            'cost_per_kilo': p.get('cost_per_kilo'),
                            'stock_sacks': p.get('stock_sacks', 0),
                            'stock_kilos': p.get('stock_kilos', 0),
                            'units_per_bulk': p.get('units_per_bulk', 50),
                            'low_stock_threshold': p.get('low_stock_threshold', 5),
                            'is_active': p.get('is_active', True),
                            'is_service': p.get('is_service', False),
                        }
                    )
                    product_map[p.get('id')] = prod

                # 3. Restore/Update Customers
                customer_map = {}
                for cust in customers:
                    c_obj, _ = Customer.objects.update_or_create(
                        name=cust['name'],
                        defaults={
                            'contact_number': cust.get('contact_number'),
                            'total_utang': cust.get('total_utang', 0),
                            'notes': cust.get('notes')
                        }
                    )
                    customer_map[cust.get('id')] = c_obj

                # 4. Restore Transactions if provided and missing
                restored_tx_count = 0
                for tx in transactions:
                    tx_id = tx.get('id')
                    if tx_id and not Transaction.objects.filter(id=tx_id).exists():
                        cust = customer_map.get(tx.get('customer')) or (Customer.objects.filter(id=tx.get('customer')).first() if tx.get('customer') else None)
                        new_tx = Transaction.objects.create(
                            id=tx_id,
                            transaction_type=tx.get('transaction_type'),
                            reference_number=tx.get('reference_number'),
                            customer=cust,
                            total_amount=tx.get('total_amount'),
                            amount_paid=tx.get('amount_paid'),
                            change_given=tx.get('change_given', 0),
                        )
                        # Transaction Items
                        for item in tx.get('items', []):
                            prod = product_map.get(item.get('product')) or Product.objects.filter(id=item.get('product')).first()
                            if prod:
                                TransactionItem.objects.create(
                                    transaction=new_tx,
                                    product=prod,
                                    unit_type=item.get('unit_type', 'pc'),
                                    quantity=item.get('quantity', 1),
                                    unit_price=item.get('unit_price', 0),
                                    subtotal=item.get('subtotal', 0),
                                    notes=item.get('notes', '')
                                )
                        restored_tx_count += 1

                return Response({
                    'success': True,
                    'message': 'Backup successfully restored!',
                    'stats': {
                        'categories': len(categories),
                        'products': len(products),
                        'customers': len(customers),
                        'new_transactions_restored': restored_tx_count
                    }
                })
        except Exception as e:
            return Response({'error': f'Failed to restore backup: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

