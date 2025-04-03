// About Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize stars background
    initStarsBackground();
    
    // Initialize scroll animations
    initScrollAnimations();
    
    // Initialize flippable algorithm cards
    initFlippableCards();
    
    // Initialize theme switch
    initThemeSwitch();
});

// Function to create stars background
function initStarsBackground() {
    const container = document.getElementById('stars');
    
    if (!container) return;
    
    // Create stars
    const starCount = 100;
    
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        
        // Random position
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        
        star.style.left = `${x}%`;
        star.style.top = `${y}%`;
        
        // Random size (small, medium, large)
        const size = Math.random();
        if (size > 0.8) {
            star.classList.add('large');
        } else if (size > 0.6) {
            star.classList.add('medium');
        }
        
        // Random animation delay
        star.style.animationDelay = `${Math.random() * 5}s`;
        
        container.appendChild(star);
    }
    
    // Create some shooting stars
    for (let i = 0; i < 5; i++) {
        const star = document.createElement('div');
        star.className = 'star shooting';
        
        // Random position at the top area
        const x = Math.random() * 100;
        const y = Math.random() * 30;
        
        star.style.left = `${x}%`;
        star.style.top = `${y}%`;
        
        // Random length and angle
        const length = 50 + Math.random() * 100;
        const angle = -30 + Math.random() * 60;
        
        star.style.width = `${length}px`;
        star.style.transform = `rotate(${angle}deg)`;
        
        // Random animation delay
        star.style.animationDelay = `${1 + Math.random() * 10}s`;
        
        container.appendChild(star);
    }
    
    // Create particles
    initParticles();
}

// Function to create particles
function initParticles() {
    const container = document.getElementById('particles');
    
    if (!container) return;
    
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random size (2-5px)
        const size = 2 + Math.random() * 3;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Random position
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        particle.style.left = `${x}%`;
        particle.style.top = `${y}%`;
        
        // Random opacity
        particle.style.opacity = 0.3 + Math.random() * 0.5;
        
        // Random color (purples and blues)
        const hue = 240 + Math.random() * 60;
        const saturation = 70 + Math.random() * 30;
        const lightness = 50 + Math.random() * 20;
        particle.style.backgroundColor = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
        particle.style.boxShadow = `0 0 ${size * 2}px hsl(${hue}, ${saturation}%, ${lightness}%)`;
        
        // Random movement direction (for CSS variable)
        particle.style.setProperty('--direction', Math.random() > 0.5 ? '1' : '-1');
        
        // Animation
        const duration = 15 + Math.random() * 25;
        const delay = Math.random() * 5;
        particle.style.animation = `moveParticle ${duration}s infinite linear`;
        particle.style.animationDelay = `-${delay}s`;
        
        container.appendChild(particle);
    }
}

// Function to handle scroll animations
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Function to handle flippable algorithm cards
function initFlippableCards() {
    const cards = document.querySelectorAll('.algorithm-card');
    
    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.classList.toggle('flipped');
        });
    });
}

// Function to handle theme switch
function initThemeSwitch() {
    const themeToggle = document.getElementById('theme-toggle');
    
    if (themeToggle) {
        // Check for saved user preference
        if (localStorage.getItem('theme') === 'light') {
            document.body.classList.add('light-theme');
            themeToggle.checked = true;
        }
        
        themeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('light-theme');
                localStorage.setItem('theme', 'light');
            } else {
                document.body.classList.remove('light-theme');
                localStorage.setItem('theme', 'dark');
            }
        });
    }
} 