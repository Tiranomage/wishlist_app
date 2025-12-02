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

## Architecture & Compatibility

### Backend (FastAPI)
- Built with FastAPI, SQLAlchemy, and PostgreSQL
- Handles all API requests and database operations
- Provides authentication, wishlist, and gift management endpoints
- Supports CORS for frontend communication

### Frontend (Vanilla JavaScript/TypeScript)
- Uses vanilla JavaScript with TypeScript compilation
- Communicates with backend via `/api` endpoints
- Implements authentication, dashboard, and public wishlist browsing
- Uses localStorage for token management

### Docker Integration
- Both backend and frontend are containerized
- Nginx reverse proxy handles API request routing
- PostgreSQL database and pgAdmin for database management
- Proper service dependencies ensure correct startup order

## Quickstart

### Prerequisites
- Docker and Docker Compose

### Running the Application
1. Start services:
```bash
docker compose up -d --build
```

2. Apply DB migrations (inside backend container):
```bash
docker compose exec backend alembic upgrade head
```

3. Open API docs: http://localhost:8000/docs

4. Access frontend: http://localhost:3000

## Environment Variables

### Backend
The backend reads settings from environment variables (see `backend/config.py`):
- `DATABASE_URL` (default: postgresql+psycopg://postgres:postgres@db:5432/wishlist)
- `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY`
- `RATE_LIMIT_PER_MINUTE` (default: 100)
- `BACKEND_CORS_ORIGINS`

### Frontend
The frontend is configured to communicate with the backend via API proxying through nginx.

## Common API Flows
- Register: POST /auth/register
- Login: POST /auth/login
- Password reset request: POST /auth/password-reset (token prints to backend logs)
- Password reset confirm: POST /auth/password-reset/confirm
- Wishlists: GET/POST /wishlists (use `public=true` to browse)
- Gifts: POST /gifts/wishlist/{id}, PATCH /gifts/{id}, DELETE /gifts/{id}

## Development

### Local Development
Install dependencies if running locally:
```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Run tests:
```bash
pytest -q
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## Docker Compose Services

- **db**: PostgreSQL database container
- **pgadmin**: Database management interface (http://localhost:5050)
- **backend**: FastAPI application (http://localhost:8000)
- **frontend**: Nginx server serving the frontend (http://localhost:3000)

The nginx configuration in the frontend container proxies `/api` requests to the backend service.

## Postman
Import `postman_collection.json` and run the requests. The login request saves tokens to collection variables used by subsequent calls.

## Notes
- Public wishlists are visible to all authenticated users. Extend as needed for unauthenticated browse.
- Frontend uses localStorage for tokens. For production, migrate to HttpOnly cookies.
- The application is fully containerized and designed for production deployment.

