# Generated by Django 4.2.11 on 2024-06-16 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coaching', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='coaching.event'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
