# Destinations API

This document outlines the destination management API for Wanderworld-AI.

## Endpoints

### Public APIs
- `GET /api/v1/destinations/`: List all published destinations (Supports search, filter, order, pagination).
- `GET /api/v1/destinations/{slug}/`: Retrieve details of a published destination.

### Admin APIs (Requires Admin Auth)
- `POST /api/v1/admin/destinations/`: Create a new destination.
- `GET /api/v1/admin/destinations/`: List all destinations (including draft/archived).
- `GET /api/v1/admin/destinations/{id}/`: Retrieve destination details.
- `PATCH /api/v1/admin/destinations/{id}/`: Update destination.
- `DELETE /api/v1/admin/destinations/{id}/`: Delete a destination.

## Functionality
- **Status Management:** Only published destinations are visible to public.
- **Filtering:** Public APIs support filtering by country, region, city, and featured status.
- **Search:** Public APIs support search by name, description, country, region, and city.
- **Ordering:** Supports ordering by name, budget, and creation date.
- **Validation:** Enforces coordinate ranges and non-negative budgets.
