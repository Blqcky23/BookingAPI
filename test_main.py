import sqlite3
from pathlib import Path

import pytest
import main
from fastapi.testclient import TestClient



@pytest.fixture
def test_client(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"

    # Podmieniamy ścieżkę bazy w naszej aplikacji
    monkeypatch.setattr(main, "DB_PATH", str(test_db))

    # Tworzymy tabele na podstawie schema.sql
    schema = Path(__file__).with_name("schema.sql").read_text(
        encoding="utf-8"
    )

    with sqlite3.connect(test_db) as conn:
        conn.executescript(schema)

        # Przykładowy użytkownik
        conn.execute(
            """
            INSERT INTO users (id, first_name, last_name, email)
            VALUES (1, 'Jan', 'Kowalski', 'jan@test.pl')
            """
        )

        # Przykładowe wydarzenie
        conn.execute(
            """
            INSERT INTO events (id, name, date, time, location)
            VALUES (1, 'Koncert', '2026-12-10', '19:00', 'Kraków')
            """
        )

        # Przykładowe miejsce
        conn.execute(
            """
            INSERT INTO seats (id, event_id, row_label, number)
            VALUES (1, 1, 'A', 1)
            """
        )

        conn.commit()

    return TestClient(main.app)


def test_invalid_user_id(test_client):
    response = test_client.post(
        "/reservations",
        json={
            "user_id": "abc",
            "seat_id": 8
        }
    )

    assert response.status_code == 422


def test_create_reservation(test_client):
    response = test_client.post(
        "/reservations",
        json={
            "user_id":1,
            "seat_id":1
        }
    )
    assert response.status_code == 201

    response_duplicate = test_client.post(
        "/reservations",
        json={
            "user_id": 1,
            "seat_id": 1
        }
    )

    assert response_duplicate.status_code == 409

def test_cancel_reservation(test_client):
    response = test_client.post(
        "/reservations",
        json={
            "user_id":1,
            "seat_id":1
        }
    )
    assert response.status_code == 201

    reservation_id = response.json()["reservation_id"]
    response_delete = test_client.delete(
        f"/reservations/{reservation_id}")

    assert response_delete.status_code == 200

    response_seats = test_client.get("events/1/seats")

    assert response_seats.status_code == 200

    print(response_seats.json())

    assert response_seats.json()[0]["available"] is True

    response_again = test_client.post(
        "/reservations",
        json={
            "user_id": 1,
            "seat_id": 1
        }
    )

    assert response_again.status_code == 201