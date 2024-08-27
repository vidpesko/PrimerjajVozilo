from django.db import models


# Create your models here.
class Vehicle(models.Model):
    avtonet_id = models.IntegerField(unique=True)
    user = models.ManyToManyField("auth.user", related_name="vehicles")

    created = models.DateTimeField(auto_now_add=True)  # When was model created / first scraped
    updated = models.DateTimeField(auto_now=True)  # When was model last updated / scraped

    # Vehicle info
    url = models.URLField(max_length=500)
    name = models.CharField(max_length=500)
    price = models.IntegerField()
