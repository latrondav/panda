# Generated by Django 4.0.6 on 2022-10-02 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spongebob', '0028_rename_price_busbooking_unit_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='busbooking',
            name='payment_method',
            field=models.CharField(default='Cash On Departure', max_length=100),
        ),
    ]
