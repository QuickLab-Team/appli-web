document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('input[name="quantite"]').addEventListener('input', function(){
        let quantite = parseFloat(this.value);
        let lien = document.querySelector('input[name="update-lien"]').value;
        let unite = document.querySelector('select[name="unite"]').value;

        if(!isNaN(quantite)){
            updateQuantite(quantite, unite, lien);
        }
    });

    document.querySelector('select[name="unite"]').addEventListener('change', function(){
        let quantite = parseFloat(document.querySelector('input[name="quantite"]').value);
        let lien = document.querySelector('input[name="update-lien"]').value;
        let unite = this.value;

        if(!isNaN(quantite)){
            updateQuantite(quantite, unite, lien);
        }
    });
});

function updateQuantite(quantite, unite, lien){
    $.ajax({
        url: lien,
        method: 'POST',
        data: {
            quantite: quantite,
            unite: unite
        },
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        },
    });
}