from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'index.html')

def management_view(request):
    return render(request, 'management.html')

def register_view(request):
    return render(request, 'management/CreateNewAcc.html')

def choose_user_view(request):
    return render(request, 'management/ChooseUser.html')