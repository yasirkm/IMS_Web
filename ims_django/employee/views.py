from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import *
from django.forms.models import fields_for_model
from django.forms import ValidationError

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from transaction.models import Transaction
from django.apps import apps

from django.utils.datastructures import MultiValueDictKeyError


from .models import Employee
from .forms import *

# Create your views here.


def login_view(request):
    context = {'title': 'Login', 'next': ''}
    # Login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, 'Username or Password correct')
            if request.POST["next"]:
                return redirect(request.POST["next"])
            else:
                return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password incorrect')
    elif request.method == "GET" and "next" in request.GET:
        context["next"] = request.GET["next"]

    return render(request, 'login.html', context)


@login_required(login_url='login')
def test_login(request):
    print(request.user.is_authenticated)
    print(request.user.username)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'index.html')

@login_required(login_url='login')
@permission_required('employee.view_management', raise_exception=True)
def management_view(request):
    return render(request, 'management.html')


@login_required(login_url='login')
@permission_required('employee.register_user', raise_exception=True)
def register_view(request):
    if request.method == 'GET':
        registration_form = Registration_Form()
        try:
            department = request.GET['department']
        except MultiValueDictKeyError:
            return redirect('choose')
        context = {'form':registration_form, 'department':department}
        return render(request, 'management/CreateNewAcc.html', context)

    elif request.method == 'POST':
        registration_form = Registration_Form(request.POST)
        context = {'form':registration_form}
        if registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            password = registration_form.cleaned_data['password']
            email = registration_form.cleaned_data['email']
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            phone_number = registration_form.cleaned_data['phone_number']
            address = registration_form.cleaned_data['address']
            department = registration_form.cleaned_data['department']

            Employee.register(username=username, password=password,
                            first_name=first_name, last_name=last_name,
                            phone_number=phone_number, address=address,
                            department=department, email=email)
            redirect('management')
            
        else:
            return render(request, 'management/CreateNewAcc.html', context)


@login_required(login_url='login')
@permission_required('employee.register_user', raise_exception=True)
def choose_user_view(request):
    return render(request, 'management/ChooseUser.html')

def permission_denied_view(request):
    return render('403.html')

def test_form_view(request):
    if request.method=="GET":
        # form = Employee_Form()
        # form = User_Form()
        # form = NameForm()
        # form = Registration_Form()
        form = Registration_Form({'user':1})
        print(form.is_valid())
        context={'form':form}
        return render(request, 'test_form.html', context)
    elif request.method=="POST":
        print(request.POST)

def test_view(request):
    model=apps.get_model('employee.Employee')
    content_type = ContentType.objects.get_for_model(model)
    print(Permission.objects.get(content_type=content_type, codename='view_management'))
    return render('index.html')