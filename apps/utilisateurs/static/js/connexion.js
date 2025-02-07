document.addEventListener("DOMContentLoaded", function () {
    const forgotPasswordLink = document.getElementById("forgotPasswordLink");
    const passwordResetPopup = document.getElementById("passwordResetPopup");
    const closePopup = document.getElementById("closePopup");
    const passwordResetForm = document.getElementById("passwordResetForm");
    const popupMessage = document.getElementById("popupMessage");
    // Ouvrir la popup
    forgotPasswordLink.addEventListener("click", function (e) {
        e.preventDefault();
        passwordResetPopup.classList.remove("hidden");
    });
    // Fermer la popup
    closePopup.addEventListener("click", function () {
        passwordResetPopup.classList.add("hidden");
        popupMessage.classList.add("hidden");
    });
    
    passwordResetForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(passwordResetForm);
        fetch(passwordResetForm.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
            body: formData,
        })
        .then((response) => {
            if (response.ok) {
                popupMessage.textContent =
                    "Un email de réinitialisation a été envoyé si l'adresse est valide.";
                popupMessage.classList.remove("hidden");
                passwordResetForm.reset();
            } else {
                popupMessage.textContent =
                    "Une erreur s'est produite. Veuillez réessayer.";
                popupMessage.classList.remove("hidden");
            }
        })
        .catch((error) => {
            console.error("Erreur :", error);
            popupMessage.textContent =
                "Une erreur s'est produite. Veuillez réessayer.";
            popupMessage.classList.remove("hidden");
        });
    });
});