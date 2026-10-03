from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    unit_bulk_name = models.CharField(max_length=50, default='Sack', blank=True, null=True)
    unit_retail_name = models.CharField(max_length=50, default='Kilo', blank=True, null=True)
    price_per_sack = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_kilo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_per_sack = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_per_kilo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_sacks = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_kilos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    units_per_bulk = models.DecimalField(max_digits=10, decimal_places=2, default=50.00, null=True, blank=True)
    low_stock_threshold = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    is_service = models.BooleanField(default=False)

    @property
    def total_base_stock(self):
        ratio = self.units_per_bulk or Decimal('1.00')
        if self.unit_bulk_name and ratio > 1:
            return (self.stock_sacks * ratio) + self.stock_kilos
        return self.stock_kilos

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    total_utang = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('CASH', 'Cash'),
        ('GCASH', 'GCash'),
        ('CREDIT', 'Credit'),
        ('DEBT_PAYMENT', 'Debt Payment'),
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    change_given = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx #{self.id} ({self.transaction_type}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='transaction_items')
    unit_type = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} {self.unit_type}(s) of {self.product.name}"
