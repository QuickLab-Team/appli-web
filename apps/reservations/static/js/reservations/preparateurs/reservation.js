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

document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('select[name="etat_reservation"').addEventListener('change', function(){
        let etat = this.value;
        let lien = document.querySelector('input[name="update_etat_reservation_lien"]').value;

        updateEtatReservation(etat, lien);
    })
});

function updateEtatReservation(etat, lien){
    $.ajax({
        url: lien,
        method: 'POST',
        data: {
            etat: etat,
        },
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        },
    });
}