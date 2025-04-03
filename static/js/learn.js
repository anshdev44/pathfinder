document.addEventListener('DOMContentLoaded', () => {
    // Initialize any interactive elements or animations here
    console.log('Learn page loaded');

    // Example: Initialize custom cursor
    initCustomCursor();

    // Example: Add stars to the background
    createStars(100);
});

function initCustomCursor() {
    const cursor = document.querySelector('.custom-cursor');
    document.addEventListener('mousemove', e => {
        cursor.style.left = `${e.clientX}px`;
        cursor.style.top = `${e.clientY}px`;
    });
}

function createStars(count) {
    const starsContainer = document.querySelector('.stars');
    for (let i = 0; i < count; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.top = `${Math.random() * 100}%`;
        star.style.left = `${Math.random() * 100}%`;
        star.style.animationDelay = `${Math.random() * 5}s`;
        starsContainer.appendChild(star);
    }
} 