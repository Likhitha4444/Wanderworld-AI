from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.attractions.models import Attraction
from apps.destinations.models import Destination
from apps.accounts.models import User

class AttractionTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email='admin@example.com', password='Password123!', role='ADMIN')
        self.user = User.objects.create_user(email='user@example.com', password='Password123!', role='USER')
        self.destination = Destination.objects.create(
            name='Mysore', slug='mysore', country='India', city='Mysore', 
            description='City of palaces.', short_description='Palace city.', 
            latitude=12.305, longitude=76.655, average_budget=500.00, status='PUBLISHED'
        )
        
        self.attraction_data = {
            'destination': self.destination.id,
            'name': 'Mysore Palace',
            'slug': 'mysore-palace',
            'short_description': 'Beautiful palace.',
            'description': 'A beautiful palace.',
            'category': 'HISTORICAL',
            'city': 'Mysore',
            'country': 'India',
            'latitude': 12.31,
            'longitude': 76.66,
            'entry_fee': 50.00,
            'estimated_duration': 60,
            'status': 'PUBLISHED'
        }
        
        self.admin_attraction_list_url = reverse('attraction-admin-list')
        self.public_attraction_list_url = reverse('attraction-public-list')

    def test_admin_can_create_attraction(self):
        self.client.force_authenticate(user=self.admin)
        data = self.attraction_data.copy()
        response = self.client.post(self.admin_attraction_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attraction.objects.count(), 1)

    def test_user_cannot_create_attraction(self):
        self.client.force_authenticate(user=self.user)
        data = self.attraction_data.copy()
        response = self.client.post(self.admin_attraction_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_can_list_published_attraction(self):
        data = self.attraction_data.copy()
        data['destination'] = self.destination
        Attraction.objects.create(**data)
        response = self.client.get(self.public_attraction_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
