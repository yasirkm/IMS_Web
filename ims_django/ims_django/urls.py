"""ims_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

from employee.views import *
from transaction.views import *
from product.views import *


urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('management/', management_view, name='management'),
    path('choose/', choose_user_view, name='temp_choose'),
    path('transaction/', transaction_view, name='transaction'),
    path('catalog/', catalog_view, name='catalog'),
    path('test/', test_login)
]
