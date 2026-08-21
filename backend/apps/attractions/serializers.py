from rest_framework import serializers
from apps.attractions.models import Attraction

class AttractionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = [
            'id', 'destination', 'name', 'slug', 'short_description', 'description', 
            'category', 'address', 'city', 'country', 'latitude', 'longitude', 
            'entry_fee', 'currency', 'estimated_duration', 'best_time_to_visit', 
            'opening_time', 'closing_time', 'average_rating', 'accessibility', 'is_featured', 'image_url'
        ]
        read_only_fields = ['id', 'average_rating', 'popularity_score']

class AttractionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
