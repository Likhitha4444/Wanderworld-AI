# Wishlist API

This document outlines the User Wishlist management API for Wanderworld-AI.

## Endpoints

### Wishlist Management
- `POST /api/v1/wishlist/`: Add a destination, hotel, or attraction to the user's wishlist.
- `DELETE /api/v1/wishlist/{id}/`: Remove an item from the wishlist.
- `GET /api/v1/wishlist/`: List all items in the user's wishlist (supports pagination, filtering by type).

### Status Check
- `GET /api/v1/wishlist/check/?destination_id=...` OR `hotel_id=...` OR `attraction_id=...`: Checks if an item is already wishlisted.

## Functionality
- **User Isolation:** Users can only view and modify their own wishlist.
- **Duplicate Prevention:** A user cannot add the same item twice.
- **Entity Validation:** Only `PUBLISHED` destinations, hotels, and attractions can be wishlisted.
- **Exactly-one Target:** Each wishlist entry links to exactly one of Destination, Hotel, or Attraction.
- **Authentication:** All wishlist endpoints require JWT authentication.
