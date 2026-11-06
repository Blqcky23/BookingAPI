import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "booking.db"

conn = sqlite3.connect(DB_PATH)

try:
    conn.execute(
        "DELETE FROM events WHERE id > ?",
        (3,)
    )
    conn.commit()

    print("Usunięto dodatkowe wydarzenia!")

finally:
    conn.close()