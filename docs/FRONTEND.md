# Frontend Architecture

## Overview
The frontend is a React application built with Vite.

## Folder Structure
- `src/api`: Centralized Axios client with JWT interceptors.
- `src/components`: Reusable components (Layout, ProtectedRoute, ErrorBoundary, ChangePasswordForm, etc.).
- `src/context`: React context for global auth state (AuthContext).
- `src/pages`: Application pages (Login, Register, Profile).

## API Client
- Uses Axios with a base URL defined in `VITE_API_BASE_URL`.
- Interceptors:
    - Request: Automatically adds `Authorization: Bearer <token>` to requests.
    - Response: Handles 401 errors by attempting token refresh and retrying the request.

## Authentication
- `AuthContext`: Manages user state and authentication methods (`login`, `register`, `logout`).
- JWT Storage: Tokens (`access`, `refresh`) are stored in `localStorage`. 
  - *Security Tradeoff*: `localStorage` is vulnerable to XSS. This is acceptable for this development prototype but should be replaced with `HttpOnly` cookies in a production environment.
- `ProtectedRoute`: Redirects unauthenticated users to `/login`.

## Authentication APIs
- POST `/auth/register/`
- POST `/auth/login/`
- POST `/auth/logout/`
- POST `/auth/token/refresh/`
- POST `/auth/change-password/`
- GET `/auth/me/`
- GET `/profile/`
- PATCH `/profile/`

## Development
- Run `npm run dev` to start the development server.
- Ensure backend server is running at `http://127.0.0.1:8000`.
