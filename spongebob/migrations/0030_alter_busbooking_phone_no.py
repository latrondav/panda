# Generated by Django 4.0.6 on 2022-10-02 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spongebob', '0029_busbooking_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busbooking',
            name='phone_no',
            field=models.IntegerField(default=256000000),
        ),
    ]
