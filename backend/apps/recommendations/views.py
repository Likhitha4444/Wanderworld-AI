from rest_framework import viewsets, permissions
from rest_framework.response import Response
from apps.recommendations.services import get_recommendations
from apps.recommendations.serializers import (
    DestinationRecommendationSerializer, 
    HotelRecommendationSerializer, 
    AttractionRecommendationSerializer
)

class RecommendationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        target_type = request.query_params.get('type', 'attraction')
        recommendations = get_recommendations(request.user, target_type)
        
        if target_type == 'destination':
            serializer = DestinationRecommendationSerializer(recommendations, many=True)
        elif target_type == 'hotel':
            serializer = HotelRecommendationSerializer(recommendations, many=True)
        else:
            serializer = AttractionRecommendationSerializer(recommendations, many=True)
            
        return Response(serializer.data)
