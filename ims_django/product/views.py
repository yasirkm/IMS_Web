import json

from django.shortcuts import render
from django.contrib.auth.decorators import *
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .models import Product
from .forms import *

# Create your views here.

@login_required(login_url='login')
@permission_required('product.view_catalog', raise_exception=True)
def catalog_view(request):
    page_title = 'Catalog'
    add_product_form = Add_Product_Form()
    catalog = Product.get_catalog()

    if request.method == 'GET':
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
            product_id = new_fields_value['id']
            product = Product.get_catalog().get(pk=product_id)
            for field, permission in field_permission.items():
                print(field, permission)
                if field in new_fields_value:
                    print(field, permission)
                    if request.user.has_perm(permission):
                        print(f'added {field}')
                        setattr(product, field, new_fields_value[field])
                    else:
                        raise PermissionError(f'You do not have the permission to edit product {field}')

            product.full_clean()
            product.save()
            response['success'] = True
            response['message'] = 'Product successfully edited'

        except ObjectDoesNotExist:
            response['message']='That product is not on database'
        except KeyError:
            response['message']='Invalid request sent'
        except ValidationError:
            response['message']='Invalid value'
        except PermissionError as e:
            response['message']=str(e)

        return JsonResponse(response)

    elif request.method == 'DELETE':
        response = {'success':False, 'message':None}
        data = json.loads(request.body)
        try:
            product_id = data['id']
            product = Product.get_catalog().get(pk=product_id)
            product.delete()
            response['success'] = True
            response['message'] = 'Product successfully deleted'
        except ObjectDoesNotExist:
            response['message']='That product is not on database'
        except KeyError:
            response['message']='Invalid request sent'

        return JsonResponse(response)