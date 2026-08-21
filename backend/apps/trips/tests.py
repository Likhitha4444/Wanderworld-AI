from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.trips.models import Trip, TripDay, TripActivity, TripRevision
from apps.destinations.models import Destination
from decimal import Decimal
from apps.trips.services import calculate_trip_budget

User = get_user_model()

class TripTests(APITestCase):
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
            average_budget=100.00
        )
        self.trip = Trip.objects.create(
            user=self.user,
            title='My Paris Trip',
            destination=self.destination,
            start_date='2026-09-01',
            end_date='2026-09-03',
            budget=Decimal('1000.00')
        )
        self.day = TripDay.objects.create(trip=self.trip, day_number=1, date='2026-09-01')

    def test_calculate_trip_budget(self):
        TripActivity.objects.create(
            trip_day=self.day, 
            activity_type='ATTRACTION',
            title='Museum',
            start_time='10:00',
            end_time='12:00',
            duration_minutes=120,
            estimated_cost=Decimal('200.00'),
            sequence=1
        )
        TripActivity.objects.create(
            trip_day=self.day, 
            activity_type='MEAL',
            title='Lunch',
            start_time='13:00',
            end_time='14:00',
            duration_minutes=60,
            estimated_cost=Decimal('300.00'),
            sequence=2
        )
        
        budget_summary = calculate_trip_budget(self.trip)
        self.assertEqual(budget_summary['estimated_cost'], Decimal('500.00'))
        self.assertEqual(budget_summary['remaining_budget'], Decimal('500.00'))
        self.assertEqual(budget_summary['budget_used_percentage'], 50.0)

    def test_revision_immutability(self):
        revision = TripRevision.objects.create(
            trip=self.trip,
            revision_number=1,
            itinerary_snapshot={'data': 'test'},
            created_by=self.user,
            change_reason='Initial'
        )
        # Attempt to modify
        revision.change_reason = 'New reason'
        with self.assertRaises(Exception):
            revision.save()
            
    def test_other_user_cannot_access_trip(self):
        other_user = User.objects.create_user(email='other@example.com', password='password')
        trip = Trip.objects.create(user=other_user, title='Other Trip', destination=self.destination, start_date='2026-09-01', end_date='2026-09-03')
        url = reverse('trip-detail', kwargs={'pk': trip.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
