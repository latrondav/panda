# Generated by Django 4.0.6 on 2022-09-27 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spongebob', '0021_alter_bus_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedseats',
            name='bus',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spongebob.bus'),
        ),
    ]
