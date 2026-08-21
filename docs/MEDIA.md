# Media Management API

This document outlines the Image and Media management API for Wanderworld-AI.

## Models
- `DestinationImage`
- `HotelImage`
- `AttractionImage`

All image models inherit from a base class with common fields: `alt_text`, `caption`, `display_order`, `is_primary`.

## Functionality
- **Centralized Management:** Images are associated with Destinations, Hotels, or Attractions.
- **Primary Image Logic:** Maximum one primary image per entity. Setting a new primary image automatically unsets the old one.
- **Ordering:** Images support display ordering.
- **Validation:** Supported image types and size validation.

## Admin APIs (Requires Admin Auth)
- `POST /api/v1/admin/{entity}/{entity_id}/images/`: Upload image.
- `GET /api/v1/admin/{entity}/{entity_id}/images/`: List images.
- `PATCH /api/v1/admin/{entity}/{entity_id}/images/{id}/`: Update image metadata.
- `DELETE /api/v1/admin/{entity}/{entity_id}/images/{id}/`: Delete image.

## Future Strategy
- Media storage is abstracted via Django's `DEFAULT_FILE_STORAGE` settings, enabling seamless migration to cloud object storage (AWS S3, GCS) in the future.
