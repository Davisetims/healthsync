// JavaScript for handling patient list interactions
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('patientSearch');
    searchInput.addEventListener('input', function() {
        filterPatients();
    });

    // Filter type change
    const filterType = document.getElementById('filterType');
    filterType.addEventListener('change', function() {
        filterPatients();
    });

    // View patient details
    const viewButtons = document.querySelectorAll('.view-btn');
    viewButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const patientId = this.getAttribute('data-id');
            openPatientModal(patientId);
        });
    });

    // Row click to view patient
    const patientRows = document.querySelectorAll('.patient-row');
    patientRows.forEach(row => {
        row.addEventListener('click', function() {
            const patientId = this.getAttribute('data-id');
            openPatientModal(patientId);
        });
    });

    // Edit patient
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const patientId = this.getAttribute('data-id');
            window.location.href = `/patients/edit/${patientId}/`;
        });
    });

    // Delete patient
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const patientId = this.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this patient?')) {
                // Send delete request to server
                deletePatient(patientId);
            }
        });
    });

    // Close modal
    const closeBtn = document.querySelector('.close-btn');
    closeBtn.addEventListener('click', function() {
        document.getElementById('patientModal').style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        const modal = document.getElementById('patientModal');
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Pagination (basic implementation)
    document.getElementById('prevPage').addEventListener('click', function() {
        // Handle previous page
        console.log('Previous page');
    });

    document.getElementById('nextPage').addEventListener('click', function() {
        // Handle next page
        console.log('Next page');
    });
});

// Filter patients based on search and filter type
function filterPatients() {
    const searchValue = document.getElementById('patientSearch').value.toLowerCase();
    const filterValue = document.getElementById('filterType').value;
    const rows = document.querySelectorAll('.patient-row');

    rows.forEach(row => {
        const name = row.children[1].textContent.toLowerCase();
        const email = row.children[2].textContent.toLowerCase();
        const matchesSearch = name.includes(searchValue) || email.includes(searchValue);
        
        // Apply filter logic (this would need to be expanded based on your actual data)
        let matchesFilter = true;
        if (filterValue === 'recent') {
            // Add logic for filtering recently added patients
        } else if (filterValue === 'upcoming') {
            // Add logic for filtering patients with upcoming appointments
        }

        if (matchesSearch && matchesFilter) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Open patient detail modal
function openPatientModal(patientId) {
    // In a real application, you would fetch patient details from the server
    // For this example, we'll simulate it with existing data
    const modal = document.getElementById('patientModal');
    const patientDetails = document.getElementById('patientDetails');
    
    // Find the patient row
    const patientRow = document.querySelector(`.patient-row[data-id="${patientId}"]`);
    if (patientRow) {
        const id = patientRow.children[0].textContent;
        const name = patientRow.children[1].textContent;
        const email = patientRow.children[2].textContent;
        const country = patientRow.children[3].textContent;
        const city = patientRow.children[4].textContent;
        
        // Create patient details HTML
        patientDetails.innerHTML = `
            <dl>
                <dt>No:</dt>
                <dd>${id}</dd>
                
                <dt>Name:</dt>
                <dd>${name}</dd>
                
                <dt>Email:</dt>
                <dd>${email}</dd>
                
                <dt>Country:</dt>
                <dd>${country}</dd>
                
                <dt>City:</dt>
                <dd>${city}</dd>
            </dl>
            <div class="modal-actions">
               
                <button class="view-btn" onclick="window.location.href='/patients/${patientId}/appointments/'">View Appointments</button>
            </div>
        `;
    } else {
        patientDetails.innerHTML = '<p>Patient not found.</p>';
    }
    
    modal.style.display = 'block';
}

// Delete patient function
function deletePatient(patientId) {
    // In a real application, you would make an AJAX request to delete the patient
    // For this example, we'll simulate it
    console.log(`Deleting patient with ID: ${patientId}`);
    
    // After successful deletion, you would typically refresh the patient list
    // For now, let's just hide the row
    const patientRow = document.querySelector(`.patient-row[data-id="${patientId}"]`);
    if (patientRow) {
        patientRow.style.display = 'none';
    }
}