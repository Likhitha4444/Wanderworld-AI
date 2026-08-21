import json
import os

from django.core.management.base import BaseCommand
from apps.destinations.models import Destination
from apps.attractions.models import Attraction
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Seeds attraction data for destinations from JSON'

    def handle(self, *args, **options):

        data_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'data',
            'attractions.json'
        )

        with open(data_path, 'r', encoding='utf-8') as f:
            attractions_data = json.load(f)

        for dest_name, attractions in attractions_data.items():

            destination = Destination.objects.filter(name=dest_name).first()

            if not destination:
                self.stdout.write(
                    self.style.WARNING(
                        f'Destination {dest_name} not found, skipping.'
                    )
                )
                continue

            # Remove old/dummy attractions for this destination
            attractions_to_delete = Attraction.objects.filter(
            destination=destination
           )

            deleted_count = attractions_to_delete.count()

            Attraction.objects.filter(
                destination=destination
            ).delete()

            self.stdout.write(
                f'Removed {deleted_count} old attractions from {dest_name}'
            )

            # Add correct attractions
            for attr in attractions:

                Attraction.objects.create(
                    destination=destination,
                    name=attr['name'],
                    slug=slugify(attr['name']),
                    category=attr['category'],
                    short_description=attr['short_description'],
                    description=attr['description'],
                    latitude=attr['latitude'],
                    longitude=attr['longitude'],
                    entry_fee=attr['entry_fee'],
                    image_url=attr['image_url'],
                    estimated_duration=attr['estimated_duration'],
                    status='PUBLISHED',
                    city=destination.city,
                    country=destination.country,
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Added {len(attractions)} correct attractions for {dest_name}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded all attractions.')
        )