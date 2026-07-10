from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    # Yeh customer kis dukan (User) ka hai, taaki ek dukandaar doosre ka data na dekh sake
    shopkeeper = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00) # Max udhaar limit
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.shopkeeper.username})"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('UDHAAR', 'Udhaar (Debit)'),
        ('JAMA', 'Jama (Credit)'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True, null=True, help_text="Kya saaman le gaya? (e.g., Surf Excel, Chawal)")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.transaction_type} - ₹{self.amount}"