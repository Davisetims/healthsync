document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("prescriptionbtn").addEventListener("click", function () {
        window.location.href = "/post/prescription/";
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("GetAppointment").addEventListener("click", function () {
        window.location.href = "/get/appointments/";
    });
});
