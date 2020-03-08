from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from api.models import Driver, Location

DRIVER_URL = reverse('drivers-list')
LOCATION_URL = reverse('locations-list')


class DriversTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.default_date = datetime(year=1996, month=6, day=26).astimezone()

    def test_driver_register(self):
        payload = {
            'name': 'Joãozinho Truckpad',
            'gender': 'MALE',
            'birth_date': self.default_date,
            'cnh_type': 'D',
            'is_loaded': False,
            'vehicle_type': 5
        }
        response = self.client.post(DRIVER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)


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
