from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from api.models import Driver

DRIVER_ENDPOINT = reverse('drivers-list')


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
        response = self.client.post(DRIVER_ENDPOINT, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)
