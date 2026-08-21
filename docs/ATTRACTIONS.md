# Attractions API

This document outlines the Attraction management API for Wanderworld-AI.

## Endpoints

### Public APIs
- `GET /api/v1/attractions/`: List all published attractions (Supports search, filter, order, pagination).
- `GET /api/v1/attractions/{slug}/`: Retrieve details of a published attraction.
- `GET /api/v1/destinations/{destination_slug}/attractions/`: List all published attractions for a destination.

### Admin APIs (Requires Admin Auth)
- `POST /api/v1/admin/attractions/`: Create a new attraction.
- `GET /api/v1/admin/attractions/`: List all attractions.
- `GET /api/v1/admin/attractions/{id}/`: Retrieve attraction details.
- `PATCH /api/v1/admin/attractions/{id}/`: Update attraction.
- `DELETE /api/v1/admin/attractions/{id}/`: Delete/archive an attraction.

## Functionality
- **Status Management:** Only published attractions are visible to public.
- **Relationships:** Attractions belong to destinations.
- **Validation:** Enforces coordinate, entry fee, duration, and rating constraints.
