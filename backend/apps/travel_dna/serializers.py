from rest_framework import serializers
from apps.travel_dna.models import TravelDNACategory, UserTravelDNA, TravelBehaviorEvent

class TravelDNACategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelDNACategory
        fields = ['id', 'name', 'slug']

class UserTravelDNASerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = UserTravelDNA
        fields = ['category', 'score', 'confidence']

class TravelBehaviorEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelBehaviorEvent
        fields = ['id', 'event_type', 'destination', 'hotel', 'attraction', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        # Validate target
        target_count = sum(data.get(field) is not None for field in ['destination', 'hotel', 'attraction'])
        event_type = data.get('event_type')

        if event_type in ['DESTINATION_VIEW', 'HOTEL_VIEW', 'ATTRACTION_VIEW']:
            if target_count != 1:
                raise serializers.ValidationError("Entity event requires exactly one target entity.")
            
            target = data.get('destination') or data.get('hotel') or data.get('attraction')
            if target.status != 'PUBLISHED':
                raise serializers.ValidationError("Cannot record events for draft or archived entities.")
        
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return TravelBehaviorEvent.objects.create(**validated_data)
