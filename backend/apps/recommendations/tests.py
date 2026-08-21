from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User
from apps.recommendations.services import get_recommendations

class RecommendationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='Password123!')
        self.rec_url = reverse('recommendation-list')

    def test_get_recommendations(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.rec_url, {'type': 'attraction'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
