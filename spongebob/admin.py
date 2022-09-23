from django.contrib import admin
from spongebob.models import BookBus, contact, buses

# Register your models here.

admin.site.register(contact)
admin.site.register(buses)
admin.site.register(BookBus)