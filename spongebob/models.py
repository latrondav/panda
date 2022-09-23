from distutils.command.upload import upload
import email
from email import message
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=200, null=False, blank=False)
    message = models.TextField(max_length=200,)

    def __str__(self):
        return str(self.name)

class buses(models.Model):
    busimage = models.ImageField(null=True, blank=True, upload_to="busimages/", default='bus.jpg')
    busname = models.CharField(max_length=200, null=False, blank=False)
    busnumplate = models.CharField(max_length=200, null=False, blank=False, default='UBA 123A')
    busfrom = models.CharField(max_length=200, null=False, blank=False)
    busto = models.CharField(max_length=200, null=False, blank=False)
    busnoofseats = models.DecimalField(decimal_places=0, max_digits=2, default=60)
    busremseats = models.DecimalField(decimal_places=0, max_digits=2, default=60)
    busprice = models.DecimalField(decimal_places=0, max_digits=2, default=0)
    busdate = models.DateField()
    bustime = models.TimeField()

    def __str__(self):
        return str(self.busname)

class BookBus(models.Model):
    no_of_seats = models.IntegerField()
    seat_no = models.IntegerField()
    total_price = models.IntegerField()
    phone_number = models.IntegerField()
    bus_station = models.CharField(max_length=200)

    def __str__():
        return str(User)