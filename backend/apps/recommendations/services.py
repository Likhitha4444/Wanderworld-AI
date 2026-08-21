from decimal import Decimal
from django.db.models import Avg
from apps.travel_dna.models import UserTravelDNA
from apps.destinations.models import Destination
from apps.hotels.models import Hotel
from apps.attractions.models import Attraction

# Weights (Must total 100%)
WEIGHT_DNA = Decimal('0.60')
WEIGHT_QUALITY = Decimal('0.30')
WEIGHT_POPULARITY = Decimal('0.10')

CATEGORY_MAP = {
    'HISTORICAL': 'history',
    'CULTURAL': 'culture',
    'NATURE': 'nature',
    'ADVENTURE': 'adventure',
    'RELIGIOUS': 'spiritual',
    'MUSEUM': 'history',
    'BEACH': 'relaxation',
    'PARK': 'nature',
    'SHOPPING': 'shopping',
    'ENTERTAINMENT': 'nightlife',
    'OTHER': 'other',
}

def get_recommendations(user, target_type):
    dna = UserTravelDNA.objects.filter(user=user)
    dna_scores = {d.category.slug: d.score for d in dna}
    is_personalized = dna.exists()
    
    if target_type == 'destination':
        candidates = Destination.objects.filter(status='PUBLISHED')
        return _score_destinations(candidates, dna_scores, is_personalized)
    elif target_type == 'hotel':
        candidates = Hotel.objects.filter(status='PUBLISHED')
        return _score_hotels(candidates, dna_scores, is_personalized)
    elif target_type == 'attraction':
        candidates = Attraction.objects.filter(status='PUBLISHED')
        return _score_attractions(candidates, dna_scores, is_personalized)
    return []

def _score_attractions(candidates, dna_scores, is_personalized):
    scored = []
    if not is_personalized:
        for cand in candidates.order_by('-average_rating')[:10]:
            scored.append({'item': cand, 'score': 0.5, 'reasons': ["Popular attraction fallback."], 'personalized': False})
        return scored

    for cand in candidates:
        score = Decimal('0.0')
        reasons = []
        
        # DNA Match
        cat_slug = CATEGORY_MAP.get(cand.category, 'other')
        if cat_slug in dna_scores:
            score += Decimal(str(dna_scores[cat_slug])) * WEIGHT_DNA / 100
            reasons.append(f"Matches your {cat_slug} preference.")
        
        # Quality
        score += Decimal(str(cand.average_rating)) / 5 * WEIGHT_QUALITY
        
        # Popularity
        score += Decimal(str(min(cand.popularity_score, 100))) / 100 * WEIGHT_POPULARITY
        
        scored.append({'item': cand, 'score': float(score), 'reasons': reasons, 'personalized': True})
    
    return sorted(scored, key=lambda x: x['score'], reverse=True)

def _score_destinations(candidates, dna_scores, is_personalized):
    scored = []
    for cand in candidates:
        score = Decimal('0.0')
        reasons = []
        
        # DNA Match
        attr_categories = cand.attractions.values_list('category', flat=True)
        match_count = 0
        if attr_categories and is_personalized:
            for cat in attr_categories:
                cat_slug = CATEGORY_MAP.get(cat, 'other')
                if cat_slug in dna_scores:
                    score += Decimal(str(dna_scores[cat_slug])) * WEIGHT_DNA / 100
                    match_count += 1
            if match_count > 0:
                score /= match_count
                reasons.append(f"Destination has {match_count} attractions matching your Travel DNA.")
        
        # Quality (Assume rating exists or fallback)
        # Using a default or popular attraction score if needed
        score += Decimal('0.5') * WEIGHT_QUALITY 
        
        # Fallback if no personalized matches
        if score < Decimal('0.1'):
            if cand.is_featured:
                score = Decimal('0.3')
                reasons = ["Featured destination."]
            else:
                score = Decimal('0.1')
                reasons = ["General destination."]
        
        scored.append({'item': cand, 'score': float(score), 'reasons': list(set(reasons)), 'personalized': bool(match_count > 0)})
    
    return sorted(scored, key=lambda x: x['score'], reverse=True)

def _score_hotels(candidates, dna_scores, is_personalized):
    scored = []
    for cand in candidates:
        score = Decimal('0.0')
        reasons = []
        
        if is_personalized:
            # Use destination score (60%)
            dest_score = Decimal(str(_score_destinations([cand.destination], dna_scores, is_personalized)[0]['score']))
            score += dest_score * WEIGHT_DNA
            
            # Use rating (25%)
            score += Decimal(str(cand.average_rating)) / 5 * Decimal('0.25')
            
            # Use star rating (15%)
            score += Decimal(str(cand.star_rating)) / 5 * Decimal('0.15')
            reasons.append("Personalized based on destination match and hotel quality.")
        else:
            score = Decimal('0.3') # Non-personalized fallback
            reasons = ["Popular hotel recommendation."]
            
        scored.append({'item': cand, 'score': float(score), 'reasons': reasons, 'personalized': is_personalized})
        
    return sorted(scored, key=lambda x: x['score'], reverse=True)
