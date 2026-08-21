import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.destinations.models import Destination
from apps.hotels.models import Hotel

dests_to_populate = ['Bangkok', 'Sydney', 'Prague', 'Venice']
for d_name in dests_to_populate:
    d = Destination.objects.get(name=d_name)
    existing = Hotel.objects.filter(destination=d)
    print(f'Destination: {d_name} | Existing: {existing.count()}')
    
    # Define hotels for each destination
    hotels = [
        {'name': f'Budget Stay in {d_name}', 'slug': f'budget-{d_name.lower().replace(" ","-")}', 'price': 50, 'star': 2},
        {'name': f'Mid-range Comfort in {d_name}', 'slug': f'mid-{d_name.lower().replace(" ","-")}', 'price': 150, 'star': 3},
        {'name': f'Luxury Resort in {d_name}', 'slug': f'lux-{d_name.lower().replace(" ","-")}', 'price': 400, 'star': 5}
    ]
    
    for h in hotels:
        if not existing.filter(name=h['name']).exists():
            Hotel.objects.create(
                destination=d,
                name=h['name'],
                slug=h['slug'],
                description='Beautiful property with great amenities and central location.',
                short_description='Great place to stay with modern facilities.',
                address='123 Main St',
                city=d_name,
                country='Country',
                latitude=0.0,
                longitude=0.0,
                star_rating=h['star'],
                price_per_night=h['price'],
                status='PUBLISHED',
                amenities=['Free WiFi', 'Air conditioning', 'Breakfast', 'Swimming pool']
            )
            print(f'  Created: {h["name"]}')
