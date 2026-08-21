from rest_framework import viewsets, permissions, filters, decorators
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.attractions.models import Attraction
from apps.attractions.serializers import AttractionPublicSerializer, AttractionAdminSerializer
from apps.accounts.views import IsAdmin
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Sin, Radians
from django.core.exceptions import ValidationError

class AttractionPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttractionPublicSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description', 'city', 'country', 'category', 'short_description']
    filterset_fields = ['destination', 'category', 'city', 'country', 'is_featured']
    ordering_fields = ['name', 'entry_fee', 'average_rating', 'popularity_score', 'estimated_duration', 'created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Attraction.objects.filter(status='PUBLISHED')
        destination_slug = self.kwargs.get('destination_slug')
        if destination_slug:
            queryset = queryset.filter(destination__slug=destination_slug)
        return queryset

    @decorators.action(detail=False, methods=['get'])
    def nearby(self, request):
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        radius = request.query_params.get('radius_km', 10)
        
        if not lat or not lon:
            return Response({"error": "Latitude and longitude are required."}, status=400)
            
        try:
            lat = float(lat)
            lon = float(lon)
            radius = float(radius)
        except ValueError:
            return Response({"error": "Invalid coordinates or radius."}, status=400)

        # Haversine distance formula: d = 6371 * acos(cos(radians(lat)) * cos(radians(lat_i)) * cos(radians(lon_i) - radians(lon)) + sin(radians(lat)) * sin(radians(lat_i)))
        # Simplified for Django ORM
        queryset = self.get_queryset().annotate(
            distance=ExpressionWrapper(
                6371 * ACos(
                    Cos(Radians(lat)) * Cos(Radians(F('latitude'))) * Cos(Radians(F('longitude')) - Radians(lon)) +
                    Sin(Radians(lat)) * Sin(Radians(F('latitude')))
                ),
                output_field=FloatField()
            )
        ).filter(distance__lte=radius).order_by('distance')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AttractionAdminViewSet(viewsets.ModelViewSet):
    serializer_class = AttractionAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Attraction.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'city', 'country', 'category']
    filterset_fields = ['status', 'is_featured', 'destination', 'category']
    ordering_fields = ['name', 'entry_fee', 'status', 'created_at']
