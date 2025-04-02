document.addEventListener("DOMContentLoaded", function () {
    const medicalRecordsModal = document.getElementById("medicalRecordsModal");

    if (medicalRecordsModal) {
        medicalRecordsModal.addEventListener("show.bs.modal", function () {
            console.log("Modal opened. Fetching data...");

            fetch("/get/medical/records/")
                .then(response => response.json())
                .then(data => {
                    console.log("Fetched data:", data);  // Debugging
                    const list = document.getElementById("medicalRecordsList");
                    list.innerHTML = ""; // Clear previous data

                    if (data.records && data.records.length > 0) {
                        data.records.forEach(record => {
                            const li = document.createElement("li");
                            li.textContent = `${record.condition} - ${record.diagnosis_date || "N/A"} (Notes: ${record.notes || "No Notes"})`;
                            list.appendChild(li);
                        });
                    } else {
                        list.innerHTML = "<li>No medical records found.</li>";
                    }
                })
                .catch(error => console.error("Error fetching medical records:", error));
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("bookAppointmentBtn").addEventListener("click", function () {
        window.location.href = "/book/appointment/";
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("GetAppointment").addEventListener("click", function () {
        window.location.href = "/get/appointments/";
    });
});

