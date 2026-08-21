from rest_framework import serializers
from .models import Trip, TripDay, TripActivity, TripRevision
from apps.destinations.models import Destination
from apps.destinations.serializers import DestinationPublicSerializer

class TripActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripActivity
        fields = '__all__'

class TripDaySerializer(serializers.ModelSerializer):
    activities = TripActivitySerializer(many=True, read_only=True)
    class Meta:
        model = TripDay
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    days = TripDaySerializer(many=True, read_only=True)
    destination = serializers.PrimaryKeyRelatedField(queryset=Destination.objects.all())

    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('user', 'status', 'planning_source', 'created_at', 'updated_at')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.destination:
            rep['destination'] = DestinationPublicSerializer(instance.destination).data
        return rep

class TripRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRevision
        fields = '__all__'
        read_only_fields = ('trip', 'revision_number', 'itinerary_snapshot', 'created_by', 'created_at', 'change_reason')
