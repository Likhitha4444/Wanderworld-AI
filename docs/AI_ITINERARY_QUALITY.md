# AI Itinerary Quality Engine

## 1. Architecture
The Quality Engine (`apps.trips.quality`) performs deterministic, rule-based validation on AI-generated itineraries *after* Gemini generation but *before* transactional persistence.

## 2. Components
- `rules.py`: Contains validation rules: `validate_schedule`, `validate_budget`.
- `engine.py`: Orchestrates validation and computes a deterministic quality score.

## 3. Scoring
- **Score Range:** 0–100.
- **Formula:** `100 - (error_count * 20) - (warning_count * 5)` (normalized to 0–100).
- **Quality Gates:**
    - `FAIL` (status="FAIL"): If any error-level rule is triggered.
    - `WARNING` (status="WARNING"): If any warning-level rule is triggered AND the score falls below 75.
    - `PASS` (status="PASS"): No errors and score >= 75.

## 4. Implemented Rules
- **Schedule Quality:** Detects activity overlaps.
- **Daily Balance & Density:** Detects overloaded days (9+ activities: Error, 7-8 activities: Warning) and empty days (Warning).
- **Budget Quality:** Detects total budget violation (Error) and extreme budget concentration in a single activity (Warning).

## 5. Integration
The `TripGenerationService` calls `evaluate_itinerary`. If the result status is `FAIL`, the persistence step is skipped, the itinerary is not created, and the trip is marked as `FAILED`.
