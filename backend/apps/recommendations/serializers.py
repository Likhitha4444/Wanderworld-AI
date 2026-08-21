from rest_framework import serializers
from apps.destinations.serializers import DestinationPublicSerializer
from apps.hotels.serializers import HotelPublicSerializer
from apps.attractions.serializers import AttractionPublicSerializer

class RecommendationSerializer(serializers.Serializer):
    score = serializers.FloatField()
    reasons = serializers.ListField(child=serializers.CharField())
    personalized = serializers.BooleanField()

class DestinationRecommendationSerializer(RecommendationSerializer):
    destination = DestinationPublicSerializer(source='item')
    class Meta:
        fields = ['destination', 'score', 'reasons']

class HotelRecommendationSerializer(RecommendationSerializer):
    hotel = HotelPublicSerializer(source='item')
    class Meta:
        fields = ['hotel', 'score', 'reasons']

class AttractionRecommendationSerializer(RecommendationSerializer):
    attraction = AttractionPublicSerializer(source='item')
    class Meta:
        fields = ['attraction', 'score', 'reasons']
