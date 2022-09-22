from distutils.command.upload import upload
import email
from email import message
from django.db import models

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=200, null=False, blank=False)
    message = models.TextField(max_length=200,)

    def __str__(self):
        return str(self.name)

class buses(models.Model):
    busimage = models.ImageField(null=True, blank=True, upload_to="busimages/")
    busname = models.CharField(max_length=200, null=False, blank=False)
    busfrom = models.CharField(max_length=200, null=False, blank=False)
    busto = models.CharField(max_length=200, null=False, blank=False)
    busdate = models.DateField(max_length=200,)
    bustime = models.TimeField(max_length=200,)

    def __str__(self):
        return str(self.busname)

    