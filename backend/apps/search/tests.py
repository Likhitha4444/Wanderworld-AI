from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.attractions.models import Attraction
from apps.destinations.models import Destination
from apps.accounts.models import User

class SearchAndDiscoveryTests(APITestCase):
    def setUp(self):
        self.destination = Destination.objects.create(
            name='Mysore', slug='mysore', country='India', city='Mysore', 
            description='City of palaces.', short_description='Palace city.', 
            latitude=12.305, longitude=76.655, average_budget=500.00, status='PUBLISHED'
        )
        self.attraction = Attraction.objects.create(
            destination=self.destination, name='Mysore Palace', slug='mysore-palace',
            short_description='Beautiful palace.', description='A beautiful palace.',
            category='HISTORICAL', city='Mysore', country='India',
            latitude=12.31, longitude=76.66, entry_fee=50.00,
            estimated_duration=60, status='PUBLISHED'
        )

    def test_global_search(self):
        url = reverse('global-search')
        response = self.client.get(url, {'q': 'mysore'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']['destinations']), 1)
        self.assertEqual(len(response.data['results']['attractions']), 1)

    def test_nearby_search(self):
        url = reverse('attraction-public-nearby')
        response = self.client.get(url, {'latitude': 12.31, 'longitude': 76.66, 'radius_km': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_destination_detail_aggregation(self):
        url = reverse('destination-public-detail', kwargs={'slug': 'mysore'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('attractions', response.data)
        self.assertEqual(len(response.data['attractions']), 1)
