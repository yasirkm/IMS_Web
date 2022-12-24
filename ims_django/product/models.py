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