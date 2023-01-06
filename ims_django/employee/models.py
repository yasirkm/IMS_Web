from django.db import models
from django.apps import apps
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class Employee(models.Model):
    class Meta:
        permissions = [
            ("view_management", "Can view management page"),
            ("register_user", "Can register another user"),
            ("configure_dynamic_pricing", "Can configure dynamic pricing"),
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.AutoField(primary_key=True)
    phone_number = models.TextField(blank=False, null=False)
    address = models.TextField()
    department = models.TextField(blank=False, null=False)

    # NEEDS TO BE CHANGED
    DEPARTMENT_PERMISSION = {
        'Management': {
            'employee.Employee': [
                'view_management',
                'register_user',
                'configure_dynamic_pricing',
            ],
            'product.Product': [
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
            'transaction.Transaction': [
                'view_transaction_history',
                'do_transaction',
            ]
        },
        'Development': {
            'product.Product': [
                'view_catalog',
                'view_product_name',
                'view_product_category',
                'view_product_description',
            ],
            'transaction.Transaction': [
                'view_transaction',
            ]
        },
        'Finance': {
            'product.Product': [
                'view_catalog',
                'view_product_name',
                'view_product_category',
                'view_product_description',
                'view_product_price',
                'view_product_stock',
                'edit_product_price',
            ],
            'transaction.Transaction': [
                'view_transaction',
            ]
        },
        'Storage': {
            'product.Product': [
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
            'transaction.Transaction': [
                'view_transaction',
                'do_transaction'
            ]
        },
        'Production': {
            'product.Product': [
                'view_catalog',
                'view_product_name',
                'view_product_category',
                'view_product_description',
                'view_product_stock',
            ]

        },
        'Sales': {
            'product.Product': [
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
    def register(cls, user, phone_number, address, department, **kwargs):
        profile = Employee(user=user, phone_number=phone_number,
                           address=address, department=department)

        # NEEDS TO BE CHANGED
        for app, app_permissions in cls.DEPARTMENT_PERMISSION[department].items():
            for permission in app_permissions:
                model = apps.get_model(app)
                content_type=ContentType.objects.get_for_model(model)
                print(app, permission)
                perm = Permission.objects.get(content_type=content_type, codename=permission)
                user.user_permissions.add(perm)
        profile.save()

        return 
        
    def update_permission(self):
        user = self.user
        for app, app_permissions in Employee.DEPARTMENT_PERMISSION[self.department].items():
            for permission in app_permissions:
                model = apps.get_model(app)
                content_type=ContentType.objects.get_for_model(model)
                print(app, permission)
                perm = Permission.objects.get(content_type=content_type, codename=permission)
                user.user_permissions.add(perm)
        self.save()
