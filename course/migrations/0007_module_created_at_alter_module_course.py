# Generated by Django 4.2.11 on 2024-06-24 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_alter_module_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modules', to='course.course'),
        ),
    ]
