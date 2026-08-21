from rest_framework import serializers
from apps.hotels.models import Hotel, Room

class RoomPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'description', 'capacity', 'bed_type', 'price_per_night', 'currency', 'amenities']

class HotelPublicSerializer(serializers.ModelSerializer):
    rooms = RoomPublicSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = [
            'id', 'destination', 'name', 'slug', 'description', 'short_description', 
            'address', 'city', 'country', 'latitude', 'longitude', 'star_rating', 
            'average_rating', 'price_per_night', 'currency', 'amenities', 'is_featured', 'rooms', 'image_url'
        ]
        read_only_fields = ['id', 'average_rating']

class RoomAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class HotelAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
