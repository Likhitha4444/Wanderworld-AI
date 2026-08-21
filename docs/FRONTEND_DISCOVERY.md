# Frontend Discovery Architecture

## Overview
The WanderWorld Travel Discovery UI allows users to search for and explore destinations, hotels, and attractions. It consumes the real Django REST APIs.

## Key Features
- **Global Search**: Search across destinations, hotels, and attractions.
- **Destination Listing**: Browse published destinations.
- **Destination Detail**: View detailed information about a destination, including nested hotels and attractions.
- **Real-Time Data**: All discovery data is fetched directly from the backend.

## Services
- `destinationService.js`: Fetches destination list and details.
- `searchService.js`: Performs global searches.

## Components
- `SearchBar`: Global search input.
- `HotelCard`: Displays hotel information.
- `AttractionCard`: Displays attraction information.
- `DestinationList`: Renders a list of destination cards.
- `DestinationDetail`: Renders the detailed view of a destination with nested content.

## Implementation Details
- API interaction is centralized via `apiClient`.
- Loading and Error states are handled per-component.
- All routing is configured in `App.jsx`.
