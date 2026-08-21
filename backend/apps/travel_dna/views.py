from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.travel_dna.models import UserTravelDNA
from apps.travel_dna.serializers import UserTravelDNASerializer
from apps.travel_dna.services import calculate_dna_score

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.travel_dna.models import UserTravelDNA, TravelBehaviorEvent
from apps.travel_dna.serializers import UserTravelDNASerializer, TravelBehaviorEventSerializer
from apps.travel_dna.services import calculate_dna_score

class TravelDNAViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserTravelDNASerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserTravelDNA.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def recalculate(self, request):
        calculate_dna_score(request.user)
        return Response({"message": "Travel DNA recalculated successfully."})

class BehaviorEventViewSet(viewsets.ModelViewSet):
    serializer_class = TravelBehaviorEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TravelBehaviorEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
