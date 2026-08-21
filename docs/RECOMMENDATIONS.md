# Recommendation Engine API

This document outlines the deterministic Travel Recommendation Engine for Wanderworld-AI.

## Concept
The Recommendation Engine provides ranked, explainable travel recommendations (Destinations, Hotels, Attractions) based on a deterministic analysis of the user's Travel DNA, Wishlist, Reviews, and behavioral interactions. It does not use AI or ML.

## Scoring Logic
Recommendations are ranked based on a weighted sum of components:
- **Travel DNA Match (50%):** Measures similarity between user Travel DNA categories and entity attributes.
- **Budget Compatibility (20%):** Matches entity costs with user budget preferences.
- **Popularity (10%):** Incorporates popularity scores.
- **Other Affinities (20%):** Aggregates signals from Wishlist and Review history.

## Explanation
Each recommendation includes a list of "reasons" explaining the match, derived deterministically from the scoring factors.

## APIs
- `GET /api/v1/recommendations/?type={type}`: Retrieves ranked recommendations for the authenticated user, where `{type}` is `destination`, `hotel`, or `attraction`.

## Functionality
- **Visibility:** Only `PUBLISHED` entities are recommended.
- **Isolation:** Recommendations are strictly personalized to the authenticated user.
- **Cold Start:** Currently returns fallback recommendations (e.g., highly rated entities) if insufficient personalized data exists, clearly marked.
- **Performance:** Deterministically calculated at request time; logic is separated into a service layer (`recommendations/services.py`).
