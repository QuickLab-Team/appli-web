function ouvrirMessagerie() {
    let messagerie = document.querySelector(".messagerie");
    messagerie.classList.add("active");

    document.querySelector(".messagerie-overlay").classList.add("active");

    let reservationDetail = document.querySelector(".reservation-detail");
    if (reservationDetail) {
        reservationDetail.style.display = "none";
    }
}

function fermerMessagerie() {
    let messagerie = document.querySelector(".messagerie");
    messagerie.classList.remove("active");

    document.querySelector(".messagerie-overlay").classList.remove("active");

    let reservationDetail = document.querySelector(".reservation-detail");
    if (reservationDetail) {
        reservationDetail.style.display = "block";
    }
}

function envoyerMessage() {
    let message = document.querySelector("input[name='message']").value;
    if (message !== "") {
        document.querySelector("input[name='message']").value = "";

        let lien = document.querySelector('input[name="ajouter_message_reservation_lien"]').value;
        $.ajax({
            url: lien,
            method: "POST",
            async: false,
            data: {
                message: message,
            },
            headers: {
                "X-CSRFToken": document.querySelector('input[name="csrf_token"]').value,
            },
        });
        window.location.reload();
    }
}
