from django.urls import path

from .views import update_model, get_vehicle, VehicleList


urlpatterns = [
    # Vehicles list
    path("vehicles/", VehicleList.as_view()),
    # Scraper interface
    path("update-model/", update_model),  # Update vehicle model
    path("get-vehicle/", get_vehicle),  # Get (and update if needed) vehicle
]
