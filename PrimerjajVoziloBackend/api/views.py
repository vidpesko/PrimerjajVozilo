# Interface to Scraper library. Tasked with scraping, creating and updating neccessary vehicles in db
import re

from pydantic import BaseModel

from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import Vehicle
from api.serializers import VehicleSerializer
from Scraper.scraper import scrape_url, run_until_complete


class VehicleList(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset to return only Vehicles that user have
        """
        user = self.request.user
        return Vehicle.objects.filter(user=user)


# Used to retrieve vehicle by url or id. It will also check if model stored is older than predifined value. If it is older, model will be first updated and than returned
@api_view(["GET"])
def get_vehicle(request):
    # Get id to filter db
    vehicle_id = request.GET.get("id", None)
    vehicle_url = request.GET.get("url", None)

    # Parameter validation
    if not vehicle_url and not vehicle_id:
        return Response({"error": "Ni parametrov"}, status=400)
    try:
        vehicle_id = int(vehicle_id)
    except ValueError:
        if not vehicle_url:
            return Response({"error": "ID vozila ni stevilo"}, status=400)
        else:
            vehicle_id = None

    vehicle_key = {"avtonet_id": vehicle_id} if vehicle_id else {"url": vehicle_url}

    # Get vehicle object
    try:
        vehicle = Vehicle.objects.get(**vehicle_key)
    # If vehicle is not found in db, use scraper to check on avto.net
    except Vehicle.DoesNotExist:
        return Response({"error": "Vozilo s parametri ne obstaja"})

    # Serialize object and return it
    serializer = VehicleSerializer(vehicle)

    return Response(serializer.data)


@api_view(["GET"])
def update_model(request):
    # Check if url parameter was provided, else 400
    try:
        vehicle_url = request.GET["url"]
    except KeyError:
        return Response({"error": "Url parameter ni bil izpolnjen"}, status=400)

    # Check if url matches regex
    match = re.match("https://www.avto.net/Ads/details.asp", vehicle_url)
    if not match:
        return Response(
            {"error": "Vnesen url je v napacnem formatu. Ali je res link do avto.net?"},
            status=400,
        )

    # try:
    vehicle_data = run_until_complete(scrape_url, vehicle_url)
    # except Exception as e:
    #     return Response({"error": "Prislo je do napake!"}, status=400)

    # Check if returned object is Vehicle schema
    # If it isn't, it means an error occured
    if not isinstance(vehicle_data, BaseModel):
        return Response(vehicle_data, status=400)

    # Construct Vehicle model instance
    vehicle_data = vehicle_data.model_dump()

    if request.user.is_authenticated:
        # If user is logged in, check if that vehicle is already in his fleet. If it isn't, add vehicle to his fleet
        print(request.user)
        # vehicle = Vehicle.objects.update_or_create(**vehicle_data)
    else:
        # If it isn't logged, only update Vehicle properties with scraped data
        print("not auth")

    return Response(vehicle_data)
