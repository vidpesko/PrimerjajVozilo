from django.urls import path

from .views import update_model, VehicleList


urlpatterns = [
    # Vehicles list
    path("vehicles/", VehicleList.as_view()),
    # Scraper interface
    path("update-model/", update_model),
]
