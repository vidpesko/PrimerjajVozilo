from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import Vehicle


class UserSerializer(serializers.ModelSerializer):
    vehicles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Vehicle.objects.all()
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "vehicles"]
