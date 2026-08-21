from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.travel_dna.models import TravelDNACategory, UserTravelDNA, TravelBehaviorEvent
from apps.attractions.models import Attraction
from apps.destinations.models import Destination
from apps.accounts.models import User

class TravelBehaviorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='Password123!')
        self.destination = Destination.objects.create(
            name='Mysore', slug='mysore', country='India', city='Mysore', 
            description='City of palaces.', short_description='Palace city.', 
            latitude=12.305, longitude=76.655, average_budget=500.00, status='PUBLISHED'
        )
        self.attraction = Attraction.objects.create(
            destination=self.destination, name='Nature Park', slug='nature-park',
            short_description='Beautiful park.', description='A beautiful park.',
            category='NATURE', city='Mysore', country='India',
            latitude=12.31, longitude=76.66, entry_fee=50.00,
            estimated_duration=60, status='PUBLISHED'
        )
        self.event_url = reverse('behavior-event-list')

    def test_record_behavior_event(self):
        self.client.force_authenticate(user=self.user)
        data = {'event_type': 'ATTRACTION_VIEW', 'attraction': self.attraction.id}
        response = self.client.post(self.event_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TravelBehaviorEvent.objects.count(), 1)
        self.assertEqual(TravelBehaviorEvent.objects.first().user, self.user)
