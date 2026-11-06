
PRAGMA foreign_keys = ON;

-- WYDARZENIA
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    location TEXT NOT NULL
);

-- MIEJSCA NA WYDARZENIACH
CREATE TABLE seats (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    row_label TEXT NOT NULL,
    number INTEGER NOT NULL CHECK (number > 0),

    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE (event_id, row_label, number)
);

-- UŻYTKOWNICY / KLIENCI
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- REZERWACJE
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'cancelled')),

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (seat_id) REFERENCES seats(id)
);

-- JEDNO MIEJSCE = MAKSYMALNIE JEDNA AKTYWNA REZERWACJA
CREATE UNIQUE INDEX unique_active_reservation
ON reservations(seat_id)
WHERE status = 'active';


