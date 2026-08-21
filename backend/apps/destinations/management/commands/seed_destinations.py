from django.core.management.base import BaseCommand
from apps.destinations.models import Destination
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with real destinations, hotels, and attractions'

    def handle(self, *args, **kwargs):
        # Existing destination seeding logic...
        dest_data = {"name": "Goa", "country": "India", "city": "Goa", "latitude": 15.2993, "longitude": 74.1240, "description": "Sun-kissed beaches, vibrant nightlife, and Portuguese heritage.", "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80"}
        
        slug = slugify(dest_data['name'])
        destination, created = Destination.objects.get_or_create(
            slug=slug,
            defaults={
                "name": dest_data['name'],
                "country": dest_data['country'],
                "city": dest_data['city'],
                "latitude": dest_data['latitude'],
                "longitude": dest_data['longitude'],
                "description": dest_data['description'],
                "short_description": dest_data['description'][:100],
                "average_budget": 1000.00,
                "status": "PUBLISHED",
                "is_featured": True,
                "cover_image_url": dest_data['image']
            }
        )

        # Seed Hotels for Goa
        hotels = [
            {"name": "Taj Exotica Resort & Spa", "address": "Benaulim, Goa", "latitude": 15.259, "longitude": 73.935, "star_rating": 5, "price_per_night": 15000},
            {"name": "W Goa", "address": "Vagator, Goa", "latitude": 15.601, "longitude": 73.738, "star_rating": 5, "price_per_night": 20000},
        ]
        for h in hotels:
            Hotel.objects.get_or_create(
                slug=slugify(h['name']),
                defaults={
                    "destination": destination,
                    "name": h['name'],
                    "description": f"Luxury stay in {h['address']}",
                    "short_description": "Luxury stay",
                    "address": h['address'],
                    "city": "Goa",
                    "country": "India",
                    "latitude": h['latitude'],
                    "longitude": h['longitude'],
                    "star_rating": h['star_rating'],
                    "price_per_night": h['price_per_night'],
                    "status": "PUBLISHED"
                }
            )

        # Seed Attractions for Goa
        attractions = [
            {"name": "Baga Beach", "category": "BEACH", "latitude": 15.555, "longitude": 73.751},
            {"name": "Basilica of Bom Jesus", "category": "HISTORICAL", "latitude": 15.500, "longitude": 73.911},
        ]
        for a in attractions:
            Attraction.objects.get_or_create(
                slug=slugify(a['name']),
                defaults={
                    "destination": destination,
                    "name": a['name'],
                    "short_description": "Popular attraction",
                    "description": f"Visit {a['name']}",
                    "category": a['category'],
                    "city": "Goa",
                    "country": "India",
                    "latitude": a['latitude'],
                    "longitude": a['longitude'],
                    "entry_fee": 0,
                    "estimated_duration": 120,
                    "status": "PUBLISHED"
                }
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded Goa with hotels and attractions.'))
