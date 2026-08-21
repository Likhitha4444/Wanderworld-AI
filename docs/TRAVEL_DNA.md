# Travel DNA API

This document outlines the Travel DNA personalization engine for Wanderworld-AI.

## Concept
Travel DNA represents a structured, deterministic representation of a user's travel preferences. It is based on real interactions (Wishlists, Reviews) and is independent of AI/Gemini.

## Models
- `TravelDNACategory`: Defines travel personality categories (e.g., Nature, Adventure).
- `UserTravelDNA`: Stores a user's score (0–100) and confidence (0–1) for each category.

## Functionality
- **Calculation:** Scores are calculated deterministically based on frequency and quality of interactions (Wishlist, Reviews).
- **Recalculation:** Scores are recalculated on demand via the `/api/v1/travel-dna/recalculate/` endpoint.
- **Independence:** The engine operates independently from any AI models.

## APIs
- `GET /api/v1/travel-dna/`: Retrieves the authenticated user's calculated travel DNA profile.
- `POST /api/v1/travel-dna/recalculate/`: Triggers a recalculation of the user's travel DNA based on current activity.

## Scoring System
- **Score:** 0–100 (normalized).
- **Confidence:** 0.0–1.0 (heuristic based on activity volume).
- **Isolation:** Users can only access their own Travel DNA data.
