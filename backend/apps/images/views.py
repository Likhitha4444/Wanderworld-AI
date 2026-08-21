from rest_framework import viewsets, permissions, filters
from apps.images.models import DestinationImage, HotelImage, AttractionImage
from apps.images.serializers import DestinationImageSerializer, HotelImageSerializer, AttractionImageSerializer
from apps.accounts.views import IsAdmin

class BaseImageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['display_order', 'created_at']

class DestinationImageViewSet(BaseImageViewSet):
    serializer_class = DestinationImageSerializer
    def get_queryset(self):
        return DestinationImage.objects.filter(destination_id=self.kwargs.get('destination_pk'))
    def perform_create(self, serializer):
        serializer.save(destination_id=self.kwargs.get('destination_pk'))

class HotelImageViewSet(BaseImageViewSet):
    serializer_class = HotelImageSerializer
    def get_queryset(self):
        return HotelImage.objects.filter(hotel_id=self.kwargs.get('hotel_pk'))
    def perform_create(self, serializer):
        serializer.save(hotel_id=self.kwargs.get('hotel_pk'))

class AttractionImageViewSet(BaseImageViewSet):
    serializer_class = AttractionImageSerializer
    def get_queryset(self):
        return AttractionImage.objects.filter(attraction_id=self.kwargs.get('attraction_pk'))
    def perform_create(self, serializer):
        serializer.save(attraction_id=self.kwargs.get('attraction_pk'))
