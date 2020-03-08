from rest_framework import viewsets

from api.models import Driver, Location
from api.serializers import DriverSerializer, LocationSerializer


class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
