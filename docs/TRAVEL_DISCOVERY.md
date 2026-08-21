# Travel Discovery API

This document outlines the Unified Travel Discovery & Search API for Wanderworld-AI.

## Endpoints

### 1. Global Search
- `GET /api/v1/search/?q={query}`: Unified search across Destinations, Hotels, and Attractions.

### 2. Nearby Discovery
- `GET /api/v1/attractions/nearby/?latitude={lat}&longitude={lon}&radius_km={radius}`: Finds attractions within a given radius.

### 3. Destination Detail Aggregation
- `GET /api/v1/destinations/{slug}/`: Now includes aggregated lists of published hotels and attractions.

## Functionality
- **Search:** Case-insensitive search across relevant fields for each entity.
- **Visibility:** All discovery endpoints strictly enforce `status='PUBLISHED'` for entities.
- **Performance:** Optimized with `prefetch_related` for nested data (hotels/attractions).
- **Nearby Search:** Implemented using haversine distance calculation in the ORM.
