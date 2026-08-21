import json
import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.hotels.models import Hotel
from apps.destinations.models import Destination

# Known placeholder names identified in research
DUMMY_NAMES = [
    "Grand Plaza Hotel",
    "Central Luxury Suites",
    "Boutique Design Hotel",
    "City View Residence",
    "Comfort Inn Downtown",
    "Grand Shopping Hotel",
    "City Central Hotel",
    "City Nature Hotel",
    "Luxury Resort",
    "Downtown Hotel"
]

class Command(BaseCommand):
    help = 'Seeds real hotel data and reconciles dummy hotels.'

    def handle(self, *args, **options):
        data_path = os.path.join('apps', 'hotels', 'data', 'hotels.json')
        
        if not os.path.exists(data_path):
            self.stdout.write(self.style.ERROR(f'Data file not found at {data_path}'))
            return

        with open(data_path, 'r') as f:
            hotels_data = json.load(f)

        for dest_name, hotels in hotels_data.items():
            try:
                destination = Destination.objects.get(name=dest_name)
            except Destination.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Destination {dest_name} not found, skipping.'))
                continue

            self.stdout.write(self.style.SUCCESS(f'Processing {dest_name}...'))

            # Reconcile: remove only "dummy" hotels for this destination
            existing_hotels = Hotel.objects.filter(destination=destination)
            for hotel in existing_hotels:
                if hotel.name in DUMMY_NAMES:
                    hotel.delete()
                    self.stdout.write(f'  Deleted dummy hotel: {hotel.name}')

            # Create or update hotels
            for hotel_info in hotels:
                # Robust slug generation
                base_slug = slugify(f"{hotel_info['name']}-{hotel_info['city']}")
                slug = base_slug
                counter = 1
                # Ensure slug uniqueness for NEW hotels
                while Hotel.objects.filter(slug=slug).exclude(destination=destination, name=hotel_info['name']).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                hotel, created = Hotel.objects.update_or_create(
                    destination=destination,
                    name=hotel_info['name'],
                    defaults={
                        'slug': slug,
                        'description': hotel_info['description'],
                        'short_description': hotel_info['short_description'],
                        'address': hotel_info['address'],
                        'city': hotel_info['city'],
                        'country': hotel_info['country'],
                        'latitude': hotel_info['latitude'],
                        'longitude': hotel_info['longitude'],
                        'star_rating': hotel_info['star_rating'],
                        'price_per_night': hotel_info['price_per_night'],
                        'currency': hotel_info['currency'],
                        'image_url': hotel_info['image_url'],
                        'amenities': hotel_info['amenities'],
                        'status': 'PUBLISHED',
                        'is_featured': hotel_info.get('is_featured', False),
                    }
                )
                if created:
                    self.stdout.write(f'  Created: {hotel_info["name"]}')
                else:
                    self.stdout.write(f'  Updated: {hotel_info["name"]}')

        self.stdout.write(self.style.SUCCESS('Hotel seeding completed.'))
