from django.db import models

from user.models import User


# Create your models here.

class Notification(models.Model):
    CHANNEL_TYPES = (
        ("EMAIL", "Email"),
        ("SMS", "SMS"),
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reference = models.CharField(max_length=10, blank=True, null=True)
    channel = models.CharField(max_length=20, choices=CHANNEL_TYPES, default="EMAIL")
    created_at = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20)
