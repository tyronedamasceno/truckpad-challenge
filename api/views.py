from rest_framework import viewsets, mixins
from rest_framework.response import Response

from api.enum import VehicleType
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


class OriginAndDestinyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def list(self, request, *args, **kwargs):
        truck_types_dict = {}
        for vehicle_type in VehicleType:
            truck_types_dict[vehicle_type.name] = set()

        for driver in Driver.objects.all():
            driver_truck_type_name = VehicleType(driver.vehicle_type).name
            truck_types_dict[driver_truck_type_name].add(driver.origin)
            truck_types_dict[driver_truck_type_name].add(driver.destiny)

        response_data = {
            truck_type: LocationSerializer(locations, many=True).data
            for truck_type, locations in truck_types_dict.items()
        }

        return Response(response_data)
