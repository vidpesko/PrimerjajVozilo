# Generated by Django 5.1 on 2024-09-17 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_vehicle_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='images',
        ),
    ]
