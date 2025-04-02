document.addEventListener("DOMContentLoaded", function () {
    // Initialize modal
    const prescriptionModal = new bootstrap.Modal(document.getElementById('prescriptionModal'));
    
    // Form submission handler
    const prescriptionForm = document.getElementById("prescriptionForm");
    if (prescriptionForm) {
        prescriptionForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const prescriptionData = {
                patient: document.getElementById("patient").value,
                name: document.getElementById("name").value,
                dosage: document.getElementById("dosage").value,
                frequency: document.getElementById("frequency").value,
                start_date: document.getElementById("start_date").value,
                end_date: document.getElementById("end_date").value,
            };

            fetch("/post/prescription/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify(prescriptionData),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                alert("Prescription added successfully!");
                prescriptionForm.reset();
                prescriptionModal.hide();
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error submitting prescription: " + error.message);
            });
        });
    }

    // Fetch patients and populate dropdown
function loadPatients() {
    fetch("/get/users/?user_type=patient")
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const patientSelect = document.getElementById("patient");
            patientSelect.innerHTML = '<option value="">Select a patient</option>';

            if (data.users && data.users.length > 0) {  // Use 'users' instead of 'patients'
                data.users.forEach(patient => {
                    const option = document.createElement("option");
                    option.value = patient.id;
                    option.textContent = patient.first_name ? `${patient.first_name} ${patient.last_name || ''}`.trim() : patient.email;
                    patientSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error("Error fetching patients:", error);
            document.getElementById("patient").innerHTML = '<option value="">Error loading patients</option>';
        });
}

// Load patients when modal is shown
document.getElementById('prescriptionModal').addEventListener('show.bs.modal', loadPatients);

    // Load patients when modal is shown
    document.getElementById('prescriptionModal').addEventListener('show.bs.modal', loadPatients);

    // CSRF token function
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

