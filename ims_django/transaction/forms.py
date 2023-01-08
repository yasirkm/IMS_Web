from django.forms import ModelForm, ModelChoiceField
from .models import Transaction, Transaction_Detail

from product.models import Product

class Add_Transaction_Form(ModelForm):
    class Meta:
        model = Transaction
        fields = {'type', 'receipt_number'}
    
    template_name = 'form/input_form.html'

class Add_Transaction_Detail_Form(ModelForm):
    product_id = ModelChoiceField(queryset=Product.get_catalog())
    class Meta:
        model = Transaction_Detail
        exclude = ('transaction_id',)
        labels = {
            'product_id':'product'
        }
    template_name = 'form/input_form.html'
