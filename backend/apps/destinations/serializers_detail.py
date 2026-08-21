from rest_framework import serializers
from apps.destinations.serializers import DestinationPublicSerializer
from apps.hotels.serializers import HotelPublicSerializer
from apps.attractions.serializers import AttractionPublicSerializer
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction

class DestinationDetailSerializer(DestinationPublicSerializer):
    hotels = HotelPublicSerializer(many=True, read_only=True)
    attractions = AttractionPublicSerializer(many=True, read_only=True)

    class Meta(DestinationPublicSerializer.Meta):
        fields = DestinationPublicSerializer.Meta.fields + ['hotels', 'attractions']
