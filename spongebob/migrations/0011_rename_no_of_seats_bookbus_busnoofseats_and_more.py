# Generated by Django 4.1.1 on 2022-09-23 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spongebob', '0010_bookedseats'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookbus',
            old_name='no_of_seats',
            new_name='busnoofseats',
        ),
        migrations.AlterField(
            model_name='bookedseats',
            name='seats',
            field=models.CharField(default='0', max_length=200),
        ),
    ]