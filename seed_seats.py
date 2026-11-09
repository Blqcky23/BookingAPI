import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "booking.db"

conn = sqlite3.connect(DB_PATH)

try:
    conn.execute("PRAGMA foreign_keys = ON")

    event_id = 1

    # Tworzymy 3 rzędy po 6 miejsc
    seats = []

    for row in ["A", "B", "C"]:
        for number in range(1, 7):
            seats.append((event_id, row, number))

    conn.executemany(
        """
        INSERT OR IGNORE INTO seats
        (event_id, row_label, number)
        VALUES (?, ?, ?)
        """,
        seats
    )

    conn.commit()
    print("Miejsca zostały dodane!")

finally:
    conn.close()
