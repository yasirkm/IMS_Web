from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False, null=False)
    category = models.TextField(blank=False, null=False)
    price = models.DecimalField(blank=False, null=False, max_digits=19, decimal_places=4)
    stock = models.IntegerField(default=0, blank=False, null=False)
    description = models.TextField()
    available = models.BooleanField(default=True)

    @classmethod
    def add_product(cls, name, category, price, description):
        new_product = cls(name=name, category=category, price=price, description=description)
        new_product.save()
        return new_product

    @classmethod
    def get_catalog(cls):
        return cls.objects.filter(available=True).order_by('product_id')

    @classmethod
    def get_by_id(cls, product_id):
        return cls.objects.get(product_id=product_id)

    def edit(self, **kwargs):
        attributes = (attribute.name for attribute in Product._meta.get_fields())

        attributes_value_edit = {attribute:new_value for attribute in attributes if attribute in kwargs}
        for attr, new_value in attributes_value_edit.items():
            setattr(self, attr, new_value)

        self.save(update_fields=[attributes_value_edit])

    def delete(self):
        self.available=False
        self.save()
