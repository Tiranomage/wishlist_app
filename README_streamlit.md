# Wishlist App - Streamlit Frontend

This is a Streamlit-based frontend for the Wishlist application. It provides a user-friendly interface to manage wishlists and gifts.

## Features

- User registration and login
- Create, edit, and delete wishlists
- Add, edit, and delete gifts within wishlists
- Public wishlists with share tokens
- Session management with JWT tokens

## Requirements

- Python 3.8+
- Streamlit
- Requests

## Setup and Installation

1. Install the required packages:
```bash
pip install -r requirements_streamlit.txt
```

2. Make sure the backend server is running on `http://localhost:8000`:
```bash
cd backend
pip install -r requirements.txt
python main.py
```

3. Run the Streamlit app:
```bash
streamlit run streamlit_frontend.py
```

## Running with Docker (Alternative)

If you prefer using Docker, you can use the existing docker-compose setup:

```bash
docker-compose up --build
```

The Streamlit app will be available at `http://localhost:8501`

## Usage

1. Open your browser and navigate to the Streamlit app URL
2. Register for a new account or log in with existing credentials
3. Create wishlists and add gifts to them
4. Manage your wishlists and gifts using the intuitive interface

## Authentication

The app handles authentication automatically:
- Login credentials are sent to the backend
- JWT tokens are stored in session state
- All subsequent API calls include the authorization header
- Session is cleared on logout

## API Integration

The frontend communicates with the backend API at `http://localhost:8000/api` using standard HTTP methods (GET, POST, PUT, DELETE) with proper authentication headers.