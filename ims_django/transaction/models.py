from django.db import models
from employee.models import Employee
from product.models import Product

# Create your models here.
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=False, null=False)
    type = models.TextField(blank=False, null=False)
    receipt_number = models.TextField()
    date_time = models.DateTimeField(blank=False, null=False)

class Transaction_Detail(models.Model):
    class Meta:
        unique_together = (('transaction_id', 'product_id'),)
        
    transaction_id = models.ForeignKey(Transaction, on_delete=models.PROTECT, blank=False, null=False)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)