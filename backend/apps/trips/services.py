from decimal import Decimal
from django.db.models import Sum
from apps.trips.models import Trip, TripActivity

def calculate_trip_budget(trip: Trip) -> dict:
    """Calculates estimated trip budget and remaining balance."""
    activities = TripActivity.objects.filter(trip_day__trip=trip)
    estimated_cost = activities.aggregate(total=Sum('estimated_cost'))['total'] or Decimal('0.00')
    
    remaining_budget = trip.budget - estimated_cost
    
    budget_used_percentage = (estimated_cost / trip.budget * 100) if trip.budget > 0 else Decimal('0.00')
    
    return {
        'estimated_cost': estimated_cost,
        'remaining_budget': remaining_budget,
        'budget_used_percentage': round(budget_used_percentage, 2)
    }
