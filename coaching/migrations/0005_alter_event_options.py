# Generated by Django 4.2.11 on 2024-06-27 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coaching', '0004_alter_event_discount_deadline'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_time']},
        ),
    ]
