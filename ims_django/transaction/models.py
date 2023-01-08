from datetime import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.forms.models import fields_for_model


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
    TYPE_CHOOSE = [
        ('IN', 'IN'),
        ('OUT', 'OUT'),
        ('RETURN', 'RETURN'),
        ]
    type = models.CharField(blank=False, null=False, choices=TYPE_CHOOSE, max_length=10)
    receipt_number = models.CharField(max_length=20, blank=True, null=True)
    date_time = models.DateTimeField(blank=False, null=False)


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
        transactions = cls.objects.all().order_by('transaction_id')
        return transactions

    
class Transaction_Detail(models.Model):
    class Meta:
        unique_together = (('transaction_id', 'product_id'),)

    transaction_id = models.ForeignKey(
        Transaction, on_delete=models.PROTECT, blank=False, null=False)
    product_id = models.ForeignKey(
        Product, on_delete=models.PROTECT, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    price_at_transaction = models.DecimalField(blank=False, null=False, default=0, max_digits=19, decimal_places=4, validators=[MinValueValidator(Decimal('0.00'))])

    @classmethod
    def get_transaction_details(cls, transaction):
        transaction_details = cls.objects.filter(transaction_id=transaction)
        return transaction_details