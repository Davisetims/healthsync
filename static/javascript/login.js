// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.getElementById('password');
    
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            // Toggle the type attribute
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle the icon
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }
    
    // Form validation
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Basic validation
            if (!email || !password) {
                showError('Please fill in all fields');
                return;
            }
            
            if (!isValidEmail(email)) {
                showError('Please enter a valid email address');
                return;
            }
            
            // Simulate login process
            simulateLogin(email, password);
        });
    }
    
    // Add floating label effect
    const inputs = document.querySelectorAll('.input-group input');
    
    inputs.forEach(input => {
        // Add focus effect
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        // Remove focus effect if input is empty
        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Check on load if input has value
        if (input.value !== '') {
            input.parentElement.classList.add('focused');
        }
    });
    
    // Add subtle animation to the doctor cards
    animateDoctorCards();
});

// Helper functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showError(message) {
    // You can implement a more sophisticated error display
    alert(message);
}

function simulateLogin(email, password) {
    // Show loading state
    const loginButton = document.querySelector('.login-button');
    loginButton.textContent = 'Logging in...';
    loginButton.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        // Reset button
        loginButton.textContent = 'LOGIN';
        loginButton.disabled = false;
        
        // In a real app, you would check credentials against your backend
        // For demo purposes, we'll just redirect to a dashboard
        window.location.href = 'dashboard.html';
    }, 1500);
}

function animateDoctorCards() {
    const doctorCards = document.querySelectorAll('.doctor-card');
    
    doctorCards.forEach((card, index) => {
        // Add a slight floating animation
        card.style.animation = `float ${2 + index * 0.5}s ease-in-out infinite alternate`;
    });
}

// Add some CSS animations
document.head.insertAdjacentHTML('beforeend', `
    <style>
        @keyframes float {
            0% {
                transform: translateY(0);
            }
            100% {
                transform: translateY(-10px);
            }
        }
        
        .input-group.focused input {
            border-color: #0077cc;
            box-shadow: 0 0 0 2px rgba(0, 119, 204, 0.2);
        }
        
        .login-button {
            position: relative;
            overflow: hidden;
        }
        
        .login-button:after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 5px;
            height: 5px;
            background: rgba(255, 255, 255, 0.5);
            opacity: 0;
            border-radius: 100%;
            transform: scale(1, 1) translate(-50%);
            transform-origin: 50% 50%;
        }
        
        .login-button:focus:not(:active)::after {
            animation: ripple 1s ease-out;
        }
        
        @keyframes ripple {
            0% {
                transform: scale(0, 0);
                opacity: 0.5;
            }
            20% {
                transform: scale(25, 25);
                opacity: 0.5;
            }
            100% {
                opacity: 0;
                transform: scale(40, 40);
            }
        }
    </style>
`);


// Helper function to display errors
function showError(message) {
    alert(message); // You can enhance this by using a modal or toast notification
}
