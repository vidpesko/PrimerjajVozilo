# Generated by Django 5.1 on 2024-09-29 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_rename_engine_vehicle_power'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='seller',
            field=models.CharField(choices=[('company', 'Company'), ('person', 'Person')], default=None, max_length=10, null=True),
        ),
    ]
