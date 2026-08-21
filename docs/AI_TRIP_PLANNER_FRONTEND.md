# AI Trip Planner Frontend

## Overview
The AI Trip Planner frontend provides users with a complete workflow to create, manage, and generate AI-powered itineraries.

## Key Features
- **Trip Creation**: Users can plan a trip by selecting a destination, dates, and budget.
- **Trip Management**: Users can view their trips and see the current status (DRAFT, GENERATING, READY, FAILED).
- **AI Generation**: Users can trigger AI itinerary generation, which leverages the backend Trip Generation service.
- **Itinerary View**: Once generated, users can view their itinerary organized by days and activities.

## Services
- `tripService.js`: Handles all trip-related API interactions (creating, listing, retrieving, triggering generation).

## Pages
- `TripListPage.jsx`: Displays all trips created by the authenticated user.
- `TripPlannerPage.jsx`: Form for collecting trip details (destination, dates, budget).
- `TripDetailPage.jsx`: Shows detailed trip information, allows AI generation trigger, and displays the generated itinerary.

## Implementation Details
- API interaction uses the centralized `apiClient`.
- Authentication is enforced via `ProtectedRoute`.
- UI uses standard React state management (`useState`, `useEffect`).
- Backend authorization ensures users can only access their own trips.
