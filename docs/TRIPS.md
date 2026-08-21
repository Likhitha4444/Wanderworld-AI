# Trips Planning

## 1. Architecture
The trips application manages user-created itineraries, including days and activities. It maintains revision history for itineraries.

## 2. Models
- `Trip`: Represents the main trip, linked to a user and a destination.
- `TripDay`: Represents a single day in a trip.
- `TripActivity`: Represents an activity within a trip day, linked to an attraction or hotel (optional).
- `TripRevision`: Stores immutable snapshots of itineraries for revision history.

## 3. Budgeting
- Budget and costs are handled using `DecimalField` to ensure precision.
- Total costs are calculated by aggregating activity costs.

## 4. Revision Immutability
Once created, `TripRevision` records are immutable. A new revision must be created for any changes.

## 5. Security & Ownership
- API endpoints strictly enforce user ownership.
- Users can only access, modify, or delete their own trips.
- IDOR is prevented.

## 6. Future Gemini Integration
- This foundation allows for structured AI itineraries.
- AI itinerary generation is NOT yet implemented.
- The `itinerary_snapshot` in `TripRevision` is a JSON field designed to store structured AI output for future validation.
