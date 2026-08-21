from decimal import Decimal
from django.db.models import Sum

# Quality Error Codes
ERR_DAY_MISSING = "DAY_MISSING"
ERR_DAY_EXTRA = "DAY_EXTRA"
ERR_DAY_DUPLICATE = "DAY_DUPLICATE"
ERR_DAY_OVERLOADED = "DAY_OVERLOADED"
ERR_DAY_EMPTY = "DAY_EMPTY"
ERR_ACTIVITY_OVERLAP = "ACTIVITY_OVERLAP"
ERR_ACTIVITY_INVALID_TIME = "ACTIVITY_INVALID_TIME"
ERR_ACTIVITY_INVALID_SEQUENCE = "ACTIVITY_INVALID_SEQUENCE"
ERR_DUPLICATE_ACTIVITY = "DUPLICATE_ACTIVITY"
ERR_INSUFFICIENT_REST = "INSUFFICIENT_REST"
ERR_MEAL_GAP = "MEAL_GAP"
ERR_LOW_DIVERSITY = "LOW_DIVERSITY"
ERR_BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
ERR_BUDGET_CONCENTRATION = "BUDGET_CONCENTRATION"
ERR_INVALID_CATALOG_ENTITY = "INVALID_CATALOG_ENTITY"
ERR_CROSS_DESTINATION_ENTITY = "CROSS_DESTINATION_ENTITY"
ERR_PREFERENCE_MISMATCH = "PREFERENCE_MISMATCH"

SEV_INFO = "INFO"
SEV_WARNING = "WARNING"
SEV_ERROR = "ERROR"

def validate_schedule(trip, itinerary_data):
    errors = []
    warnings = []
    
    # 1. Overlap check
    for day in itinerary_data.get('days', []):
        activities = sorted(day.get('activities', []), key=lambda x: x['start_time'])
        for i in range(len(activities) - 1):
            if activities[i]['end_time'] > activities[i+1]['start_time']:
                errors.append({
                    "code": ERR_ACTIVITY_OVERLAP,
                    "severity": SEV_ERROR,
                    "message": f"Overlapping activities: {activities[i]['title']} and {activities[i+1]['title']}",
                    "day": day['day_number']
                })
    
    # 2. Daily Balance & Density
    for day in itinerary_data.get('days', []):
        act_count = len(day.get('activities', []))
        if act_count == 0:
            warnings.append({"code": ERR_DAY_EMPTY, "severity": SEV_WARNING, "message": "Empty day", "day": day['day_number']})
        elif act_count > 9:
            errors.append({"code": ERR_DAY_OVERLOADED, "severity": SEV_ERROR, "message": "Overloaded day", "day": day['day_number']})
        elif act_count > 7:
            warnings.append({"code": ERR_DAY_OVERLOADED, "severity": SEV_WARNING, "message": "High activity density", "day": day['day_number']})
            
    return errors, warnings

def validate_budget(trip, itinerary_data):
    errors = []
    warnings = []
    
    total_cost = Decimal('0.00')
    max_activity_cost = Decimal('0.00')
    
    for day in itinerary_data.get('days', []):
        for act in day.get('activities', []):
            cost = Decimal(str(act.get('estimated_cost', '0.00')))
            total_cost += cost
            if cost > max_activity_cost:
                max_activity_cost = cost
            
    if total_cost > trip.budget:
        errors.append({
            "code": ERR_BUDGET_EXCEEDED,
            "severity": SEV_ERROR,
            "message": f"Itinerary cost {total_cost} exceeds budget {trip.budget}."
        })
    elif total_cost > Decimal('0.0') and (max_activity_cost / total_cost) > Decimal('0.8'):
        warnings.append({
            "code": ERR_BUDGET_CONCENTRATION,
            "severity": SEV_WARNING,
            "message": "Extreme budget concentration in a single activity."
        })
        
    return errors, warnings
