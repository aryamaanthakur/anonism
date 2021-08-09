from django.db import models
from django.contrib.auth.models import User

class Confession(models.Model):
    content = models.TextField(blank=False)
    visibility = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

class ConfessionRequest(models.Model):
    content = models.TextField(blank=False)
    approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

class ConfessionReport(models.Model):
    confession = models.ForeignKey(Confession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=False)
    complete = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)