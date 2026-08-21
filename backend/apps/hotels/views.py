from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.hotels.models import Hotel, Room
from apps.hotels.serializers import HotelPublicSerializer, HotelAdminSerializer, RoomPublicSerializer, RoomAdminSerializer
from apps.accounts.views import IsAdmin
from django.shortcuts import get_object_or_404

class HotelPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelPublicSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description', 'city', 'country']
    filterset_fields = ['destination', 'city', 'country', 'star_rating', 'is_featured']
    ordering_fields = ['name', 'price_per_night', 'star_rating', 'average_rating']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Hotel.objects.filter(status='PUBLISHED')
        destination_slug = self.kwargs.get('destination_slug')
        if destination_slug:
            queryset = queryset.filter(destination__slug=destination_slug)
        return queryset

class HotelAdminViewSet(viewsets.ModelViewSet):
    serializer_class = HotelAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Hotel.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'city', 'country']
    filterset_fields = ['status', 'is_featured', 'destination']
    ordering_fields = ['name', 'price_per_night', 'status', 'created_at']

class RoomPublicViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RoomPublicSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['room_type', 'capacity']
    ordering_fields = ['price_per_night', 'capacity']

    def get_queryset(self):
        hotel_slug = self.kwargs.get('hotel_slug')
        return Room.objects.filter(hotel__slug=hotel_slug, status='ACTIVE', hotel__status='PUBLISHED')

class RoomAdminViewSet(viewsets.ModelViewSet):
    serializer_class = RoomAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    
    def get_queryset(self):
        return Room.objects.filter(hotel_id=self.kwargs.get('hotel_pk'))
