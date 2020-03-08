from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from rest_framework import status
from rest_framework.test import APIClient

from api.enum import VehicleType
from api.models import Driver, Location
from api.serializers import DriverSerializer, LocationSerializer

DRIVER_URL = reverse('drivers-list')
NOT_LOADED_DRIVER_URL = reverse('not-loaded-drivers-list')
OWN_VEHICLE_DRIVER_URL = reverse('own-vehicle-drivers-list')
LOCATION_URL = reverse('locations-list')
ORIGINS_AND_DESTINYS_URL = reverse('origin-and-destiny-list')


class DriversTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.default_date = datetime(year=1996, month=6, day=26).date()

    def test_driver_register(self):
        location1, location2 = baker.make(Location, 2)
        payload = {
            'name': 'Joãozinho Truckpad',
            'gender': 'MALE',
            'birth_date': self.default_date,
            'cnh_type': 'D',
            'is_loaded': False,
            'vehicle_type': 5,
            'origin': location1.id,
            'destiny': location2.id
        }
        response = self.client.post(DRIVER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

    def test_updating_driver_info(self):
        driver = baker.make(Driver, name='Chiquinho')
        patch_url = reverse('drivers-detail', args=[driver.id])

        response = self.client.patch(patch_url, {'name': 'Joãozinho'})

        driver = Driver.objects.get(id=driver.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(driver.name, 'Joãozinho')

    def test_listing_all_drivers(self):
        drivers = baker.make(Driver, _quantity=2)
        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for driver in drivers:
            self.assertIn(DriverSerializer(driver).data, response.data)

    def test_listing_all_non_loaded_drivers(self):
        driver1 = baker.make(Driver, is_loaded=True)
        driver2 = baker.make(Driver, is_loaded=False)

        response = self.client.get(NOT_LOADED_DRIVER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(DriverSerializer(driver1).data, response.data)
        self.assertIn(DriverSerializer(driver2).data, response.data)

    def test_listing_all_drivers_with_own_vehicles(self):
        driver1 = baker.make(Driver, owns_vehicle=True)
        driver2 = baker.make(Driver, owns_vehicle=False)

        response = self.client.get(OWN_VEHICLE_DRIVER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(DriverSerializer(driver1).data, response.data)
        self.assertNotIn(DriverSerializer(driver2).data, response.data)


class LocationsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_location_register(self):
        payload = {
            'name': 'Truckpad',
            'latitude': 123.1234,
            'longitude': -15.1234
        }
        response = self.client.post(LOCATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

    def test_location_geo_coordinates_are_unique(self):
        payload = {
            'name': 'Truckpad',
            'latitude': 123.1234,
            'longitude': -15.1234
        }

        response1 = self.client.post(LOCATION_URL, payload)
        response2 = self.client.post(LOCATION_URL, payload)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 1)

    def test_endpoint_listing_origin_and_destiny(self):
        loc1, loc2, loc3 = baker.make(Location, 3)
        baker.make(Driver, origin=loc1, destiny=loc2,
                   vehicle_type=VehicleType.CAMINHAO_TOCO.value)
        baker.make(Driver, origin=loc1, destiny=loc3,
                   vehicle_type=VehicleType.CAMINHAO_TRUCK.value)
        baker.make(Driver, origin=loc3, destiny=loc2,
                   vehicle_type=VehicleType.CARRETA_SIMPLES.value)

        response = self.client.get(ORIGINS_AND_DESTINYS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for vehicle_type in VehicleType:
            self.assertIn(vehicle_type.name, response.data)

        self.assertIn(
            LocationSerializer(loc1).data,
            response.data[VehicleType.CAMINHAO_TOCO.name]
        )
        self.assertIn(
            LocationSerializer(loc1).data,
            response.data[VehicleType.CAMINHAO_TRUCK.name]
        )
        self.assertIn(
            LocationSerializer(loc3).data,
            response.data[VehicleType.CARRETA_SIMPLES.name]
        )
