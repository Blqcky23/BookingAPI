from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from pathlib import Path
app = FastAPI()

DB_PATH = Path(__file__).resolve().parent / "booking.db"
class ReservationCreate(BaseModel):
    user_id: int
    seat_id: int

@app.get("/")
def home():
    return {"message": "Witaj w Booking API!"}


@app.get("/events")
def get_events():
    conn = sqlite3.connect(DB_PATH)

    try:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")

        cursor = conn.execute(
            "SELECT id, name, date, time, location FROM events"
        )

        events = cursor.fetchall()

        return [dict(event) for event in events]

    finally:
        conn.close()



@app.get("/events/{event_id}/seats")
def get_seats(event_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        # Sprawdzamy, czy wydarzenie istnieje
        event = conn.execute(
            "SELECT id FROM events WHERE id = ?",
            (event_id,)
        ).fetchone()

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Wydarzenie nie istnieje"
            )

        # Pobieramy miejsca i ich dostępność
        cursor = conn.execute(
            """
            SELECT
                s.id,
                s.row_label,
                s.number,
                NOT EXISTS (
                    SELECT 1
                    FROM reservations r
                    WHERE r.seat_id = s.id
                    AND r.status = 'active'
                ) AS available
            FROM seats s
            WHERE s.event_id = ?
            ORDER BY s.row_label, s.number
            """,
            (event_id,)
        )

        seats = []

        for seat in cursor.fetchall():
            item = dict(seat)
            item["available"] = bool(item["available"])
            seats.append(item)

        return seats

    finally:
        conn.close()



@app.post("/reservations", status_code=201)
def create_reservation(data: ReservationCreate):
    conn = sqlite3.connect(DB_PATH)


    try:
        conn.execute("PRAGMA foreign_keys = ON")
        user = conn.execute(
            "SELECT id FROM users WHERE id = ?",
            (data.user_id,)
        ).fetchone()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Użytkownik nie istnieje"
            )

        seat = conn.execute(
            "SELECT id FROM seats WHERE id = ?",
            (data.seat_id,)
        ).fetchone()

        if seat is None:
            raise HTTPException(
                status_code=404,
                detail="Miejsce nie istnieje"
            )



        # 1. Wykonaj INSERT INTO reservations
        cursor = conn.execute("INSERT INTO reservations (user_id,seat_id) VALUES (?,?)",
                              (data.user_id,data.seat_id))

        conn.commit()
        reservation_id = cursor.lastrowid
        return {
            "message": "Reservation created successfully",
            "reservation_id": reservation_id
        }


    except sqlite3.IntegrityError as error:
        conn.rollback()

        if str(error) == "UNIQUE constraint failed: reservations.seat_id":
            raise HTTPException(
                status_code=409,
                detail="To miejsce jest już zarezerwowane"
            )

        raise


    finally:
        conn.close()



@app.delete("/reservations/{reservation_id}")
def cancel_reservation(reservation_id: int):
    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.execute(
            """
            UPDATE reservations
            SET status = 'cancelled'
            WHERE id = ? AND status = 'active'
            """,
            (reservation_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Nie znaleziono aktywnej rezerwacji"
            )

        conn.commit()

        return {
            "message": "Reservation cancelled successfully",
            "reservation_id": reservation_id
        }

    finally:
        conn.close()
