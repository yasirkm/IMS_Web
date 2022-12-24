from django.db import models

# Create your models here.
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    username = models.TextField(blank=False, null=False)
    password = models.TextField(blank=False, null=False)
    name = models.TextField(blank=False, null=False)
    phone_number = models.TextField(blank=False, null=False)
    address = models.TextField()
    department = models.TextField(blank=False, null=False)