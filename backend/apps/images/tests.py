from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.images.models import DestinationImage
from apps.destinations.models import Destination
from apps.accounts.models import User
from PIL import Image
import io

class ImageTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email='admin@example.com', password='Password123!', role='ADMIN')
        self.destination = Destination.objects.create(
            name='Mysore', slug='mysore', country='India', city='Mysore', 
            description='City of palaces.', short_description='Palace city.', 
            latitude=12.305, longitude=76.655, average_budget=500.00, status='PUBLISHED'
        )
        self.admin_url = reverse('destination-image-list', kwargs={'destination_pk': self.destination.id})

    def test_admin_can_upload_image(self):
        self.client.force_authenticate(user=self.admin)
        
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'jpeg')
        file.name = 'test.jpg'
        file.seek(0)
        
        data = {
            'image': file,
            'alt_text': 'Test Image',
            'is_primary': 'true'
        }
        response = self.client.post(self.admin_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(DestinationImage.objects.count(), 1)
