from django.shortcuts import render
from django.contrib.auth.decorators import *

from .models import Product
from .forms import *

# Create your views here.


@login_required(login_url='login')
@permission_required('product.view_catalog', raise_exception=True)
def catalog_view(request):
    page_title = 'Catalog'

    if request.method == 'GET':
        catalog = Product.get_catalog()
        add_product_form = Add_Product_Form()
        context = {'catalog': catalog, 'title': page_title, 'form':add_product_form}
        return render(request, 'catalog.html', context)

    elif request.method == 'POST':
        add_product_form = Add_Product_Form(request.POST)
        if add_product_form.is_valid():
            add_product_form.save()
            catalog = Product.get_catalog()
            context = {'catalog': catalog, 'title': page_title, 'form':add_product_form}
        else:
            for field in add_product_form:
                print(field.errors)
            context = {'catalog': catalog, 'title': page_title, 'form':add_product_form}
        return render(request, 'catalog.html', context)