import json

from django.shortcuts import render
from django.contrib.auth.decorators import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

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
            context = {'catalog': catalog, 'title': page_title, 'form':Add_Product_Form()}
        else:
            for field in add_product_form:
                print(field.errors)
            context = {'catalog': catalog, 'title': page_title, 'form':add_product_form}
        return render(request, 'catalog.html', context)

    elif request.method == 'PATCH':
        response = {'success':False, 'message':None}
        field_permission = {
            'name':'product.edit_product_name',
            'category':'product.edit_product_category',
            'description':'product.edit_product_description',
            'price':'product.edit_product_price',
            'stock':'product.edit_product_stock',
            'available':'product.edit_catalog',
        }
        new_fields_value = json.loads(request.body)
        try:
            product = Product.get_catalog().get(pk=new_fields_value['id'])
            form = Add_Product_Form(instance=product)
            for field, permission in field_permission:
                if request.user.has_perm(permission):
                    form.fields[field] = new_fields_value[field]
                else:
                    response['message']=f'You do not have the permission to edit product {field}'
                    break

            if form.is_valid():
                form.save()
            else :
                    response['message']=f'Invalid value'
        except ObjectDoesNotExist:
            response['message']='That product is not on database'
        except KeyError:
            response['message']='Invalid request sent'

        return JsonResponse(response)