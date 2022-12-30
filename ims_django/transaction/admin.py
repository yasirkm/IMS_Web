from django.contrib import admin
from .models import Transaction, Transaction_Detail

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Transaction_Detail)