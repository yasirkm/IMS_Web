from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.AutoField(primary_key=True)
    username = models.TextField(blank=False, null=False)
    password = models.TextField(blank=False, null=False)
    name = models.TextField(blank=False, null=False)
    phone_number = models.TextField(blank=False, null=False)
    address = models.TextField()
    department = models.TextField(blank=False, null=False)