# AI Trip Planner

## 1. Architecture
The AI Trip Planner uses a service-oriented approach. The `TripGenerationService` orchestrates the process: context building, Gemini API interaction, structured response parsing, validation, and transactional persistence.

## 2. Generation Flow
1. User requests generation.
2. System validates trip state (`DRAFT` only).
3. System builds context (Travel DNA, catalog entities).
4. System calls Gemini API (wrapped in `GeminiService`).
5. System validates JSON output against schema.
6. System performs business validation (dates, budget, catalog entity IDs).
7. System persists itinerary in a database transaction.
8. System updates trip status to `READY` or `FAILED`.

## 3. Security
- API endpoints require JWT authentication and verify trip ownership (User IDOR prevention).
- Gemini API key and provider configuration are strictly managed via environment variables.
- Prompt injection mitigation: Input data is delimited and structured as data, not instructions.
- Generation status is controlled by backend logic to prevent metadata spoofing.

## 4. Validation
- Schema validation ensures required fields exist.
- ID validation ensures catalog entities exist and belong to the trip's destination.
- Budget validation checks if the generated itinerary fits the defined budget.
- Time consistency checks prevent overlapping activities within a day.

## 5. Persistence
- Generation happens outside of database transactions initially.
- Persistence is performed inside a database transaction to ensure atomicity.

## 6. Limitations
- Gemini itinerary generation is currently single-destination.
- The Re-Optimizer is not yet implemented.
