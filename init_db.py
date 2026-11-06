import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


DB_PATH = BASE_DIR / "booking.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


conn = sqlite3.connect(DB_PATH)

try:
    conn.execute("PRAGMA foreign_keys = ON")


    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema)

    conn.commit()


    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()

    print("Baza danych została utworzona!")
    print("Tabele:", tables)

finally:
    conn.close()
