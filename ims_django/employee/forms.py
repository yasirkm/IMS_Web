from django.contrib.auth.models import User
from django.forms.models import fields_for_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from django import forms
from .models import Employee

class User_Registration_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'form/input_form.html'


class Employee_Registration_Form(ModelForm):
    class Meta:
        model = Employee
        exclude = ('user',)
        widgets ={
            'department': forms.HiddenInput(),
            'address': forms.TextInput(attrs={'class':'custom-class'})
        }
    template_name = 'form/registration_form.html'
    