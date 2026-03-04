from django.db import models

from user.models import User


# Create your models here.

class Notification(models.Model):
    CHANNEL_TYPES = (
        ("EMAIL", "Email"),
        ("SMS", "SMS"),
    )
    wallet_number = models.CharField(max_length=10, null=True, blank=True)
    message = models.TextField(max_length=500, null=True, blank=True)
    reference = models.CharField(max_length=10, blank=True, null=True)
    channel = models.CharField(max_length=20, choices=CHANNEL_TYPES, default="EMAIL")
    created_at = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=1000, default="EMAIL")
    is_read = models.BooleanField(default=False)
