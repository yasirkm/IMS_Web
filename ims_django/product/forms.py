from django import forms
from django.forms import ModelForm

from .models import Product


class Add_Product_Form(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ('available',)
        widgets = {
            'available':forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class':''}),
            'category': forms.TextInput(attrs={'class':''}),
            'description': forms.Textarea(attrs={'class':''})
        }

    template_name = 'form/add_product_form.html'
