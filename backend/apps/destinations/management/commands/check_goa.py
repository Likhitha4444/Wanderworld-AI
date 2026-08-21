
from django.core.management.base import BaseCommand
from apps.destinations.models import Destination

class Command(BaseCommand):
    help = 'Check Goa data'

    def handle(self, *args, **kwargs):
        try:
            goa = Destination.objects.get(name='Goa')
            print(f"Destination: {goa.name}")
            print(f"Hotels count: {goa.hotels.count()}")
            for hotel in goa.hotels.all():
                print(f" - Hotel: {hotel.name}")
            print(f"Attractions count: {goa.attractions.count()}")
            for attraction in goa.attractions.all():
                print(f" - Attraction: {attraction.name}")
        except Destination.DoesNotExist:
            print("Goa not found")
