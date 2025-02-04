document.addEventListener("DOMContentLoaded", function () {
    function togglePopup(popupId, show) {
        const popup = document.getElementById(popupId);
        if (show) {
            popup.classList.remove("hidden");
            popup.style.display = "block";
        } else {
            popup.classList.add("hidden");
            popup.style.display = "none";
        }
    }

    // Gestion popup familles
    document.getElementById("familles-bouton").addEventListener("click", function () {
        togglePopup("popup-familles", true);
    });

    document.getElementById("annuler-bouton-familles").addEventListener("click", function () {
        togglePopup("popup-familles", false);
    });

    document.getElementById("confirmer-bouton").addEventListener("click", function () {
        let select = document.querySelector('select[name="filtre_famille"]');
        let famille = select.value;
        let url = produitsUrl;

        if (famille !== "0") {
            url += "?famille=" + famille;
        }

        window.location.href = url;
    });

    // Gestion popup services
    document.getElementById("services-bouton").addEventListener("click", function () {
        togglePopup("popup-services", true);
    });

    document.getElementById("annuler-bouton-services").addEventListener("click", function () {
        togglePopup("popup-services", false);
    });

    document.getElementById("confirmer-bouton-service").addEventListener("click", function () {
        let select = document.querySelector('select[name="filtre_service"]');
        let service = select.value;
        let url = produitsUrl; 

        if (service !== "0") {
            url += "?service=" + service;
        }

        window.location.href = url;
    });

    const menu = document.querySelector('.menu');
    const menuBurger = document.querySelector('.menu-burger');
    const closeMenu = document.querySelector('.close-menu');

    menu.style.position = 'absolute'; 
    menu.style.top = '0';
    menu.style.left = '0';
    menu.style.width = '100%';
    menu.style.height = '100%';
    menu.style.zIndex = '1000';
    menu.style.display = 'none';
    menu.style.backgroundColor = 'white';

    menuBurger.addEventListener('click', () => {
        menu.style.display = 'block';
    });

    closeMenu.addEventListener('click', () => {
        menu.style.display = 'none';
    });
});