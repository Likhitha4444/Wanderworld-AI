from rest_framework import serializers
from apps.reviews.models import Review
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction
from django.utils.translation import gettext_lazy as _

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.first_name')
    
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'hotel', 'attraction', 'rating', 'title', 'comment', 'status', 'created_at']
        read_only_fields = ['id', 'user_name', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        targets = [data.get('hotel'), data.get('attraction')]
        if sum(t is not None for t in targets) != 1:
            raise serializers.ValidationError(_("Exactly one of hotel or attraction must be set."))
        
        target = data.get('hotel') or data.get('attraction')
        if target.status != 'PUBLISHED':
            raise serializers.ValidationError(_("Cannot review a draft or archived entity."))
            
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Review.objects.create(
            user=user,
            status='PUBLISHED',
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.status = 'PUBLISHED'
        # Update other fields from validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
