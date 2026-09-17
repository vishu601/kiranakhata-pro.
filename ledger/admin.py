from django.contrib import admin
from .models import Customer, Transaction

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'shopkeeper', 'credit_limit', 'created_at')
    search_fields = ('name', 'phone')
    list_filter = ('shopkeeper',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'transaction_type', 'date')
    list_filter = ('transaction_type', 'date')
    search_fields = ('customer__name', 'description')