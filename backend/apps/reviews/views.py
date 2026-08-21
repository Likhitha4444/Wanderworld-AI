from rest_framework import viewsets, permissions, filters
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from apps.accounts.views import IsAdmin

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rating', 'created_at']

    def get_queryset(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return Review.objects.filter(user=self.request.user)
        # Note: listing should be public. 
        # But this viewset is currently protected by permissions.IsAuthenticated. 
        # Instructions say "public review listing", so I need a public viewset.
        return Review.objects.filter(status='PUBLISHED')

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class ReviewAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Review.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'rating']

class ReviewPublicListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rating', 'created_at']

    def get_queryset(self):
        hotel_slug = self.kwargs.get('hotel_slug')
        attraction_slug = self.kwargs.get('attraction_slug')
        
        # Base queryset: Published reviews
        queryset = Review.objects.filter(status='PUBLISHED')
        
        # If user is authenticated, add their own PENDING reviews
        if self.request.user.is_authenticated:
            queryset = queryset | Review.objects.filter(user=self.request.user, status='PENDING')
        
        # Apply filtering
        if hotel_slug:
            return queryset.filter(hotel__slug=hotel_slug)
        if attraction_slug:
            return queryset.filter(attraction__slug=attraction_slug)
        
        return queryset
