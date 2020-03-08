from datetime import datetime, time, timedelta

from django.utils import timezone

from rest_framework import views, viewsets, mixins, status
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


class DriversCounterView(views.APIView):
    def get(self, request, period):
        acceptable_periods = {'day': 0, 'week': 7, 'month': 30}
        if period not in acceptable_periods:
            return Response(
                data={'error': f'Period must be one of {acceptable_periods}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        today_start = datetime.combine(
            timezone.now().date(), time(), tzinfo=timezone.utc
        )
        period_start = today_start - timedelta(days=acceptable_periods[period])

        total = Driver.objects.filter(created_at__gte=period_start).count()

        return Response(data={
            'drivers_counter': total, 'period': period
        })
