document.addEventListener("DOMContentLoaded", function() {
    const dataElement = document.getElementById("data-statistiques");
    if (!dataElement) {
        console.error("Erreur : L'élément contenant les statistiques n'existe pas !");
        return;
    }

    let data;
    try {
        data = JSON.parse(dataElement.textContent);
        console.log("Données récupérées :", data);
    } catch (error) {
        console.error("Erreur lors du parsing JSON :", error);
        return;
    }

    // Années spécifiques
    const allAnnees = ["1ère année", "2ème année", "3ème année"];

    // Graphique des connexions étudiantes
    const dataAujourdhui = allAnnees.map(annee => data.etudiants_connectes_aujourdhui[annee] || 0);
    const dataMois = allAnnees.map(annee => data.etudiants_connectes_mois[annee] || 0);

    const chartEtudiants = new Chart(document.getElementById("chartEtudiantsConnexions"), {
        type: "bar",
        data: {
            labels: allAnnees,
            datasets: [
                { label: "Aujourd'hui", data: dataAujourdhui, backgroundColor: "rgba(255, 99, 132, 0.5)", borderColor: "rgba(255, 99, 132, 1)", borderWidth: 1 },
                { label: "Ce mois", data: dataMois, backgroundColor: "rgba(54, 162, 235, 0.5)", borderColor: "rgba(54, 162, 235, 1)", borderWidth: 1 }
            ]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, stepSize: 1 } }
        }
    });

    // Graphique des réservations étudiantes
    const dataResAujourdhui = allAnnees.map(annee => data.reservations_etudiants_aujourdhui[annee] || 0);
    const dataResMois = allAnnees.map(annee => data.reservations_etudiants_mois[annee] || 0);

    const chartReservations = new Chart(document.getElementById("chartReservationsEtudiants"), {
        type: "bar",
        data: {
            labels: allAnnees,
            datasets: [
                { label: "Aujourd'hui", data: dataResAujourdhui, backgroundColor: "rgba(75, 192, 192, 0.5)", borderColor: "rgba(75, 192, 192, 1)", borderWidth: 1 },
                { label: "Ce mois", data: dataResMois, backgroundColor: "rgba(54, 162, 235, 0.5)", borderColor: "rgba(54, 162, 235, 1)", borderWidth: 1 }
            ]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, stepSize: 1 } }
        }
    });

    // Fonction pour modifier les graphiques (TEST)
    window.modifierGraphique = function() {
        chartEtudiants.data.datasets[0].data = allAnnees.map(() => Math.floor(Math.random() * 50));
        chartEtudiants.data.datasets[1].data = allAnnees.map(() => Math.floor(Math.random() * 100));
        chartEtudiants.update();
    };

    window.modifierGraphiqueReservations = function() {
        chartReservations.data.datasets[0].data = allAnnees.map(() => Math.floor(Math.random() * 50));
        chartReservations.data.datasets[1].data = allAnnees.map(() => Math.floor(Math.random() * 100));
        chartReservations.update();
    };
});
