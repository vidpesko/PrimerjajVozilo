# Generated by Django 5.1 on 2024-08-26 11:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avtonet_id', models.IntegerField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('price', models.IntegerField()),
                ('user', models.ManyToManyField(related_name='vehicles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
