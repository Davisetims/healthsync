document.addEventListener('DOMContentLoaded', function() {
    // FAQ Toggle
    const faqToggles = document.querySelectorAll('.faq-toggle');
    faqToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const faqItem = this.closest('.faq-item');
            const answer = faqItem.querySelector('.faq-answer');

            if (answer.style.display === 'none' || answer.style.display === '') {
                answer.style.display = 'block';
                this.textContent = '-';
            } else {
                answer.style.display = 'none';
                this.textContent = '+';
            }
        });
    });

    // Doctor Tab Selection
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            tabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            // Would typically load appropriate doctors here via AJAX
        });
    });

    // Appointment Type Selection
    const appointmentTypes = document.querySelectorAll('.appointment-type .type');
    appointmentTypes.forEach(type => {
        type.addEventListener('click', function() {
            appointmentTypes.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
