from django.db import models
from django.contrib.auth.models import User, Permission

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
        'Management': {
            'employee': [
                'view_management',
                'register_user',
            ],
            'product': [
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
            ],
            'transaction': [
                'view_transaction',
                'do_transaction',
            ]
        },
        'Development': {
            'product': [
                'view_catalog',
                'view_product_name',
                'view_product_category',
                'view_product_description',
            ],
            'transaction': [
                'view_transaction',
            ]
        },
        'Finance': {
            'product': [
                'view_catalog',
                'view_product_name',
                'view_product_category',
                'view_product_description',
                'view_product_price',
                'view_product_stock',
                'edit_product_price',
            ],
            'transaction': [
                'view_transaction',
            ]
        },
        'Storage': {
            'product': [
                'view_catalog',
                'edit_catalog',
                'view_product_name',
                'view_product_category',
                'view_product_description',
                'view_product_stock',
                'edit_product_name',
                'edit_product_category',
                'edit_product_description',
            ],
            'transaction': [
                'view_transaction',
                'do_transaction'
            ]
        },
        'Production': {
            'product': [
                'view_catalog',
                'view_product_name',
                'view_product_category',
                'view_product_description',
                'view_product_stock',
            ]

        },
        'Sales': {
            'product': [
                'view_catalog',
                'view_product_name',
                'view_product_category',
                'view_product_description',
                'view_product_price',
                'view_product_stock',
            ]
        },
    }

    @classmethod
    def register(cls, username, password, first_name, last_name, phone_number, address, department, email=None, **kwargs):
        user = User(username=username, password=password,
                    first_name=first_name, last_name=last_name, email=email, **kwargs)
        profile = Employee(user=user, phone_number=phone_number,
                           address=address, department=department)

        for app, app_permissions in cls.DEPARTMENT_PERMISSION[department]:
            for permission in app_permissions:
                user.user_permissions.add(
                    Permission.objects.get(content_type__app_label=app, codename=permission))

        user.save()
        profile.save()

        return user
