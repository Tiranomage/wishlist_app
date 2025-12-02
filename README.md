# Wishlist App

Production-ready wishlist application built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, and a vanilla JS frontend.

## Features
- Email/password auth with bcrypt-hashed passwords
- JWT access/refresh tokens
- Password reset (token printed to console)
- CRUD wishlists and gifts, ownership checks, public/private toggle
- Search wishlists by title or gift name
- Rate limiting (default 100 req/min)
- Dockerized stack with PostgreSQL and pgAdmin

## Quickstart
1. Prerequisites: Docker, Docker Compose
2. Start services:
```bash
docker compose up -d --build
```
3. Apply DB migrations (inside backend container):
```bash
docker compose exec backend alembic upgrade head
```
4. Open API docs: http://localhost:8000/docs
5. Open frontend: open `frontend/index.html` in your browser

## Environment
The backend reads settings from env variables (see `backend/config.py`):
- DATABASE_URL (default: postgresql+psycopg2://postgres:postgres@db:5432/wishlist)
- JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY
- RATE_LIMIT_PER_MINUTE (default: 100)
- BACKEND_CORS_ORIGINS

## Common API Flows
- Register: POST /auth/register
- Login: POST /auth/login
- Password reset request: POST /auth/password-reset (token prints to backend logs)
- Password reset confirm: POST /auth/password-reset/confirm
- Wishlists: GET/POST /wishlists (use `public=true` to browse)
- Gifts: POST /gifts/wishlist/{id}, PATCH /gifts/{id}, DELETE /gifts/{id}

## Development
Install dependencies if running locally:
```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
Run tests:
```bash
pytest -q
```

## Postman
Import `postman_collection.json` and run the requests. The login request saves tokens to collection variables used by subsequent calls.

## Notes
- Public wishlists are visible to all authenticated users. Extend as needed for unauthenticated browse.
- Frontend uses localStorage for tokens. For production, migrate to HttpOnly cookies.

