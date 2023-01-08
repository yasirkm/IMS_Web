from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.


class Transaction(models.Model):
    class Meta:
        permissions = [
            ("view_transaction_history", "Can view transaction history"),
            ("do_transaction", "Can add new transactions"),
        ]
    transaction_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
    type = models.TextField(blank=False, null=False)
    receipt_number = models.TextField()
    date_time = models.DateTimeField(blank=False, null=False)

    TYPE_CHOOSE = [
        ('IN', 'IN'),
        ('OUT', 'OUT'),
        ('RETURN', 'RETURN'),
        ]

    @classmethod
    def add_transaction(cls, employee_id, type, receipt_number, transaction_details):
        date_time = datetime.now()
        new_transaction = Transaction(
            employee_id=employee_id, type=type, receipt_number=receipt_number)
        new_transaction_details = []
        for product, quantity in transaction_details:
            new_transaction_details.append(Transaction_Detail(new_transaction, product, quantity))
            if type == 'OUT':
                product-=quantity
            else:
                product.stock+=quantity

        new_transaction.save()
        product.save()
        for new_transaction_detail in new_transaction_details:
            new_transaction_detail.save()

    @classmethod
    def get_transaction_history(cls):
        transactions = cls.get_transactions()
        transaction_history = []
        for transaction in transactions:
            transaction_detail = Transaction_Detail.get_transaction_details(transaction)
            transaction_history.append((transaction, transaction_detail))

        return transaction_history

    @classmethod
    def get_transactions(cls):
        transactions = cls.objects.all()
        return transactions

    
class Transaction_Detail(models.Model):
    class Meta:
        unique_together = (('transaction_id', 'product_id'),)

    transaction_id = models.ForeignKey(
        Transaction, on_delete=models.PROTECT, blank=False, null=False)
    product_id = models.ForeignKey(
        Product, on_delete=models.PROTECT, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)

    @classmethod
    def get_transaction_details(cls, transaction):
        transaction_details = cls.objects.filter(transaction_id=transaction)
        return transaction_details