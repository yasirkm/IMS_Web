from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import *

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

<<<<<<< HEAD


=======
def logout_view(request):
    logout(request)
    return redirect('login')

>>>>>>> fe95db8 (Add logout)
@login_required(login_url='login')
def dashboard_view(request):
    context = {"user" : request.user}
    return render(request, 'index.html')



@login_required(login_url='login')
@permission_required('employee.view_management')
def management_view(request):
    return render(request, 'management.html')


@login_required(login_url='login')
@permission_required('employee.register_user')
def register_view(request):
    return render(request, 'management/CreateNewAcc.html')


@login_required(login_url='login')
@permission_required('employee.register_user')
def choose_user_view(request):
    return render(request, 'management/ChooseUser.html')
