from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.wishlist.models import Wishlist
from apps.wishlist.serializers import WishlistSerializer
from django.db.models import Q

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def check(self, request):
        destination_id = request.query_params.get('destination_id')
        hotel_id = request.query_params.get('hotel_id')
        attraction_id = request.query_params.get('attraction_id')
        
        query = Q(user=request.user)
        if destination_id: query &= Q(destination_id=destination_id)
        elif hotel_id: query &= Q(hotel_id=hotel_id)
        elif attraction_id: query &= Q(attraction_id=attraction_id)
        else: return Response({"error": "Exactly one ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        exists = Wishlist.objects.filter(query).exists()
        return Response({"wishlisted": exists})
