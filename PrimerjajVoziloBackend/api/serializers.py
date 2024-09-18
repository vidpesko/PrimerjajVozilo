import copy

from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import Vehicle


VEHICLE_RESPONSE_SCHEMA = {
    "id": None,
    "required": {
        "name": None,
        "images": [],
        "mileage": None,  # 0 mileage means new car, None means unkown
        "engine": None,
        "firstRegistration": None,
        "price": None,  # If None, price is set to "Poklicite za ceno!"
        "location": None,
        "phoneNumber": None,
    },
    "other": None,
    "metadata": {"url": None, "updated": None, "vehicleType": None, "seller": None, "status": None},
}


def fill_dict_values(keyword, response: dict, data: dict):
    _response = copy.deepcopy(response)
    for key, value in _response[keyword].items():
        _response[keyword][key] = data.get(key, value)
    return _response


def generate_response_with_schema(data: dict):
    response = copy.deepcopy(VEHICLE_RESPONSE_SCHEMA)
    # Set values
    response["id"] = data.get("avtonet_id", response["id"])

    for keyword in ["required", "metadata"]:
        response = fill_dict_values(keyword, response, data)

    response["other"] = data["other"]

    return response


class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Generate response using VEHICLE_RESPONSE_SCHEMA
        data = generate_response_with_schema(data)
        return data

    def to_internal_value(self, data):
        response = {
            "avtonet_id": data["id"],
            "url": data["url"],
        }

        del data["url"]
        del data["id"]

        for key in VEHICLE_RESPONSE_SCHEMA["required"].keys():
            if not key in data:
                continue
            value = data.get(key)
            response[key] = value
            del data[key]

        response["other"] = {}
        for key, value in data.items():
            response["other"][key] = value

        return response

    class Meta:
        model = Vehicle
        fields = [
            "avtonet_id",
            "updated",
            "name",
            "images",
            "url",
            "user",
            "mileage",
            "engine",
            "firstRegistration",
            "price",
            "location",
            "phoneNumber",
            "vehicleType",
            "other",
        ]
