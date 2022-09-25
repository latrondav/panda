from distutils.command.upload import upload
import email
from email import message
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=200, null=False, blank=False)
    message = models.TextField(max_length=200,)

    def __str__(self):
        return str(self.name)

class Bus(models.Model):
    name = models.CharField(default='Bus',max_length=100)
    image=models.ImageField(upload_to='', default='salafy_4.png')
    number_plate =models.CharField(max_length=100, default="UBA 123A")
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    no_of_seats = models.DecimalField(decimal_places=0, max_digits=2)
    remaining_seats = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=0, max_digits=6)
    date = models.DateField()
    departure_time = models.TimeField()

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("bus-detail", kwargs={"pk": self.pk})
    
class User(models.Model):
    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})
    


class BookedSeats(models.Model):
        bus=models.OneToOneField(Bus, on_delete=models.CASCADE)
        seats=models.CharField(max_length=100, default='0')

        def __str__(self):
            return str(self.bus)


class BookBus(models.Model):
    no_of_seats=models.IntegerField()
    seat_no=models.IntegerField()
    total_price=models.IntegerField()
    phone_number=models.IntegerField()
    bus_station=models.CharField(max_length=100)

    

class BusBooking(models.Model):
    user_name=models.CharField(max_length=100)
    user_email=models.EmailField()
    user_id=models.IntegerField(default=0)
    source=models.CharField(max_length=30)
    pick_up_station=models.CharField(max_length=100,default='Home station')
    destination=models.CharField(max_length=30)
    date=models.DateField()
    price=models.IntegerField()
    phone_no=models.IntegerField(default=+254000000)
    time=models.TimeField()
    no_of_seats=models.IntegerField(default=0)
    bus_name=models.CharField(max_length=20)
    bus_id=models.IntegerField()
    seat_numbers=models.CharField(max_length=100, default='')

    def __str__(self):
        return str(self.date)
   