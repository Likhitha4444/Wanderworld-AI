# AI Infrastructure

## 1. AI Architecture
WanderWorld uses a centralized AI service (`apps.ai`) to interact with the Google Gemini API. This service abstracts the SDK and enforces strict separation between business logic and the AI provider.

## 2. Gemini Integration
We use the official `google-genai` Python SDK. The API key is managed through environment variables and is never exposed to the frontend or logged.

## 3. Configuration
- `GEMINI_API_KEY`: Required.
- `GEMINI_MODEL`: Defaults to `gemini-2.5-flash`.
- `GEMINI_TIMEOUT`: Defaults to 30 seconds.
- `GEMINI_MAX_RETRIES`: Defaults to 3.

## 4. Error Handling
We use custom AI exceptions (`AIConfigurationError`, `AIAuthenticationError`, `AIRateLimitError`, `AITimeoutError`, `AIServiceUnavailableError`, `AIResponseError`) to map raw provider errors into safe, application-level exceptions.

## 5. Security & Prompt Injection
- API key never reaches frontend.
- API key never appears in logs.
- Sensitive user data (JWT, password, PII) is never sent to Gemini.
- We implement strict separation between system instructions, user context, and user input to mitigate prompt injection risks.

## 6. Future AI Trip Planner
The foundation supports structured AI responses, validation layers, and context-aware prompt building to support the future AI Trip Planner.
