from django.db import models
from django.contrib.auth.models import User, Permission


from product.models import Product
from transaction.models import Transaction

# Create your models here.


class Employee(models.Model):
    class Meta:
        permissions = [
            ("register_user", "Can register another user"),
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.AutoField(primary_key=True)
    phone_number = models.TextField(blank=False, null=False)
    address = models.TextField()
    department = models.TextField(blank=False, null=False)

    DEPARTMENT_PERMISSION = {
        'Management': [
            'view_management',
            'register_user',
            'view_catalog',
            'edit_catalog',
            'view_product_name',
            'view_product_category',
            'view_product_description',
            'view_product_price',
            'view_product_stock',
            'edit_product_name',
            'edit_product_category',
            'edit_product_description',
            'edit_product_price',
            'edit_product_stock',
            'view_transaction',
            'do_transaction',
        ],
        'Development': [
            'view_catalog',
            'view_product_name',
            'view_product_category',
            'view_product_description',
            'view_transaction',
        ],
        'Finance': [
            'view_catalog',
            'view_product_name',
            'view_product_category',
            'view_product_description',
            'view_product_price',
            'view_product_stock',
            'edit_product_price',
            'view_transaction',
        ],
        'Storage': [
            'view_catalog',
            'edit_catalog',
            'view_product_name',
            'view_product_category',
            'view_product_description',
            'view_product_stock',
            'edit_product_name',
            'edit_product_category',
            'edit_product_description',
            'view_transaction',
            'do_Transaction'

        ],
        'Production': [
            'view_catalog',
            'view_product_name',
            'view_product_category',
            'view_product_description',
            'view_product_stock',
        ],
        'Sales': [
            'view_catalog',
            'view_product_name',
            'view_product_category',
            'view_product_description',
            'view_product_price',
            'view_product_stock',
        ],
    }

    @classmethod
    def register(cls, username, password, first_name, last_name, phone_number, address, department, email=None, **kwargs):
        user = User(username=username, password=password,
                    first_name=first_name, last_name=last_name, email=email, **kwargs)
        profile = Employee(user=user, phone_number=phone_number,
                           address=address, department=department)

        for codename in cls.DEPARTMENT_PERMISSION[department]:
            user.user_permissions.add(
                Permission.objects.get(codename=codename))

        user.save()
        profile.save()

        return user
