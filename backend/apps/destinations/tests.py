from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.destinations.models import Destination
from apps.accounts.models import User

class DestinationTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email='admin@example.com', password='Password123!', role='ADMIN')
        self.user = User.objects.create_user(email='user@example.com', password='Password123!', role='USER')
        
        self.dest_data = {
            'name': 'Mysore Palace',
            'slug': 'mysore-palace',
            'country': 'India',
            'city': 'Mysore',
            'description': 'A beautiful palace.',
            'short_description': 'Beautiful palace.',
            'latitude': 12.305,
            'longitude': 76.655,
            'average_budget': 500.00,
            'status': 'PUBLISHED'
        }
        self.public_list_url = reverse('destination-public-list')
        self.admin_list_url = reverse('destination-admin-list')

    def test_admin_can_create(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.admin_list_url, self.dest_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Destination.objects.count(), 1)

    def test_user_cannot_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.admin_list_url, self.dest_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_can_list_published(self):
        Destination.objects.create(**self.dest_data)
        response = self.client.get(self.public_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_public_cannot_list_draft(self):
        data = self.dest_data.copy()
        data['slug'] = 'draft-dest'
        data['status'] = 'DRAFT'
        Destination.objects.create(**data)
        response = self.client.get(self.public_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
