from rest_framework.views import APIView
from rest_framework.response import Response
from apps.destinations.models import Destination
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction
from apps.destinations.serializers import DestinationPublicSerializer
from apps.hotels.serializers import HotelPublicSerializer
from apps.attractions.serializers import AttractionPublicSerializer
from django.db.models import Q

class GlobalSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"results": {"destinations": [], "hotels": [], "attractions": []}})

        destinations = Destination.objects.filter(
            Q(status='PUBLISHED') & (Q(name__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query))
        )[:10]
        
        hotels = Hotel.objects.filter(
            Q(status='PUBLISHED') & (Q(name__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query))
        )[:10]
        
        attractions = Attraction.objects.filter(
            Q(status='PUBLISHED') & (Q(name__icontains=query) | Q(city__icontains=query) | Q(country__icontains=query) | Q(category__icontains=query))
        )[:10]

        return Response({
            "query": query,
            "results": {
                "destinations": DestinationPublicSerializer(destinations, many=True).data,
                "hotels": HotelPublicSerializer(hotels, many=True).data,
                "attractions": AttractionPublicSerializer(attractions, many=True).data
            }
        })
