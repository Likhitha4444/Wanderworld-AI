from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.reviews.models import Review
from apps.hotels.models import Hotel
from apps.destinations.models import Destination
from apps.accounts.models import User

class ReviewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email='admin@example.com', password='Password123!', role='ADMIN')
        self.user = User.objects.create_user(email='user@example.com', password='Password123!', role='USER')
        self.destination = Destination.objects.create(
            name='Mysore', slug='mysore', country='India', city='Mysore', 
            description='City of palaces.', short_description='Palace city.', 
            latitude=12.305, longitude=76.655, average_budget=500.00, status='PUBLISHED'
        )
        self.hotel = Hotel.objects.create(
            destination=self.destination, name='Radisson Blu Mysore', slug='radisson-blu-mysore',
            description='Luxury.', short_description='Luxury.', address='MG Road',
            city='Mysore', country='India', latitude=12.31, longitude=76.66,
            star_rating=5, price_per_night=100.00, status='PUBLISHED'
        )
        self.review_list_url = reverse('review-list')

    def test_create_review(self):
        self.client.force_authenticate(user=self.user)
        data = {'hotel': self.hotel.id, 'rating': 5, 'comment': 'Great!'}
        response = self.client.post(self.review_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().status, 'PENDING')
