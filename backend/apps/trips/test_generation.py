from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.trips.models import Trip, TripStatus
from apps.destinations.models import Destination
from unittest.mock import patch, MagicMock
from decimal import Decimal

User = get_user_model()

class GenerationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.destination = Destination.objects.create(
            name='Paris', 
            slug='paris',
            country='France',
            city='Paris',
            description='City of Light',
            short_description='Romantic city',
            latitude=48.8566,
            longitude=2.3522,
            average_budget=100.00,
            status='PUBLISHED'
        )
        self.trip = Trip.objects.create(
            user=self.user,
            title='My Paris Trip',
            destination=self.destination,
            start_date='2026-09-01',
            end_date='2026-09-03',
            budget=Decimal('1000.00')
        )

    @patch('apps.trips.generation_service.GeminiService')
    def test_generate_itinerary_success(self, mock_ai_service):
        mock_ai_instance = mock_ai_service.return_value
        mock_ai_instance.generate.return_value = {
            'status': 'success',
            'data': {
                'days': [
                    {
                        'day_number': 1,
                        'date': '2026-09-01',
                        'activities': [
                            {
                                'activity_type': 'ATTRACTION',
                                'title': 'Museum',
                                'start_time': '10:00:00',
                                'end_time': '12:00:00',
                                'duration_minutes': 120,
                                'estimated_cost': '100.00',
                                'sequence': 1
                            }
                        ]
                    }
                ]
            }
        }
        
        url = reverse('trip-generate', kwargs={'pk': self.trip.id})
        response = self.client.post(url, {'preferences': {}}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.status, TripStatus.READY)
        self.assertEqual(self.trip.days.count(), 1)
