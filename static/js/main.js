// Main JavaScript for PathFinder Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initAnimations();
    
    // Mobile navigation functionality
    initMobileNav();
    
    // Initialize ripple effect on buttons
    initRippleEffect();
});

// Function to handle animations
function initAnimations() {
    // Animate elements with animate-in class when they are in view
    const animatedElements = document.querySelectorAll('.animate-in');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Data animation attribute elements
    const dataAnimations = document.querySelectorAll('[data-animation]');
    
    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                
                // Add delay if specified
                const delay = entry.target.getAttribute('data-delay');
                if (delay) {
                    entry.target.style.animationDelay = delay;
                }
            }
        });
    }, { threshold: 0.1 });
    
    dataAnimations.forEach(element => {
        animationObserver.observe(element);
    });
    
    // Parallax effect for sections with parallax-section class
    const parallaxSections = document.querySelectorAll('.parallax-section');
    
    window.addEventListener('scroll', function() {
        parallaxSections.forEach(section => {
            const scrollPosition = window.pageYOffset;
            const speed = section.getAttribute('data-speed') || 0.5;
            const yPos = -(scrollPosition * speed);
            section.style.backgroundPosition = `center ${yPos}px`;
        });
    });
}

// Function to handle mobile navigation
function initMobileNav() {
    const navbarToggle = document.getElementById('navbar-toggle');
    const navbar = document.getElementById('navbar');
    
    if (navbarToggle && navbar) {
        navbarToggle.addEventListener('click', function() {
            navbar.classList.toggle('active');
            
            // Change hamburger icon to X when menu is open
            this.innerHTML = navbar.classList.contains('active') 
                ? '<i class="fas fa-times"></i>' 
                : '<i class="fas fa-bars"></i>';
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInside = navbar.contains(event.target) || navbarToggle.contains(event.target);
            
            if (!isClickInside && navbar.classList.contains('active')) {
                navbar.classList.remove('active');
                navbarToggle.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });
    }
}

// Function to add ripple effect to buttons
function initRippleEffect() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.className = 'btn-ripple';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
} 