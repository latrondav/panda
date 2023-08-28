from django.db.models.signals import post_save
from .models import Bus, BookedSeats
from django.dispatch import receiver

@receiver(post_save,sender=Bus)
def create_bookedseat(sender,instance,created,**kwargs):
    if created:
        BookedSeats.objects.create(bus=instance)


@receiver(post_save,sender=Bus)
def save_bookedseat(sender,instance, **kwargs):
    instance.bookedseats.save()


            