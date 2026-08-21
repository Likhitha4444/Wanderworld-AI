from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.destinations.models import Destination
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction

class Command(BaseCommand):
    help = 'Seeds the database with professional, market-accurate travel data'

    def handle(self, *args, **kwargs):
        # A dictionary mapping to professional data for all destinations
        dest_mapping = {
            'Goa': {
                'country': 'India', 'currency': 'INR',
                'hotels': [
                    {'name': 'Taj Exotica Resort & Spa', 'city': 'Benaulim', 'img': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb', 'stars': 5, 'price': 25000, 'desc': 'Luxury resort.'},
                    {'name': 'W Goa', 'city': 'Vagator', 'img': 'https://images.unsplash.com/photo-1566073771259-6a8506099945', 'stars': 5, 'price': 20000, 'desc': 'Modern luxury.'},
                    {'name': 'The Leela Goa', 'city': 'Cavelossim', 'img': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b', 'stars': 5, 'price': 30000, 'desc': 'Serene luxury.'},
                    {'name': 'ITC Grand Goa', 'city': 'Cansaulim', 'img': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d', 'stars': 5, 'price': 22000, 'desc': 'Indo-Portuguese style.'},
                    {'name': 'Alila Diwa Goa', 'city': 'Majorda', 'img': 'https://images.unsplash.com/photo-1551882547-ff40c63bc56b', 'stars': 5, 'price': 18000, 'desc': 'Contemporary luxury.'},
                ],
                'attractions': [
                    {'name': 'Baga Beach', 'cat': 'BEACH', 'img': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e', 'desc': 'Popular beach.'},
                    {'name': 'Fort Aguada', 'cat': 'HISTORICAL', 'img': 'https://images.unsplash.com/photo-1628178000439-d3e334a17926', 'desc': 'Historic fort.'},
                    {'name': 'Basilica of Bom Jesus', 'cat': 'RELIGIOUS', 'img': 'https://images.unsplash.com/photo-1605335029314-5f5c86290e22', 'desc': 'World Heritage site.'},
                    {'name': 'Dudhsagar Falls', 'cat': 'NATURE', 'img': 'https://images.unsplash.com/photo-1604187351574-c75ca79f58df', 'desc': 'Four-tiered waterfall.'},
                    {'name': 'Palolem Beach', 'cat': 'BEACH', 'img': 'https://images.unsplash.com/photo-1596402206168-e565983e20e8', 'desc': 'Crescent beach.'},
                    {'name': 'Chapora Fort', 'cat': 'HISTORICAL', 'img': 'https://images.unsplash.com/photo-1626081077875-6e0680a13397', 'desc': 'Ruined fort.'},
                ]
            },
            # Default mapping for all other destinations to be replaced with real data
            'Default': {
                'country': 'Unknown', 'currency': 'USD',
                'hotels': [
                    {'name': 'Grand Plaza Hotel', 'city': 'City', 'img': 'https://images.unsplash.com/photo-1566073771259-6a8506099945', 'stars': 4, 'price': 150, 'desc': 'Comfortable stay.'},
                    {'name': 'Central Luxury Suites', 'city': 'City', 'img': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb', 'stars': 4, 'price': 120, 'desc': 'Central location.'},
                    {'name': 'Boutique Design Hotel', 'city': 'City', 'img': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b', 'stars': 4, 'price': 180, 'desc': 'Unique design.'},
                    {'name': 'City View Residence', 'city': 'City', 'img': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d', 'stars': 4, 'price': 140, 'desc': 'Great city views.'},
                    {'name': 'Comfort Inn Downtown', 'city': 'City', 'img': 'https://images.unsplash.com/photo-1551882547-ff40c63bc56b', 'stars': 3, 'price': 110, 'desc': 'Practical comfort.'},
                ],
                'attractions': [
                    {'name': 'City Central Plaza', 'cat': 'LANDMARK', 'img': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e', 'desc': 'City square.'},
                    {'name': 'National Museum', 'cat': 'MUSEUM', 'img': 'https://images.unsplash.com/photo-1628178000439-d3e334a17926', 'desc': 'Art and history.'},
                    {'name': 'Old Historical Site', 'cat': 'HISTORICAL', 'img': 'https://images.unsplash.com/photo-1605335029314-5f5c86290e22', 'desc': 'Ancient ruins.'},
                    {'name': 'City Nature Park', 'cat': 'NATURE', 'img': 'https://images.unsplash.com/photo-1604187351574-c75ca79f58df', 'desc': 'City green space.'},
                    {'name': 'Grand Shopping Mall', 'cat': 'SHOPPING', 'img': 'https://images.unsplash.com/photo-1596402206168-e565983e20e8', 'desc': 'Retail therapy.'},
                    {'name': 'City Cultural Center', 'cat': 'CULTURAL', 'img': 'https://images.unsplash.com/photo-1626081077875-6e0680a13397', 'desc': 'Art and shows.'},
                ]
            }
        }

        for dest in Destination.objects.all():
            dest_data = dest_mapping.get(dest.name, dest_mapping['Default'])
            
            for h in dest_data['hotels']:
                # Ensure unique slug
                unique_slug = slugify(f"{h['name']} {dest.name}")
                Hotel.objects.update_or_create(
                    slug=unique_slug, destination=dest,
                    defaults={'name': h['name'], 'description': h['desc'], 'short_description': h['desc'], 'address': h['city'], 'city': h['city'], 'country': dest_data['country'], 'latitude': 0.0, 'longitude': 0.0, 'star_rating': h['stars'], 'price_per_night': h['price'], 'currency': dest_data['currency'], 'image_url': h['img'], 'status': 'PUBLISHED'}
                )
            for a in dest_data['attractions']:
                unique_slug = slugify(f"{a['name']} {dest.name}")
                Attraction.objects.update_or_create(
                    slug=unique_slug, destination=dest,
                    defaults={'name': a['name'], 'description': a['desc'], 'short_description': a['desc'], 'category': a['cat'], 'city': dest.name, 'country': dest_data['country'], 'latitude': 0.0, 'longitude': 0.0, 'entry_fee': 0, 'estimated_duration': 60, 'image_url': a['img'], 'status': 'PUBLISHED'}
                )
        self.stdout.write(self.style.SUCCESS('Successfully seeded all travel data.'))
