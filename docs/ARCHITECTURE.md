# Architecture: WanderWorld

## Overview
WanderWorld follows a decoupled, production-ready architecture.

## Tech Stack
- **Frontend:** React.js
- **API/Backend:** Django REST Framework
- **Database:** PostgreSQL
- **AI/External APIs:** Gemini, Maps, Weather, Payments

## Communication Flow
1. **Client** (React) requests data from **API** (Django).
2. **API** interacts with **PostgreSQL** or calls external **Services** (AI/Maps/Weather).
3. **API** returns JSON response to **Client**.
