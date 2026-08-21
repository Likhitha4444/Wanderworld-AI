# Backend Setup: WanderWorld

## 1. Environment
- **Python:** 3.12+ (in virtual environment)
- **Django:** 6.1
- **Django REST Framework:** 3.18.0
- **PostgreSQL Driver:** psycopg 3.3.4

## 2. Structure
- `backend/`: Django project root.
- `backend/.venv/`: Virtual environment.
- `backend/apps/`: Django modular applications.
- `backend/config/`: Django configuration package.

## 3. Setup
1. Create virtual environment: `python -m venv backend/.venv`
2. Install dependencies: `backend/.venv/Scripts/python -m pip install -r backend/requirements.txt`
3. Setup environment variables in `backend/.env` (use `backend/.env.example` as reference).

## 4. PostgreSQL Configuration
- Configured in `backend/config/settings.py` using standard Django PostgreSQL engine. Requires DB credentials in environment variables (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).

## 5. Running Backend
1. Activate environment: `backend/.venv/Scripts/activate`
2. Run server: `python backend/manage.py runserver`

## 6. API Health Check
- `GET /api/v1/health/`

## 7. Notes
- Business logic, authentication, models, and migrations for business entities are **NOT** implemented yet.
- This is a structural foundation.
