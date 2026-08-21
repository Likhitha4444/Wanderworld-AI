from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.hotels.models import Hotel, Room
from apps.destinations.models import Destination
from apps.accounts.models import User

class HotelAndRoomTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email='admin@example.com', password='Password123!', role='ADMIN')
        self.user = User.objects.create_user(email='user@example.com', password='Password123!', role='USER')
        self.destination = Destination.objects.create(
            name='Mysore', slug='mysore', country='India', city='Mysore', 
            description='City of palaces.', short_description='Palace city.', 
            latitude=12.305, longitude=76.655, average_budget=500.00, status='PUBLISHED'
        )
        
        self.hotel_data = {
            'destination': self.destination.id,
            'name': 'Radisson Blu Mysore',
            'slug': 'radisson-blu-mysore',
            'description': 'Luxury hotel.',
            'short_description': 'Luxury.',
            'address': 'MG Road',
            'city': 'Mysore',
            'country': 'India',
            'latitude': 12.31,
            'longitude': 76.66,
            'star_rating': 5,
            'price_per_night': 100.00,
            'status': 'PUBLISHED'
        }
        
        self.admin_hotel_list_url = reverse('hotel-admin-list')
        self.public_hotel_list_url = reverse('hotel-public-list')

    def test_admin_can_create_hotel(self):
        self.client.force_authenticate(user=self.admin)
        data = self.hotel_data.copy()
        data['destination'] = self.destination.id
        response = self.client.post(self.admin_hotel_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hotel.objects.count(), 1)

    def test_user_cannot_create_hotel(self):
        self.client.force_authenticate(user=self.user)
        data = self.hotel_data.copy()
        data['destination'] = self.destination.id
        response = self.client.post(self.admin_hotel_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_can_list_published_hotel(self):
        data = self.hotel_data.copy()
        data['destination'] = self.destination
        Hotel.objects.create(**data)
        response = self.client.get(self.public_hotel_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
