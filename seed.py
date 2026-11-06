
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "booking.db"

conn = sqlite3.connect(DB_PATH)

try:
    events = [
        ("Koncert Rockowy", "2026-11-20", "19:30", "Kraków"),
        ("Stand-up", "2026-11-22", "20:00", "Warszawa"),
        ("Festiwal Muzyczny", "2026-12-05", "18:00", "Wrocław")
    ]

    conn.executemany(
        """
        INSERT INTO events (name, date, time, location)
        VALUES (?, ?, ?, ?)
        """,
        events
    )

    conn.commit()
    print("Dodano 3 wydarzenia!")

finally:
    conn.close()
