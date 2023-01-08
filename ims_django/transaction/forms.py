from django.forms import ModelForm, ModelChoiceField
from django import forms
from .models import Transaction, Transaction_Detail

from product.models import Product

class Add_Transaction_Form(ModelForm):
    class Meta:
        model = Transaction
        fields = {'type', 'receipt_number'}
    
    template_name = 'form/add_transaction_form.html'

class Add_Transaction_Detail_Form(ModelForm):
    product_id = ModelChoiceField(queryset=Product.get_catalog(), label='product')
    class Meta:
        model = Transaction_Detail
        exclude = ('transaction_id', 'price_at_transaction')
        widgets = {
            'quantity':forms.NumberInput(attrs={'min':1})
        }
    template_name = 'form/add_transaction_form.html'
