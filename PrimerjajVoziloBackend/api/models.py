from django.db import models


VEHICLE_TYPES = {
    "car": "Car",
    "motorcycle": "Motorcycle"
}

SELLER_TYPES = {
    "company": "Company",
    "person": "Person"
}


class Vehicle(models.Model):
    avtonet_id = models.IntegerField(unique=True)
    # user = models.ManyToManyField("auth.user", related_name="vehicles")

    created = models.DateTimeField(auto_now_add=True)  # When was model created / first scraped
    updated = models.DateTimeField(auto_now=True)  # When was model last updated / scraped

    # Vehicle info
    url = models.URLField(max_length=500)
    vehicleType = models.CharField(max_length=50, choices=VEHICLE_TYPES, null=True, default=None)
    images = models.JSONField(default=list)
    seller = models.CharField(max_length=10, choices=SELLER_TYPES, null=True, default=None)

    name = models.CharField(max_length=500, null=True, default=None)
    price = models.CharField(max_length=50, null=True, default=None)
    mileage = models.CharField(max_length=50, null=True, default=None)
    power = models.CharField(max_length=100, null=True, default=None)
    firstRegistration = models.CharField(max_length=20, null=True, default=None)
    description = models.TextField(null=True, default=None)
    location = models.CharField(max_length=100, null=True, default=None)
    phoneNumber = models.CharField(max_length=20, null=True, default=None)

    other = models.JSONField(null=True, default=None)
