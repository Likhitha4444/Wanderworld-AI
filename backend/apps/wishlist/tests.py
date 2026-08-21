from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.wishlist.models import Wishlist
from apps.destinations.models import Destination
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction
from apps.accounts.models import User

class WishlistTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='Password123!')
        self.destination = Destination.objects.create(
            name='Mysore', slug='mysore', country='India', city='Mysore', 
            description='City of palaces.', short_description='Palace city.', 
            latitude=12.305, longitude=76.655, average_budget=500.00, status='PUBLISHED'
        )
        self.list_url = reverse('wishlist-list')
        self.check_url = reverse('wishlist-check')

    def test_add_destination_to_wishlist(self):
        self.client.force_authenticate(user=self.user)
        data = {'destination': self.destination.id}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wishlist.objects.count(), 1)

    def test_duplicate_wishlist_entry(self):
        self.client.force_authenticate(user=self.user)
        data = {'destination': self.destination.id}
        self.client.post(self.list_url, data, format='json')
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
