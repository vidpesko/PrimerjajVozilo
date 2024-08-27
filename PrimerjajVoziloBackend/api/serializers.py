from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Vehicle
        fields = ["avtonet_id", "updated", "name", "url", "user"]
