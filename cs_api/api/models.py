from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    balance = models.FloatField(blank=False, null=False, default=0.0)

class Transaction(models.Model):
    origin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="origin")

    destination = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="destination")

    quantity = models.FloatField(blank=False, null=False, default=0.0)

    date_realized = models.DateTimeField(blank=False, null=False, auto_now_add=True)
