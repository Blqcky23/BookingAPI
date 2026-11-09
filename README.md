
# Booking API

A simple event ticket reservation application built with
Python, FastAPI, SQLite, and vanilla JavaScript.

The project demonstrates REST API development, database
constraints, automated testing, and frontend-backend
communication.

## Features

- Browse available events
- Display seats and their availability
- Create ticket reservations
- Prevent double-booking of seats
- Cancel reservations while preserving their history
- Display reservation results and errors
- Automatically refresh seat availability

## Tech Stack

**Backend:** Python, FastAPI, SQLite, Pydantic

**Frontend:** HTML, CSS, JavaScript

**Testing:** pytest, FastAPI TestClient, HTTPX

**Version Control:** Git, GitHub

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /events | List all events |
| GET | /events/{event_id}/seats | List event seats and availability |
| POST | /reservations | Create a reservation |
| DELETE | /reservations/{reservation_id} | Cancel a reservation |

## Database Design

The SQLite database contains four tables:

- `users` — registered users
- `events` — available events
- `seats` — seats assigned to events
- `reservations` — active and cancelled reservations

A partial UNIQUE index prevents multiple active reservations
for the same seat.

Cancelled reservations remain in the database to preserve
reservation history.

## Running Locally

Requires Python 3.13.

### 1. Clone the repository

    git clone https://github.com/Blqcky23/BookingAPI.git
    cd BookingAPI

### 2. Create a virtual environment

    python -m venv .venv

Activate it in Windows PowerShell:

    .venv\Scripts\Activate.ps1

### 3. Install dependencies

    python -m pip install -r requirements.txt

### 4. Initialize the database

    python init_db.py
    python seed.py
    python seed_seats.py

### 5. Start the application

    python -m uvicorn main:app --reload

Open:

- Application: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs

## Running Tests

    python -m pytest -v

Automated tests cover:

- Request validation
- Successful reservation creation
- Double-booking prevention
- Reservation cancellation
- Seat availability after cancellation

Tests use temporary SQLite databases to avoid modifying
the application's normal database.

## Limitations

This is a demonstration project, not a production-ready
ticketing platform.

- Authentication is not implemented.
- The frontend uses a hardcoded demo user (`user_id = 1`).
- Cancellation is available through the REST API,
  but not through a dedicated frontend interface.
- Payments and user account management are not implemented.


