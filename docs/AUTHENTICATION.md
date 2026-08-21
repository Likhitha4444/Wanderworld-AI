# Authentication API

This document outlines the core authentication and profile API for Wanderworld-AI.

## Endpoints

### 1. Register User
`POST /api/v1/auth/register/`

Creates a new user account with a default role and auto-created profile.

### 2. Login
`POST /api/v1/auth/login/`

Authenticates a user and returns JWT tokens and user information.

### 3. Logout
`POST /api/v1/auth/logout/`

Invalidates a refresh token.

**Request Body:**
```json
{
    "refresh": "<refresh_token>"
}
```

### 4. Token Refresh
`POST /api/v1/auth/token/refresh/`

Refreshes the access token.

### 5. Change Password
`POST /api/v1/auth/change-password/`

Changes the user's password. Requires current password verification.

### 6. Current User
`GET /api/v1/auth/me/`

Retrieves the authenticated user's profile info.

### 7. Profile
`GET /api/v1/profile/`

Retrieves the authenticated user's profile fields.

`PATCH /api/v1/profile/`

Updates the authenticated user's profile fields.

## Testing

Run tests with:
`python manage.py test apps.accounts`
