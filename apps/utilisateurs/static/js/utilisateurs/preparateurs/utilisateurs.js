document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-supprimer-utilisateurs");
    const deleteButton = document.getElementById("btn-supprimer");
    const hiddenInput = document.getElementById("selected-utilisateurs");
    
    deleteButton.addEventListener("click", function (event) {
        event.preventDefault(); // Empêche le comportement par défaut

        // Récupère toutes les cases cochées
        const selectedCheckboxes = document.querySelectorAll('input[name="utilisateurs"]:checked');
        const selectedIds = Array.from(selectedCheckboxes).map(cb => cb.value);
        const count = selectedIds.length;

        if (count === 0) {
            Swal.fire({
                icon: "warning",
                title: "Aucune sélection",
                text: "Veuillez sélectionner au moins un utilisateur à supprimer.",
            });
            return;
        }

        // Confirmation avant suppression
        Swal.fire({
            title: `Êtes-vous sûr ?`,
            text: `Vous êtes sur le point de supprimer ${count} utilisateur(s).`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Oui, supprimer",
            cancelButtonText: "Annuler",
        }).then((result) => {
            if (result.isConfirmed) {
                // Envoyer les IDs sélectionnés via AJAX
                fetch(form.action, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": document.querySelector('[name="csrfmiddlewaretoken"]').value,
                    },
                    body: JSON.stringify({ utilisateurs: selectedIds }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire({
                                icon: "success",
                                title: "Succès",
                                text: data.message,
                            }).then(() => {
                                location.reload(); // Recharge la page
                            });
                        } else {
                            Swal.fire({
                                icon: "error",
                                title: "Erreur",
                                text: data.message,
                            });
                        }
                    })
                    .catch(error => {
                        Swal.fire({
                            icon: "error",
                            title: "Erreur",
                            text: "Une erreur est survenue. Veuillez réessayer.",
                        });
                    });
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const editButton = document.getElementById("btn-edit");
    const checkboxes = document.querySelectorAll('#form-supprimer-utilisateurs input[name="utilisateurs"]');

    // Gérer le clic sur le bouton d'édition
    editButton.addEventListener("click", function () {
        const selectedCheckboxes = Array.from(checkboxes).filter(cb => cb.checked);
        const count = selectedCheckboxes.length;

        if (count === 0) {
            Swal.fire({
                icon: 'warning',
                title: 'Aucune sélection',
                text: 'Veuillez sélectionner un utilisateur à modifier.',
            });
            return;
        }

        if (count > 1) {
            Swal.fire({
                icon: 'error',
                title: 'Trop de sélections',
                text: 'Vous ne pouvez modifier qu’un seul utilisateur à la fois.',
            });
            return;
        }

        // Récupérer l'ID de l'utilisateur sélectionné
        const userId = selectedCheckboxes[0].value;

        // Ouvrir une popup pour modifier l'utilisateur
        fetch(`/modifier/${userId}/`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message || "Une erreur est survenue.");
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: 'Modifier l’utilisateur',
                        html: `
                            <form id="edit-user-form">
                                <div class="form-group">
                                    <label>Nom</label>
                                    <input type="text" id="edit-nom" class="swal2-input" value="${data.nom}">
                                </div>
                                <div class="form-group">
                                    <label>Prénom</label>
                                    <input type="text" id="edit-prenom" class="swal2-input" value="${data.prenom}">
                                </div>
                                <div class="form-group">
                                    <label>Email</label>
                                    <input type="email" id="edit-email" class="swal2-input" value="${data.email}">
                                </div>
                                <div class="form-group">
                                    <label>Année</label>
                                    <input type="text" id="edit-annee" class="swal2-input" value="${data.annee}">
                                </div>
                                <div class="form-group">
                                    <label>Groupe</label>
                                    <input type="text" id="edit-groupe" class="swal2-input" value="${data.groupe}">
                                </div>
                            </form>
                        `,
                        showCancelButton: true,
                        confirmButtonText: 'Modifier',
                        cancelButtonText: 'Annuler',
                        preConfirm: () => {
                            return {
                                nom: document.getElementById('edit-nom').value,
                                prenom: document.getElementById('edit-prenom').value,
                                email: document.getElementById('edit-email').value,
                                annee: document.getElementById('edit-annee').value,
                                groupe: document.getElementById('edit-groupe').value,
                            };
                        }
                    }).then((result) => {
                        if (result.isConfirmed) {
                            // Envoyer les modifications au serveur
                            fetch(`/modifier/${userId}/`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                                },
                                body: JSON.stringify(result.value),
                            })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.success) {
                                        Swal.fire({
                                            icon: 'success',
                                            title: 'Succès',
                                            text: data.message,
                                        }).then(() => {
                                            location.reload(); // Recharger la page
                                        });
                                    } else {
                                        Swal.fire({
                                            icon: 'error',
                                            title: 'Erreur',
                                            text: data.message,
                                        });
                                    }
                                })
                                .catch(error => {
                                    Swal.fire({
                                        icon: 'error',
                                        title: 'Erreur',
                                        text: "Une erreur est survenue. Veuillez réessayer.",
                                    });
                                });
                        }
                    });
                }
            })
            .catch(error => {
                // Gérer les erreurs (autorisation ou autre)
                Swal.fire({
                    icon: 'error',
                    title: 'Erreur',
                    text: error.message,
                });
            });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById("select-all");

    function toggleCheckboxes(checked) {
        const checkboxes = document.querySelectorAll('input[name="utilisateurs"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = checked;
        });
    }

    function updateSelectAllState() {
        const checkboxes = document.querySelectorAll('input[name="utilisateurs"]');
        const allChecked = Array.from(checkboxes).every(cb => cb.checked); // Vérifie si tout est coché

        selectAllCheckbox.checked = allChecked;
    }


    selectAllCheckbox.addEventListener("change", function () {
        toggleCheckboxes(selectAllCheckbox.checked);
    });

    document.addEventListener("change", function (event) {
        if (event.target.name === "utilisateurs") {
            updateSelectAllState();
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const filters = document.querySelectorAll('input[name="q"], select[name="role"], select[name="annee"], select[name="groupe"]');
    
    filters.forEach(filter => {
        filter.addEventListener("input", function() {
            updateTable();
        });
    });

    function updateTable() {
        const query = document.querySelector('input[name="q"]').value;
        const role = document.querySelector('select[name="role"]').value;
        const annee = document.querySelector('select[name="annee"]').value;
        const groupe = document.querySelector('select[name="groupe"]').value;

        const params = new URLSearchParams({ q: query, role: role, annee: annee, groupe: groupe });

        fetch("?" + params.toString(), {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.json())
        .then(data => {
            document.querySelector("table.table-scroll tbody").innerHTML = data.html;
        })
        .catch(error => console.error("Erreur:", error));
    }
});