from rest_framework import serializers
from apps.wishlist.models import Wishlist
from apps.destinations.serializers import DestinationPublicSerializer
from apps.hotels.serializers import HotelPublicSerializer
from apps.attractions.serializers import AttractionPublicSerializer
from django.core.exceptions import ValidationError as DjangoValidationError

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'destination', 'hotel', 'attraction', 'created_at']
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.destination:
            rep['destination_detail'] = DestinationPublicSerializer(instance.destination).data
        if instance.hotel:
            rep['hotel_detail'] = HotelPublicSerializer(instance.hotel).data
        if instance.attraction:
            rep['attraction_detail'] = AttractionPublicSerializer(instance.attraction).data
        return rep

    def validate(self, data):
        targets = [data.get('destination'), data.get('hotel'), data.get('attraction')]
        if sum(t is not None for t in targets) != 1:
            raise serializers.ValidationError("Exactly one of destination, hotel, or attraction must be set.")
        
        # Public visibility check
        if data.get('destination') and data['destination'].status != 'PUBLISHED':
            raise serializers.ValidationError("Cannot wishlist a draft or archived destination.")
        if data.get('hotel') and data['hotel'].status != 'PUBLISHED':
            raise serializers.ValidationError("Cannot wishlist a draft or archived hotel.")
        if data.get('attraction') and data['attraction'].status != 'PUBLISHED':
            raise serializers.ValidationError("Cannot wishlist a draft or archived attraction.")
            
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        try:
            return Wishlist.objects.create(**validated_data)
        except Exception:
            raise serializers.ValidationError("Wishlist entry already exists.")
