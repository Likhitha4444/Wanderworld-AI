from django.test import TestCase
from decimal import Decimal
from apps.trips.models import Trip
from apps.destinations.models import Destination
from apps.trips.quality import evaluate_itinerary
from apps.trips.quality.rules import ERR_ACTIVITY_OVERLAP, ERR_BUDGET_EXCEEDED
from django.contrib.auth import get_user_model

User = get_user_model()

class QualityEngineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.destination = Destination.objects.create(
            name='Paris', slug='paris', country='France', city='Paris', description='...', short_description='...',
            latitude=0, longitude=0, average_budget=100.00, status='PUBLISHED'
        )
        self.trip = Trip.objects.create(
            user=self.user,
            title='Test Trip', destination=self.destination, start_date='2026-09-01', end_date='2026-09-01', budget=Decimal('100.00')
        )
        
    def test_evaluate_itinerary_overlap(self):
        itinerary = {
            'days': [{
                'day_number': 1,
                'date': '2026-09-01',
                'activities': [
                    {'title': 'Act1', 'start_time': '10:00:00', 'end_time': '12:00:00', 'estimated_cost': '10.00'},
                    {'title': 'Act2', 'start_time': '11:00:00', 'end_time': '13:00:00', 'estimated_cost': '10.00'}
                ]
            }]
        }
        result = evaluate_itinerary(self.trip, itinerary)
        self.assertEqual(result['status'], 'FAIL')
        self.assertTrue(any(e['code'] == ERR_ACTIVITY_OVERLAP for e in result['errors']))
        
    def test_evaluate_itinerary_budget_exceeded(self):
        itinerary = {
            'days': [{
                'day_number': 1,
                'date': '2026-09-01',
                'activities': [
                    {'title': 'Act1', 'start_time': '10:00:00', 'end_time': '12:00:00', 'estimated_cost': '200.00'}
                ]
            }]
        }
        result = evaluate_itinerary(self.trip, itinerary)
        self.assertEqual(result['status'], 'FAIL')
        self.assertTrue(any(e['code'] == ERR_BUDGET_EXCEEDED for e in result['errors']))
        
    def test_evaluate_itinerary_pass(self):
        itinerary = {
            'days': [{
                'day_number': 1,
                'date': '2026-09-01',
                'activities': [
                    {'title': 'Act1', 'start_time': '10:00:00', 'end_time': '11:00:00', 'estimated_cost': '50.00'}
                ]
            }]
        }
        result = evaluate_itinerary(self.trip, itinerary)
        self.assertEqual(result['status'], 'PASS')
