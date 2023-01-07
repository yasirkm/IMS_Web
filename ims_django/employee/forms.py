from django.contrib.auth.models import User
from django.forms.models import fields_for_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from django import forms
from .models import Employee


class Login_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    template_name = 'form_snippet.html'

class Employee_Form(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class Test_Form(forms.Form):
    name=forms.CharField()

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class Registration_Form(forms.Form):
    user_field = fields_for_model(User)
    employee_field = fields_for_model(Employee)
    template_name = 'form/input_form.html'

    username = user_field['username']
    email = user_field['email']
    password = user_field['password']
    password.widget = forms.PasswordInput()
    first_name = user_field['first_name']
    last_name = user_field['last_name']

    phone_number = employee_field['phone_number']
    address = employee_field['address']
    department = employee_field['department']
    department.widget = forms.HiddenInput()
    department.hidden = True

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
            'department': forms.HiddenInput()
        }
    template_name = 'form/input_form.html'
    # department = fields_for_model(Employee)['department']
    # department.widget = forms.HiddenInput()
    # department.hidden=True
    