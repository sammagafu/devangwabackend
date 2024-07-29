# Generated by Django 4.2.11 on 2024-07-04 20:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=255, unique=True),
        ),
    ]