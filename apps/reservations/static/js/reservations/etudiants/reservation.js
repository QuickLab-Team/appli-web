function ouvrirMessagerie(){
    let messagerie = document.querySelector(".messagerie");
    messagerie.style.display = "flex";

    let reservation_detail = document.querySelector(".reservation-detail");
    reservation_detail.style.display = "none";
}

function fermerMessagerie(){
    let messagerie = document.querySelector(".messagerie");
    messagerie.style.display = "none";

    let reservation_detail = document.querySelector(".reservation-detail");
    reservation_detail.style.display = "block";
}

function envoyerMessage(){
    let message = document.querySelector("input[name='message'").value;
    if(message != ""){
        document.querySelector("input[name='message'").value = "";

        let lien = document.querySelector('input[name="ajouter_message_reservation_lien"]').value;
        $.ajax({
            url: lien,
            method: 'POST',
            async: false,
            data: {
                message: message,
            },
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
        });

        window.location.reload();
    }
}