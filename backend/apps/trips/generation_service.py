import logging
import json
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.ai.services import GeminiService
from apps.trips.models import Trip, TripStatus, TripDay, TripActivity, TripRevision
from apps.trips.services import calculate_trip_budget
from apps.destinations.models import Destination
from apps.attractions.models import Attraction
from apps.hotels.models import Hotel
from decimal import Decimal

logger = logging.getLogger(__name__)

class TripGenerationService:
    def __init__(self):
        self.ai_service = GeminiService()

    def generate_itinerary(self, user, trip_id, preferences):
        trip = Trip.objects.select_related('destination').get(id=trip_id, user=user)

        if trip.status == TripStatus.READY:
            raise ValidationError("Trip is already generated.")
        if trip.status == TripStatus.GENERATING:
            raise ValidationError("Trip is already being generated.")
        
        trip.status = TripStatus.GENERATING
        trip.save()

        try:
            from .ai_context import build_trip_context
            context = build_trip_context(user, trip)
            context['preferences'] = preferences
            
            prompt = f"""
Generate an itinerary for the trip: {trip.title}.
Use this context data: {json.dumps(context)}.

Output STRICTLY valid JSON. Do NOT include markdown code fences (like ```json), do NOT include any explanatory text before or after the JSON.

The top-level JSON object MUST contain a key "days", which is a list of objects.
Each object in "days" MUST have:
- day_number (int)
- date (YYYY-MM-DD string)
- title (string)
- summary (string)
- activities (list of objects)

Each object in "activities" MUST have:
- attraction_id (int, optional; MUST refer to an existing attraction ID from the provided context)
- activity_type (string, one of: ATTRACTION, MEAL, HOTEL, TRAVEL, FREE_TIME, CUSTOM)
- title (string)
- start_time (HH:MM:SS string)
- end_time (HH:MM:SS string)
- duration_minutes (int)
- estimated_cost (float)
- sequence (int)

Constraint Rules:
1. attraction_id MUST refer ONLY to an existing attraction from the context. Do NOT invent IDs.
2. start_time < end_time.
3. sequence must be chronological within each day (1, 2, 3...).
4. Activities must not overlap in time.
5. Dates must fall within trip start/end range.
6. Total estimated_cost must not exceed trip budget ({float(trip.budget)}).
7. Generate a realistic, useful itinerary.
"""
            response = self.ai_service.generate(prompt)
            
            if response['status'] != 'success':
                raise Exception("AI generation failed.")
                
            data = response['data']

            # Quality Evaluation
            from .quality import evaluate_itinerary
            quality_result = evaluate_itinerary(trip, data)
            if quality_result['status'] == 'FAIL':
                raise ValidationError(f"Itinerary quality check failed: {quality_result['errors']}")

            # 3. Validate and Persist
            with transaction.atomic():
                self._persist_itinerary(trip, user, data)

                # Budget validation (Keep for redundancy as per requirement)
                budget_summary = calculate_trip_budget(trip)
                if budget_summary['estimated_cost'] > trip.budget:
                    raise ValidationError(f"Itinerary cost ({budget_summary['estimated_cost']}) exceeds trip budget ({trip.budget}).")

                trip.status = TripStatus.READY
                trip.save()

            return trip



        except Exception as e:
            logger.error(f"Generation failed: {e}")
            trip.status = TripStatus.FAILED
            trip.save()
            raise e

    def _persist_itinerary(self, trip, user, data):
        # 1. Basic schema validation
        if 'days' not in data:
            print(f"DEBUG: Data received by _persist_itinerary: {json.dumps(data)}")
            raise ValidationError(f"Invalid response schema: missing 'days'. Received: {data}")
        
        # 2. Persist TripDays and TripActivities
        last_revision = TripRevision.objects.filter(trip=trip).order_by('-revision_number').first()
        new_revision_number = (last_revision.revision_number + 1) if last_revision else 1
        
        for day_data in data['days']:
            day = TripDay.objects.create(
                trip=trip,
                day_number=day_data['day_number'],
                date=day_data['date'],
                title=day_data.get('title', ''),
                summary=day_data.get('summary', '')
            )
            for act_data in day_data.get('activities', []):
                # ID validation (simplified for now)
                attraction = None
                if act_data.get('attraction_id'):
                    attraction = Attraction.objects.filter(id=act_data['attraction_id'], destination=trip.destination, status='PUBLISHED').first()
                    if not attraction:
                        raise ValidationError(f"Invalid or unpublished attraction: {act_data.get('attraction_id')}")

                TripActivity.objects.create(
                    trip_day=day,
                    attraction=attraction,
                    activity_type=act_data['activity_type'],
                    title=act_data['title'],
                    start_time=act_data['start_time'],
                    end_time=act_data['end_time'],
                    duration_minutes=act_data['duration_minutes'],
                    estimated_cost=Decimal(str(act_data.get('estimated_cost', '0.00'))),
                    sequence=act_data['sequence']
                )
        
        # 3. Create Revision
        TripRevision.objects.create(
            trip=trip,
            revision_number=new_revision_number,
            itinerary_snapshot=data,
            created_by=user,
            change_reason='AI Generation'
        )
