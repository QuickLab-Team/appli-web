document.addEventListener('DOMContentLoaded', function(){
    let quantiteElem = document.querySelector('input[name="quantite"]');
    if(quantiteElem){
        quantiteElem.addEventListener('input', function(){
            let quantite = parseFloat(this.value);
            let lien = document.querySelector('input[name="update-lien"]').value;
            let unite = document.querySelector('select[name="unite"]').value;
    
            if(!isNaN(quantite)){
                updateQuantite(quantite, unite, lien);
            }
        });
    }

    let uniteElem = document.querySelector('select[name="unite"]');
    if(uniteElem){
        uniteElem.addEventListener('change', function(){
            let quantite = parseFloat(document.querySelector('input[name="quantite"]').value);
            let lien = document.querySelector('input[name="update-lien"]').value;
            let unite = this.value;
    
            if(!isNaN(quantite)){
                updateQuantite(quantite, unite, lien);
            }
        });
    }
});

function updateQuantite(quantite, unite, lien){
    $.ajax({
        url: lien,
        method: 'POST',
        data: {
            quantite: quantite,
            unite: unite,
            produit_id: document.querySelector('input[name="produit_id"]').value
        },
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        },
    });
}