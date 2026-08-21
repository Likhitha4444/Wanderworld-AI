# Hotels and Rooms API

This document outlines the Hotel and Room management API for Wanderworld-AI.

## Endpoints

### Hotel Public APIs
- `GET /api/v1/hotels/`: List all published hotels (Supports search, filter, order, pagination).
- `GET /api/v1/hotels/{slug}/`: Retrieve details of a published hotel.
- `GET /api/v1/destinations/{destination_slug}/hotels/`: List all published hotels for a destination.

### Room Public APIs
- `GET /api/v1/hotels/{hotel_slug}/rooms/`: List all active rooms for a published hotel.

### Admin APIs (Requires Admin Auth)
- `POST /api/v1/admin/hotels/`: Create a new hotel.
- `GET /api/v1/admin/hotels/`: List all hotels.
- `GET /api/v1/admin/hotels/{id}/`: Retrieve hotel details.
- `PATCH /api/v1/admin/hotels/{id}/`: Update hotel.
- `DELETE /api/v1/admin/hotels/{id}/`: Delete/archive a hotel.

- `POST /api/v1/admin/hotels/{hotel_id}/rooms/`: Create a room for a hotel.
- `GET /api/v1/admin/hotels/{hotel_id}/rooms/`: List rooms for a hotel.
- `PATCH /api/v1/admin/hotels/{hotel_id}/rooms/{id}/`: Update room.
- `DELETE /api/v1/admin/hotels/{hotel_id}/rooms/{id}/`: Delete room.

## Functionality
- **Status Management:** Only published hotels and active rooms are visible publicly.
- **Relationships:** Hotels belong to destinations; rooms belong to hotels.
- **Validation:** Enforces price, capacity, and room availability constraints.
