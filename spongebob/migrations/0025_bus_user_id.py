# Generated by Django 4.0.6 on 2022-10-02 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spongebob', '0024_rename_pick_up_station_busbooking_bus_station'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]