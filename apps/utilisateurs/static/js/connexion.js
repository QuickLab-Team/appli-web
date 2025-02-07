document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("forgotPasswordModal");
    var btn = document.getElementById("forgotPasswordLink");
    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function (event) {
        event.preventDefault();
        modal.style.display = "block";
    };

    span.onclick = function () {
        modal.style.display = "none";
    };

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});
