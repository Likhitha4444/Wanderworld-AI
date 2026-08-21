# Travel Behavior API

This document outlines the Travel Behavior and Event Signal API for Wanderworld-AI.

## Endpoints

### Event Recording
- `POST /api/v1/behavior/events/`: Records a user's travel behavior event (e.g., view, search, wishlist action).

### Event Querying
- `GET /api/v1/behavior/events/`: List the authenticated user's own behavior events.

## Functionality
- **Signal Sources:** Records `DESTINATION_VIEW`, `HOTEL_VIEW`, `ATTRACTION_VIEW`, `SEARCH`, `WISHLIST_ADD`, `WISHLIST_REMOVE`, `REVIEW_SUBMITTED`.
- **Target Validation:** Ensures entity-specific events reference only `PUBLISHED` entities.
- **Privacy/Security:** Strict user isolation; users can only record and query their own behavior data.
- **DNA Integration:** Behavioral events are utilized as a medium-weight signal source by the Travel DNA calculation engine to inform user travel personality scores.
- **Performance:** Efficiently handles event recording; normalization and decay are applied during Travel DNA recalculation.
