
async function loadEvents() {
    const response = await fetch("/events");

    if (!response.ok) {
        throw new Error("Nie udało się pobrać wydarzeń");
    }

    const events = await response.json();
    const container = document.querySelector("#events");

    container.replaceChildren();

    events.forEach(event => {
        const button = document.createElement("button");
        button.textContent = event.name;

        button.addEventListener("click", () => {
            showMessage("");

            loadSeats(event.id).catch(error => {
                console.error(error);
                showMessage("Nie udało się pobrać miejsc", true);
            });
        });

        container.appendChild(button);
    });
}


async function loadSeats(eventId) {
    const response = await fetch(`/events/${eventId}/seats`);

    if (!response.ok) {
        throw new Error("Błąd pobierania miejsc");
    }

    const seats = await response.json();
    const container = document.querySelector("#seats");

    container.replaceChildren();

    seats.forEach(seat => {
        const button = document.createElement("button");

        if (seat.available) {
            button.textContent =
                `${seat.row_label}${seat.number} - wolne`;

            button.addEventListener("click", () => {
                reserveSeat(seat.id, eventId).catch(error => {
                    console.error(error);
                    showMessage("Błąd połączenia z serwerem", true);
                });
            });

        } else {
            button.textContent =
                `${seat.row_label}${seat.number} - zajęte`;

            button.disabled = true;
        }

        container.appendChild(button);
    });
}


async function reserveSeat(seatId, eventId) {
    const response = await fetch("/reservations", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: 1,
            seat_id: seatId
        })
    });

    if (response.status === 201) {
        showMessage("Rezerwacja zakończona sukcesem!");

        await loadSeats(eventId);

    } else if (response.status === 409) {
        showMessage("To miejsce jest już zajęte!", true);

        await loadSeats(eventId);

    } else if (response.status === 404) {
        showMessage("Nie znaleziono użytkownika lub miejsca", true);

    } else {
        showMessage(
            `Wystąpił błąd: ${response.status}`,
            true
        );
    }
}


function showMessage(text, isError = false) {
    const message = document.querySelector("#message");

    message.textContent = text;
    message.style.color = isError ? "red" : "green";
}


loadEvents().catch(error => {
    console.error(error);
    showMessage("Nie udało się załadować wydarzeń", true);
});
