from django.contrib import admin
from spongebob.models import BookBus, Contact, Bus, BookedSeats, BusBooking

# Register your models here.

admin.site.register(Contact)
admin.site.register(Bus)
admin.site.register(BookBus)
admin.site.register(BookedSeats)
admin.site.register(BusBooking)