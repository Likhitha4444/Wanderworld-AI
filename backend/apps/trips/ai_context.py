from django.contrib.auth import get_user_model
from apps.trips.models import Trip
from apps.travel_dna.models import UserTravelDNA
from apps.recommendations.services import get_recommendations
from apps.destinations.models import Destination

def build_trip_context(user, trip: Trip) -> dict:
    """Builds a structured Python dictionary for AI trip planning."""
    
    # Travel DNA
    dna = list(UserTravelDNA.objects.filter(user=user).values('category__name', 'score'))
    
    # Recommendations
    top_destinations = get_recommendations(user, 'destination')[:5]
    top_hotels = get_recommendations(user, 'hotel')[:3]
    top_attractions = get_recommendations(user, 'attraction')[:5]

    context = {
        'trip_details': {
            'destination': trip.destination.name,
            'start_date': str(trip.start_date),
            'end_date': str(trip.end_date),
            'travelers': trip.number_of_travelers,
            'budget': float(trip.budget),
            'currency': trip.currency,
        },
        'user_context': {
            'travel_dna': dna,
        },
        'recommendations': {
            'destinations': [{'id': r['item'].id, 'name': r['item'].name} for r in top_destinations],
            'hotels': [{'id': r['item'].id, 'name': r['item'].name} for r in top_hotels],
            'attractions': [{'id': r['item'].id, 'name': r['item'].name} for r in top_attractions],
        }
    }
    
    return context
