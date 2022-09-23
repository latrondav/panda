# Generated by Django 4.1.1 on 2022-09-23 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spongebob', '0005_alter_buses_busimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='buses',
            name='busnoofseats',
            field=models.DecimalField(decimal_places=0, default=60, max_digits=2),
        ),
        migrations.AddField(
            model_name='buses',
            name='busremseats',
            field=models.DecimalField(decimal_places=0, default=60, max_digits=2),
        ),
        migrations.AddField(
            model_name='buses',
            name='price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2),
        ),
        migrations.AlterField(
            model_name='buses',
            name='busdate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='buses',
            name='busimage',
            field=models.ImageField(blank=True, default='bus.jpg', null=True, upload_to='busimages/'),
        ),
        migrations.AlterField(
            model_name='buses',
            name='bustime',
            field=models.TimeField(),
        ),
    ]