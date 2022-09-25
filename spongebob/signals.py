from django.db.models.signals import post_save
from .models import Bus, BookedSeats
from django.dispatch import receiver
from .models import Profile


@receiver(post_save,sender=Bus)
def create_profile(sender,created,instance,**kwargs):
    if created:
        BookedSeats.objects.create(bus=instance)



@receiver(post_save,sender=Bus)
def save_profile(sender,instance,**kwargs):
    instance.bookedseats.save()


            