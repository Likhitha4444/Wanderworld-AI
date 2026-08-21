from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from .models import Trip, TripDay, TripActivity, TripRevision
from .serializers import TripSerializer, TripDaySerializer, TripActivitySerializer, TripRevisionSerializer
from .generation_service import TripGenerationService

class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @decorators.action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        
        trip = self.get_object()
        preferences = request.data.get('preferences', {})
        service = TripGenerationService()
        try:
            service.generate_itinerary(request.user, trip.id, preferences)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Generation failed: {error_msg}\n{traceback.format_exc()}")
            return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

class TripDayViewSet(viewsets.ModelViewSet):
    serializer_class = TripDaySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TripDay.objects.filter(trip__user=self.request.user, trip_id=self.kwargs['trip_pk'])

class TripActivityViewSet(viewsets.ModelViewSet):
    serializer_class = TripActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TripActivity.objects.filter(trip_day__trip__user=self.request.user, trip_day__trip_id=self.kwargs['trip_pk'], trip_day_id=self.kwargs['day_pk'])

class TripRevisionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TripRevisionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TripRevision.objects.filter(trip__user=self.request.user, trip_id=self.kwargs['trip_pk'])
