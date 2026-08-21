from rest_framework import serializers
from apps.destinations.models import Destination

class DestinationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'country', 'region', 'city', 
            'description', 'short_description', 'latitude', 'longitude',
            'cover_image_url', 'best_time_to_visit', 'average_budget', 'currency', 'is_featured'
        ]
        read_only_fields = ['id']

class DestinationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
