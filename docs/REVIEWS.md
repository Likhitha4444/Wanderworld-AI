# Reviews and Ratings API

This document outlines the Review and Rating management API for Wanderworld-AI.

## Endpoints

### User Review Management
- `POST /api/v1/reviews/`: Create a review for a Hotel or Attraction.
- `GET /api/v1/reviews/`: List user's reviews.
- `PATCH /api/v1/reviews/{id}/`: Update user's review.
- `DELETE /api/v1/reviews/{id}/`: Delete user's review.

### Public Review Listing
- `GET /api/v1/hotels/{hotel_slug}/reviews/`: List published reviews for a hotel.
- `GET /api/v1/attractions/{attraction_slug}/reviews/`: List published reviews for an attraction.

### Admin Moderation
- `GET /api/v1/admin/reviews/`: List all reviews.
- `PATCH /api/v1/admin/reviews/{id}/`: Moderate review status (PUBLISH/REJECT).

## Functionality
- **Moderation:** Reviews are `PENDING` by default. Admins must `PUBLISH` reviews for them to be visible publicly.
- **Rating Aggregation:** Average rating and review count are dynamically recalculated and synchronized to the Hotel/Attraction models when a published review is saved or deleted.
- **Constraints:** Exactly one target (Hotel or Attraction) per review. One review per user per target.
- **Isolation:** Users can only modify/delete their own reviews.
- **Visibility:** Only `PUBLISHED` reviews are visible to public users or factored into ratings.
