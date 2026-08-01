from django.contrib import admin
from .models import Category, Product, Customer, Transaction, TransactionItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price_per_sack', 'price_per_kilo', 'stock_sacks', 'stock_kilos', 'low_stock_threshold', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_number', 'total_utang')
    search_fields = ('name', 'contact_number')


class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'customer', 'total_amount', 'amount_paid', 'change_given', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('customer__name', 'id')
    inlines = [TransactionItemInline]


@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'product', 'unit_type', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('unit_type',)
    search_fields = ('product__name', 'transaction__id')
