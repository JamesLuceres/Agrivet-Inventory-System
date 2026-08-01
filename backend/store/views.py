from django.shortcuts import render
from django.utils import timezone
from django.db.models import F, Q, Sum
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
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        """
        Returns products where stock_sacks or stock_kilos fall below the low_stock_threshold.
        """
        low_stock_products = Product.objects.filter(
            Q(stock_sacks__lt=F('low_stock_threshold')) | 
            Q(stock_kilos__lt=F('low_stock_threshold')),
            is_active=True
        ).order_by('name')
        
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('name')
    serializer_class = CustomerSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['get'], url_path='daily-summary')
    def daily_summary(self, request):
        """
        Calculates total cash revenue, credit given, transaction count, and top-selling products for the current day.
        """
        today = timezone.localtime(timezone.now()).date()
        today_transactions = Transaction.objects.filter(created_at__date=today)

        # Cash revenue: total amount of all CASH transactions today
        cash_revenue = today_transactions.filter(transaction_type='CASH').aggregate(
            total=Sum('total_amount')
        )['total'] or 0.00

        # Credit given: total amount of all CREDIT transactions today minus what was paid today
        # i.e., the unpaid portion of today's credit transactions
        credit_transactions = today_transactions.filter(transaction_type='CREDIT')
        credit_given = sum(tx.total_amount - tx.amount_paid for tx in credit_transactions)

        total_sales_count = today_transactions.count()

        # Top-selling products today
        top_products = TransactionItem.objects.filter(
            transaction__created_at__date=today
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
            'date': today.isoformat(),
            'total_cash_revenue': float(cash_revenue),
            'total_credit_given': float(credit_given),
            'total_sales_count': total_sales_count,
            'top_products': top_products_list
        })

    @action(detail=False, methods=['get'], url_path='monthly-summary')
    def monthly_summary(self, request):
        """
        Accepts optional query params ?year=2026&month=7 (defaulting to the current month/year).
        Returns total revenue, credit issued, transaction count, and daily breakdown list for that entire month.
        """
        year_param = request.query_params.get('year')
        month_param = request.query_params.get('month')

        now = timezone.localtime(timezone.now())
        year = int(year_param) if year_param else now.year
        month = int(month_param) if month_param else now.month

        month_transactions = Transaction.objects.filter(
            created_at__year=year,
            created_at__month=month
        )

        total_revenue = month_transactions.aggregate(total=Sum('total_amount'))['total'] or 0.00
        
        # Credit issued: unpaid portion of all credit transactions in this month
        credit_transactions = month_transactions.filter(transaction_type='CREDIT')
        total_credit_issued = sum(tx.total_amount - tx.amount_paid for tx in credit_transactions)

        transaction_count = month_transactions.count()

        # Build daily breakdown list
        breakdown_dict = {}
        for tx in month_transactions:
            day_str = timezone.localtime(tx.created_at).date().isoformat()
            if day_str not in breakdown_dict:
                breakdown_dict[day_str] = {
                    'date': day_str,
                    'cash_revenue': 0.00,
                    'credit_given': 0.00,
                    'sales_count': 0
                }
            
            if tx.transaction_type == 'CASH':
                breakdown_dict[day_str]['cash_revenue'] += float(tx.total_amount)
            elif tx.transaction_type == 'CREDIT':
                breakdown_dict[day_str]['credit_given'] += float(tx.total_amount - tx.amount_paid)
            
            breakdown_dict[day_str]['sales_count'] += 1

        daily_breakdown = sorted(breakdown_dict.values(), key=lambda x: x['date'])

        return Response({
            'year': year,
            'month': month,
            'total_revenue': float(total_revenue),
            'total_credit_issued': float(total_credit_issued),
            'transaction_count': transaction_count,
            'daily_breakdown': daily_breakdown
        })
