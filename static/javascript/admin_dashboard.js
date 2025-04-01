// Initialize with data
document.addEventListener('DOMContentLoaded', function() {
    // Initialize statistics
    updateStatCounts();
    
    // Set up buttons and interactive elements
    setupButtons();
});

function updateStatCounts() {
    // Get statistics elements
    let doctorsCount = document.getElementById('doctors-count');
    let patientsCount = document.getElementById('patients-count');
    let nursesCount = document.getElementById('nurses-count');
    let appointmentsCount = document.getElementById('appointments-count');
    let messagesCount = document.getElementById('messages-count');
    
    // Initial values
    let doctors = 24;
    let patients = 653;
    let nurses = 42;
    let appointments = 98;
    let messages = 35;
    
    // Update display
    doctorsCount.textContent = doctors;
    patientsCount.textContent = patients;
    nursesCount.textContent = nurses;
    appointmentsCount.textContent = appointments;
    messagesCount.textContent = messages;
    
    // Simulate live updates every 30 seconds
    setInterval(() => {
        // Small random changes to simulate live data
        doctors = Math.max(20, doctors + (Math.random() > 0.7 ? Math.floor(Math.random() * 3) - 1 : 0));
        patients = patients + Math.floor(Math.random() * 5) - 1;
        nurses = Math.max(35, nurses + (Math.random() > 0.8 ? Math.floor(Math.random() * 2) - 1 : 0));
        appointments = Math.max(50, appointments + Math.floor(Math.random() * 4) - 1);
        messages = Math.max(10, messages + Math.floor(Math.random() * 3) - 1);
        
        // Update with animation
        animateCounter(doctorsCount, doctorsCount.textContent, doctors);
        animateCounter(patientsCount, patientsCount.textContent, patients);
        animateCounter(nursesCount, nursesCount.textContent, nurses);
        animateCounter(appointmentsCount, appointmentsCount.textContent, appointments);
        animateCounter(messagesCount, messagesCount.textContent, messages);
    }, 30000);
}

function animateCounter(element, start, end) {
    let startNum = parseInt(start);
    let endNum = parseInt(end);
    let duration = 1000; // 1 second
    let startTime = null;
    
    function animate(currentTime) {
        if (!startTime) startTime = currentTime;
        let timeElapsed = currentTime - startTime;
        let progress = Math.min(timeElapsed / duration, 1);
        
        let currentValue = Math.floor(startNum + (endNum - startNum) * progress);
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

function setupButtons() {
    // Setup for Reschedule and Cancel buttons
    const rescheduleButtons = document.querySelectorAll('.btn-reschedule');
    const cancelButtons = document.querySelectorAll('.btn-cancel');
    
    rescheduleButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Appointment rescheduling system will open');
        });
    });
    
    cancelButtons.forEach(button => {
        button.addEventListener('click', function() {
            const appointment = this.closest('.appointment');
            if (confirm('Are you sure you want to cancel this appointment?')) {
                appointment.style.opacity = '0.5';
                setTimeout(() => {
                    appointment.style.display = 'none';
                    // Update appointment count
                    let appointmentsCount = document.getElementById('appointments-count');
                    let currentCount = parseInt(appointmentsCount.textContent);
                    appointmentsCount.textContent = currentCount - 1;
                }, 1000);
            }
        });
    });
    
    // Setup for Quick action cards
    const actionCards = document.querySelectorAll('.action-card');
    
    actionCards.forEach(card => {
        card.addEventListener('click', function() {
            const action = this.querySelector('p').textContent;
            alert(`${action} system will open`);
        });
    });
    
    // Setup for Menu items
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (!this.classList.contains('active') && !this.classList.contains('logout')) {
                e.preventDefault();
                document.querySelector('.menu-item.active').classList.remove('active');
                this.classList.add('active');
                alert(`Navigating to ${this.querySelector('span').textContent}`);
            }
            
            if (this.classList.contains('logout')) {
                e.preventDefault();
                if (confirm('Are you sure you want to logout?')) {
                    alert('Logging out...');
                }
            }
        });
    });
}

// Add event listeners for search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-bar input');
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            alert(`Searching for: ${this.value}`);
            this.value = '';
        }
    });
});