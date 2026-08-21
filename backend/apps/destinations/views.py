from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.destinations.models import Destination
from apps.destinations.serializers import DestinationPublicSerializer, DestinationAdminSerializer
from apps.destinations.serializers_detail import DestinationDetailSerializer
from apps.accounts.views import IsAdmin
from django.db.models import Prefetch
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction

from apps.destinations.filters import DestinationFilter

class DestinationPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DestinationPublicSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'city', 'region', 'country', 'short_description']
    filterset_class = DestinationFilter
    ordering_fields = ['name', 'average_budget', 'created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        return Destination.objects.filter(status='PUBLISHED')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DestinationDetailSerializer
        return self.serializer_class

    def get_object(self):
        queryset = self.get_queryset().prefetch_related(
            Prefetch('hotels', queryset=Hotel.objects.filter(status='PUBLISHED')),
            Prefetch('attractions', queryset=Attraction.objects.filter(status='PUBLISHED'))
        )
        return super().get_object()

class DestinationAdminViewSet(viewsets.ModelViewSet):
    serializer_class = DestinationAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Destination.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'city', 'region', 'country']
    filterset_fields = ['status', 'is_featured', 'country']
    ordering_fields = ['name', 'average_budget', 'status', 'created_at']
