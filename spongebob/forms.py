from dataclasses import field
from pyexpat import model
from socket import fromshare
from django import forms
from .models import BookBus

class BookBusForm(forms.ModelForm):
    class Meta:
        model = BookBus
        fields = [
            'phone_number',
            'bus_station',
            ]
