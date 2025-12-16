# Wishlist Management Application

A complete wishlist management application with user authentication, wishlist creation, and gift tracking. Features a Streamlit frontend for easier development and deployment.

## Features

- User registration and authentication (JWT)
- Wishlist management
- Gift management within wishlists
- Role-based access control
- Database models with relationships
- Pydantic schemas for data validation
- Streamlit-based web interface

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (see example below)
6. Run database migrations: `cd backend && alembic upgrade head`

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_REFRESH_SECRET_KEY=your_refresh_secret_key_here
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/wishlist
ENVIRONMENT=development
BACKEND_CORS_ORIGINS=http://localhost,http://localhost:3000,http://127.0.0.1,http://127.0.0.1:3000
```

For development without PostgreSQL, you can use SQLite instead:
```bash
DATABASE_URL=sqlite:///./wishlist.db
```

## Running the Application

### Option 1: Using the startup script (recommended)
1. Make sure you've installed the requirements and set up environment variables
2. Run: `python start_app.py`
3. Access the application at `http://localhost:8501`

### Option 2: Manual startup
1. Open two terminals
2. In the first terminal (from the backend directory): `cd backend && uvicorn main:app --reload`
3. In the second terminal (from the root directory): `streamlit run streamlit_frontend.py`
4. Access the application at `http://localhost:8501`

## Usage

1. Register a new account or log in with existing credentials
2. Create wishlists to organize your items
3. Add gifts to your wishlists with descriptions and links
4. Mark gifts as purchased or update their status
5. Manage your wishlists by editing or deleting them

## API Endpoints

- `/auth/register` - Register a new user
- `/auth/login` - Login and get JWT token
- `/wishlists/` - Get all user's wishlists
- `/wishlists/{wishlist_id}` - Get a specific wishlist
- `/wishlists/create` - Create a new wishlist
- `/wishlists/{wishlist_id}/update` - Update a wishlist
- `/wishlists/{wishlist_id}/delete` - Delete a wishlist
- `/gifts/{wishlist_id}/add_gift` - Add a gift to a wishlist
- `/gifts/{gift_id}/update` - Update a gift
- `/gifts/{gift_id}/delete` - Delete a gift
