function updateFileName() {
    const fileInput = document.getElementById('file_input');
    const fileNameSpan = document.getElementById('file_name');
    fileNameSpan.textContent = fileInput.files[0].name;
}

function openServicePopup() {
    document.getElementById('servicePopup').style.display = 'block';
}

function closeServicePopup() {
    document.getElementById('servicePopup').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-service-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const newServiceName = document.getElementById('new_service_name').value;

        fetch(addServiceUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ name: newServiceName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                closeServicePopup();
                location.reload();
            } else {
                alert('Erreur: ' + data.error);
            }
        });
    });
});