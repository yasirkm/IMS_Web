from django.db import models

# Create your models here.
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    username = models.CharField(blank=False, null=False)
    password = models.CharField(blank=False, null=False)
    name = models.CharField(blank=False, null=False)
    phone_number = models.CharField(blank=False, null=False)
    address = models.TextField()
    department = models.CharField(blank=False, null=False)