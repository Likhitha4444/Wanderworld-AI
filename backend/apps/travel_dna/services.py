from apps.travel_dna.models import TravelBehaviorEvent, TravelDNACategory, UserTravelDNA
from apps.wishlist.models import Wishlist
from apps.reviews.models import Review
from django.db import models
from django.db.models import Avg, Count
from django.utils import timezone
import datetime

def record_event(user, event_type, destination=None, hotel=None, attraction=None, metadata=None):
    if metadata is None:
        metadata = {}
    return TravelBehaviorEvent.objects.create(
        user=user,
        event_type=event_type,
        destination=destination,
        hotel=hotel,
        attraction=attraction,
        metadata=metadata
    )

def calculate_dna_score(user):
    category_map = {
        'HISTORICAL': 'history',
        'CULTURAL': 'culture',
        'NATURE': 'nature',
        'ADVENTURE': 'adventure',
        'RELIGIOUS': 'spiritual',
        'MUSEUM': 'culture',
        'BEACH': 'relaxation',
        'PARK': 'nature',
        'SHOPPING': 'shopping',
        'ENTERTAINMENT': 'nightlife',
    }

    # Signals
    wishlist_items = Wishlist.objects.filter(user=user)
    reviews = Review.objects.filter(user=user, status='PUBLISHED')
    recent_events = TravelBehaviorEvent.objects.filter(
        user=user, 
        created_at__gte=timezone.now() - datetime.timedelta(days=30)
    )

    raw_scores = {}

    def add_signal(cat, weight):
        raw_scores[cat] = raw_scores.get(cat, 0) + weight

    for entry in wishlist_items:
        target = entry.destination or entry.hotel or entry.attraction
        if hasattr(target, 'category'):
            add_signal(category_map.get(target.category, 'other'), 10)
    
    for review in reviews:
        target = review.hotel or review.attraction
        if hasattr(target, 'category'):
            add_signal(category_map.get(target.category, 'other'), review.rating * 4)

    for event in recent_events:
        target = event.destination or event.hotel or event.attraction
        if target and hasattr(target, 'category'):
            add_signal(category_map.get(target.category, 'other'), 2)
        elif event.event_type == 'SEARCH' and 'query' in event.metadata:
            # Simple keyword mapping
            query = event.metadata['query'].lower()
            if 'nature' in query: add_signal('nature', 1)
            elif 'history' in query: add_signal('history', 1)

    # Normalize and Save
    max_score = max(raw_scores.values()) if raw_scores else 1
    
    for cat_slug, score in raw_scores.items():
        category = TravelDNACategory.objects.get(slug=cat_slug)
        norm_score = int((score / max_score) * 100)
        confidence = min(1.0, len(wishlist_items) * 0.1 + len(reviews) * 0.05 + len(recent_events) * 0.01)
        
        UserTravelDNA.objects.update_or_create(
            user=user, category=category,
            defaults={'score': norm_score, 'confidence': confidence}
        )
