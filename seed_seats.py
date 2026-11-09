import sqlite3

conn = sqlite3.connect("booking.db")

try:
    with conn:
        # Pobranie wszystkich wydarzeń
        events = conn.execute(
            "SELECT id FROM events"
        ).fetchall()

        # Tworzenie miejsc dla każdego wydarzenia
        for (event_id,) in events:
            for row_label in "ABC":
                for number in range(1, 7):
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO seats
                        (event_id, row_label, number)
                        VALUES (?, ?, ?)
                        """,
                        (event_id, row_label, number)
                    )

    print("Miejsca zostały przygotowane.")

finally:
    conn.close()
