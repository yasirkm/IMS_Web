from django.db import models

# Create your models here.


class Product(models.Model):
    class Meta:
        permissions = [
            ("view_catalog", "can view catalog"),
            ("edit_catalog", "can edit catalog"),
            ("view_product_name", "can view product name"),
            ("view_product_category", "Can view product category"),
            ("view_product_description", "Can view product description"),
            ("view_product_price", "Can view product price"),
            ("view_product_stock", "Can view product stock"),
            ("edit_product_name", "can edit product name"),
            ("edit_product_category", "Can edit product category"),
            ("edit_product_description", "Can edit product description"),
            ("edit_product_price", "Can edit product price"),
            ("edit_product_stock", "Can edit product stock"),
        ]
    product_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False, null=False)
    category = models.TextField(blank=False, null=False)
    price = models.DecimalField(blank=False, null=False, default=0, max_digits=19, decimal_places=4)
    stock = models.IntegerField(default=0, blank=False, null=False)
    description = models.TextField()
    available = models.BooleanField(default=True)

    @classmethod
    def add_product(cls, name, category, price, description):
        new_product = cls(name=name, category=category,
                          price=price, description=description)
        new_product.save()
        return new_product

    @classmethod
    def get_catalog(cls):
        return cls.objects.filter(available=True).order_by('product_id')

    @classmethod
    def get_by_id(cls, product_id):
        return cls.objects.get(product_id=product_id)

    def edit(self, **kwargs):
        attributes = (
            attribute.name for attribute in Product._meta.get_fields())

        attributes_value_edit = {
            attribute: new_value for attribute in attributes if attribute in kwargs}
        for attr, new_value in attributes_value_edit.items():
            setattr(self, attr, new_value)

        self.save(update_fields=[attributes_value_edit])

    def delete(self):
        self.available = False
        self.save()
