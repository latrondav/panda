from django.contrib import admin
from spongebob.models import bookbus, contact, buses, bookedseats

# Register your models here.

admin.site.register(contact)
admin.site.register(buses)
admin.site.register(bookbus)
admin.site.register(bookedseats)