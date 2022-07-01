import email
from email import message
from django.db import models

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=200, null=False, blank=False)
    message = models.TextField(max_length=200,)

    