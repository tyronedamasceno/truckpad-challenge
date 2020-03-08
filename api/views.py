from rest_framework import viewsets, mixins

from api.models import Driver, Location
from api.serializers import DriverSerializer, LocationSerializer


class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class LocationViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class NotLoadedDriversViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.filter(is_loaded=False)


class OwnVehicleDriversViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.filter(owns_vehicle=True)
