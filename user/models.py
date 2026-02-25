from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)