# Generated by Django 4.2.11 on 2025-05-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('mpesa', 'M-Pesa'), ('vodacom', 'Vodacom'), ('airtel', 'Airtel'), ('mtn', 'MTN'), ('card', 'Card')], default='mpesa', max_length=20),
        ),
    ]
