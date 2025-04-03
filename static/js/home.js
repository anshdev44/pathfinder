// Home Page Specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize stars background
    initStarsBackground();
    
    // Initialize particles animation
    initParticles();
    
    // Initialize network graph visualization
    initNetworkGraph();
});

// Function to create stars background
function initStarsBackground() {
    const container = document.querySelector('.bg-gradient');
    
    if (!container) return;
    
    // Create stars container if it doesn't exist
    let starsContainer = document.querySelector('.stars');
    if (!starsContainer) {
        starsContainer = document.createElement('div');
        starsContainer.className = 'stars';
        container.parentNode.insertBefore(starsContainer, container.nextSibling);
    }
    
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
        
        starsContainer.appendChild(star);
    }
    
    // Create some shooting stars
    for (let i = 0; i < 5; i++) {
        const star = document.createElement('div');
        star.className = 'star shooting';
        
        // Random position at the top-right area
        const x = 50 + Math.random() * 50;
        const y = Math.random() * 50;
        
        star.style.left = `${x}%`;
        star.style.top = `${y}%`;
        
        // Random length and angle
        const length = 50 + Math.random() * 100;
        const angle = -15 - Math.random() * 30;
        
        star.style.width = `${length}px`;
        star.style.transform = `rotate(${angle}deg)`;
        
        // Random animation delay
        star.style.animationDelay = `${1 + Math.random() * 10}s`;
        
        starsContainer.appendChild(star);
    }
}

// Function to create particles animation
function initParticles() {
    const container = document.getElementById('particles');
    
    if (!container) return;
    
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random size (3-8px)
        const size = 3 + Math.random() * 5;
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
        
        // Animation
        const duration = 10 + Math.random() * 20;
        const delay = Math.random() * 5;
        particle.style.animation = `moveParticle ${duration}s infinite linear`;
        particle.style.animationDelay = `-${delay}s`;
        
        container.appendChild(particle);
    }
}

// Function to create network graph visualization
function initNetworkGraph() {
    const container = document.getElementById('network-container');
    
    if (!container) return;
    
    // Clear previous content
    container.innerHTML = '';
    
    // Create nodes
    const nodeCount = 15;
    const nodes = [];
    
    for (let i = 0; i < nodeCount; i++) {
        const node = document.createElement('div');
        node.className = 'node';
        
        // Random position with margins
        const x = 10 + Math.random() * 80;
        const y = 10 + Math.random() * 80;
        
        node.style.left = `${x}%`;
        node.style.top = `${y}%`;
        
        // Random animation delay
        node.style.animationDelay = `${Math.random() * 3}s`;
        
        // Random pulsing effect for some nodes
        if (Math.random() > 0.7) {
            node.classList.add('pulse');
        }
        
        container.appendChild(node);
        nodes.push({ element: node, x, y });
    }
    
    // Create connections between nodes
    for (let i = 0; i < nodes.length; i++) {
        // Connect to 2-3 closest nodes
        const connections = Math.floor(2 + Math.random() * 2);
        
        // Calculate distances to other nodes
        const distances = nodes
            .map((node, index) => {
                if (index === i) return { index, distance: Infinity }; // Skip self
                
                const dx = nodes[i].x - node.x;
                const dy = nodes[i].y - node.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                return { index, distance };
            })
            .sort((a, b) => a.distance - b.distance)
            .slice(0, connections);
        
        // Create connection lines
        distances.forEach(({ index }) => {
            const connection = document.createElement('div');
            connection.className = 'connection';
            
            // Calculate line dimensions and position
            const x1 = nodes[i].x;
            const y1 = nodes[i].y;
            const x2 = nodes[index].x;
            const y2 = nodes[index].y;
            
            const length = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
            const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
            
            connection.style.width = `${length}%`;
            connection.style.left = `${x1}%`;
            connection.style.top = `${y1}%`;
            connection.style.transform = `rotate(${angle}deg)`;
            
            // Random animation delay
            connection.style.animationDelay = `${Math.random() * 3}s`;
            
            // Highlight some connections
            if (Math.random() > 0.7) {
                connection.classList.add('highlight');
            }
            
            // Add to container before nodes for proper z-index
            container.insertBefore(connection, container.firstChild);
        });
    }
    
    // Animate a path through the network occasionally
    setInterval(() => {
        // Randomly select nodes to highlight
        const nodesToHighlight = Math.min(5, Math.floor(nodes.length * 0.3));
        const selectedNodes = [];
        
        // Reset all nodes
        nodes.forEach(node => {
            node.element.classList.remove('highlight');
        });
        
        // Select random nodes
        while (selectedNodes.length < nodesToHighlight) {
            const randomIndex = Math.floor(Math.random() * nodes.length);
            if (!selectedNodes.includes(randomIndex)) {
                selectedNodes.push(randomIndex);
                nodes[randomIndex].element.classList.add('highlight');
            }
        }
        
        // Highlight connections between selected nodes
        const connections = container.querySelectorAll('.connection');
        connections.forEach(connection => {
            connection.classList.remove('active');
        });
        
        // Highlight a few connections
        const connectionsToHighlight = Math.min(5, Math.floor(connections.length * 0.2));
        for (let i = 0; i < connectionsToHighlight; i++) {
            const randomIndex = Math.floor(Math.random() * connections.length);
            connections[randomIndex].classList.add('active');
        }
    }, 3000);
} 