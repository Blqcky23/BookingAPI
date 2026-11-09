import sqlite3

conn = sqlite3.connect("booking.db")

try:
    with conn:
        # Dodawanie wydarzeń
        events = [
            (1, "Koncert Rockowy", "2026-11-20", "19:30", "Kraków"),
            (2, "Stand-up", "2026-11-22", "20:00", "Warszawa"),
            (3, "Festiwal Muzyczny", "2026-12-05", "18:00", "Wrocław")
        ]

        conn.executemany(
            """
            INSERT OR IGNORE INTO events
            (id, name, date, time, location)
            VALUES (?, ?, ?, ?, ?)
            """,
            events
        )

        # Dodawanie użytkownika demonstracyjnego
        conn.execute(
            """
            INSERT OR IGNORE INTO users
            (id, first_name, last_name, email)
            VALUES (?, ?, ?, ?)
            """,
            (1, "Jan", "Kowalski", "jan@example.com")
        )

    print("Wydarzenia i użytkownik zostali przygotowani.")

finally:
    conn.close()
