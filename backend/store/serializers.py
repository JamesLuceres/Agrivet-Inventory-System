from decimal import Decimal
from rest_framework import serializers
from .models import Category, Product, Customer, Transaction, TransactionItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    total_base_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, attrs):
        stock_sacks = attrs.get('stock_sacks')
        if stock_sacks is None:
            stock_sacks = self.instance.stock_sacks if (self.instance and self.instance.stock_sacks is not None) else Decimal('0.00')
        stock_kilos = attrs.get('stock_kilos')
        if stock_kilos is None:
            stock_kilos = self.instance.stock_kilos if (self.instance and self.instance.stock_kilos is not None) else Decimal('0.00')
        unit_bulk_name = attrs.get('unit_bulk_name', self.instance.unit_bulk_name if self.instance else None)
        units_per_bulk = attrs.get('units_per_bulk')
        if units_per_bulk is None:
            units_per_bulk = self.instance.units_per_bulk if (self.instance and self.instance.units_per_bulk is not None) else Decimal('50.00')

        if unit_bulk_name and units_per_bulk and Decimal(str(units_per_bulk)) > 1:
            total_base = (Decimal(str(stock_sacks)) * Decimal(str(units_per_bulk))) + Decimal(str(stock_kilos))
            attrs['stock_sacks'] = total_base // Decimal(str(units_per_bulk))
            attrs['stock_kilos'] = total_base % Decimal(str(units_per_bulk))
        elif not unit_bulk_name:
            attrs['stock_sacks'] = Decimal('0.00')
        return attrs


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class TransactionItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = TransactionItem
        fields = '__all__'
        read_only_fields = ('transaction',)  # Make transaction read-only as we set it in create()


class TransactionSerializer(serializers.ModelSerializer):
    items = TransactionItemSerializer(many=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        transaction = Transaction.objects.create(**validated_data)
        
        # 1. Update customer total credit balance (total_utang) if type is CREDIT
        if transaction.transaction_type == 'CREDIT' and transaction.customer:
            unpaid_balance = transaction.total_amount - transaction.amount_paid
            if unpaid_balance > 0:
                customer = transaction.customer
                customer.total_utang += unpaid_balance
                customer.save()

        # 2. Unified Auto-Conversion Pool Stock Deduction
        for item_data in items_data:
            item = TransactionItem.objects.create(transaction=transaction, **item_data)
            product = item.product

            # Skip inventory stock deduction if product is a service, GCash, or custom other item
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
                # Total available stock in base units (e.g. kilos)
                total_base_qty = (product.stock_sacks * ratio) + product.stock_kilos

                # Determine sold quantity in base units
                if unit_type_upper == bulk_name_upper or unit_type_upper in ['SACK', 'CASE', 'BOX', 'PACK', 'BULK']:
                    sold_base_qty = Decimal(str(item.quantity)) * ratio
                else:
                    sold_base_qty = Decimal(str(item.quantity))

                # Deduct from unified pool
                new_total_base = max(Decimal('0.00'), total_base_qty - sold_base_qty)

                # Auto-calculate full bulk units and loose retail units
                product.stock_sacks = new_total_base // ratio
                product.stock_kilos = new_total_base % ratio
            else:
                # Single-unit product
                product.stock_kilos = max(Decimal('0.00'), product.stock_kilos - Decimal(str(item.quantity)))
                product.stock_sacks = Decimal('0.00')

            product.save()

        return transaction
