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
5. Set up environment variables (see `.env.example`)
6. Run database migrations: `alembic upgrade head`

## Running the Application

1. Start the backend server: `uvicorn main:app --reload`
2. In another terminal, start the Streamlit frontend: `streamlit run streamlit_frontend.py`
3. Access the application at `http://localhost:8501`

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


## Docker Deployment

To run the entire application using Docker:

```bash
docker-compose up --build
```

The backend will be available at `http://localhost:8000` and the Streamlit frontend at `http://localhost:8501`.
