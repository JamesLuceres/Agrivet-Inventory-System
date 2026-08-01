from rest_framework import serializers
from .models import Category, Product, Customer, Transaction, TransactionItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = '__all__'


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

        # 2. Loop through nested items to create them and deduct product stock
        for item_data in items_data:
            item = TransactionItem.objects.create(transaction=transaction, **item_data)
            product = item.product
            if item.unit_type == 'SACK':
                product.stock_sacks -= item.quantity
            elif item.unit_type == 'KILO':
                product.stock_kilos -= item.quantity
            product.save()

        return transaction
