// ======== DOCUMENT READY ========
document.addEventListener('DOMContentLoaded', function() {
    initNetworkGraph();
    initTypewriterEffect();
    initSmoothScroll();
    initCustomCursor();
    initAlgorithmToggle();
    initCardFlip();
    initFormSubmit();
    initScrollAnimations();
    initAutocomplete();
});

// ======== NETWORK GRAPH BACKGROUND ========
function initNetworkGraph() {
    const container = document.getElementById('networkGraph');
    const nodeCount = Math.min(30, Math.floor(window.innerWidth / 40)); // Responsive node count
    const nodes = [];
    const lines = [];
    
    // Create nodes
    for (let i = 0; i < nodeCount; i++) {
        const node = document.createElement('div');
        node.className = 'graph-node';
        
        // Random position with margins from the edges
        const x = 5 + Math.random() * 90; // 5-95% of width
        const y = 5 + Math.random() * 90; // 5-95% of height
        
        node.style.left = `${x}%`;
        node.style.top = `${y}%`;
        
        // Random delay for pulse animation
        node.style.animationDelay = `${Math.random() * 4}s`;
        
        container.appendChild(node);
        nodes.push({ element: node, x, y });
    }
    
    // Create connections between nodes
    for (let i = 0; i < nodes.length; i++) {
        // Connect each node to 2-3 nearest nodes
        const connections = 2 + Math.floor(Math.random() * 2);
        
        // Find closest nodes
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
        
        // Create lines to closest nodes
        distances.forEach(({ index }) => {
            const line = document.createElement('div');
            line.className = 'graph-line';
            
            // Calculate line position and rotation
            const x1 = nodes[i].x;
            const y1 = nodes[i].y;
            const x2 = nodes[index].x;
            const y2 = nodes[index].y;
            
            const length = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
            const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
            
            line.style.width = `${length}%`;
            line.style.left = `${x1}%`;
            line.style.top = `${y1}%`;
            line.style.transform = `rotate(${angle}deg)`;
            
            // Random animation delay
            line.style.animationDelay = `${Math.random() * 3}s`;
            
            container.appendChild(line);
            lines.push(line);
        });
    }
    
    // Add subtle random movement to nodes
    let animationFrameId;
    
    function animateNodes() {
        nodes.forEach(node => {
            const dx = (Math.random() - 0.5) * 0.05; // Tiny movement in x
            const dy = (Math.random() - 0.5) * 0.05; // Tiny movement in y
            
            node.x += dx;
            node.y += dy;
            
            // Keep within bounds
            node.x = Math.max(5, Math.min(95, node.x));
            node.y = Math.max(5, Math.min(95, node.y));
            
            node.element.style.left = `${node.x}%`;
            node.element.style.top = `${node.y}%`;
        });
        
        animationFrameId = requestAnimationFrame(animateNodes);
    }
    
    animateNodes();
    
    // Cleanup animation on page unload
    window.addEventListener('beforeunload', () => {
        cancelAnimationFrame(animationFrameId);
    });
}

// ======== TYPEWRITER EFFECT ========
function initTypewriterEffect() {
    const typewriterElement = document.getElementById('typewriter');
    const text = 'Find the shortest path... in just a click!';
    const typingSpeed = 100; // ms per character
    const startDelay = 500; // ms before typing starts
    
    setTimeout(() => {
        let i = 0;
        
        function typeNextChar() {
            if (i < text.length) {
                typewriterElement.textContent += text.charAt(i);
                i++;
                setTimeout(typeNextChar, typingSpeed);
            }
        }
        
        typeNextChar();
    }, startDelay);
}

// ======== SMOOTH SCROLL ========
function initSmoothScroll() {
    const navLinks = document.querySelectorAll('.nav-link, .footer-link, .cta-buttons a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '/' || targetId === '/about' || targetId === '/learn') {
                return; // Allow default behavior for Home, About, and Learn links
            }
            e.preventDefault();
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                // Update active link
                document.querySelectorAll('.nav-link').forEach(navLink => {
                    navLink.classList.remove('active');
                });
                if (this.classList.contains('nav-link')) {
                    this.classList.add('active');
                }
                // Smooth scroll to section
                window.scrollTo({
                    top: targetSection.offsetTop - 70, // Offset for navbar height
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Update active nav link on scroll
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        
        // Add background color to navbar when scrolled
        const navbar = document.querySelector('.navbar');
        if (scrollPosition > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Update active nav link
        const sections = document.querySelectorAll('section');
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                const targetLink = document.querySelector(`.nav-link[href="#${section.id}"]`);
                
                document.querySelectorAll('.nav-link').forEach(navLink => {
                    navLink.classList.remove('active');
                });
                
                if (targetLink) {
                    targetLink.classList.add('active');
                }
            }
        });
    });
}

// ======== CUSTOM CURSOR ========
function initCustomCursor() {
    const cursor = document.querySelector('.custom-cursor');
    
    document.addEventListener('mousemove', e => {
        cursor.style.left = `${e.clientX}px`;
        cursor.style.top = `${e.clientY}px`;
        
        if (!cursor.classList.contains('active')) {
            cursor.classList.add('active');
        }
    });
    
    // Hover effect on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .algorithm-toggle .toggle-option, .algo-card, .form-input');
    
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            cursor.classList.add('hovering');
        });
        
        element.addEventListener('mouseleave', () => {
            cursor.classList.remove('hovering');
        });
    });
    
    // Hide cursor when it leaves the window
    document.addEventListener('mouseleave', () => {
        cursor.classList.remove('active');
    });
    
    document.addEventListener('mouseenter', () => {
        cursor.classList.add('active');
    });
}

// ======== ALGORITHM TOGGLE ========
function initAlgorithmToggle() {
    const toggleOptions = document.querySelectorAll('.toggle-option');
    const algorithmInput = document.getElementById('selectedAlgorithm');
    const slider = document.querySelector('.toggle-slider');
    
    console.log('Initializing algorithm toggle with', toggleOptions.length, 'options');
    
    toggleOptions.forEach(option => {
        option.addEventListener('click', function() {
            const algorithm = this.getAttribute('data-algorithm');
            console.log('Toggle option clicked:', algorithm);
            
            // Update visual state
            toggleOptions.forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            
            // Move slider
            if (algorithm === 'astar') {
                slider.style.transform = 'translateX(100%)';
                algorithmInput.value = 'a_star'; // Convert for backend
            } else {
                slider.style.transform = 'translateX(0)';
                algorithmInput.value = 'dijkstra';
            }
            
            console.log(`Algorithm selected: ${algorithmInput.value}`);
        });
    });
}

// ======== CARD FLIP ========
function initCardFlip() {
    const flipButtons = document.querySelectorAll('.flip-btn');
    
    flipButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const card = this.closest('.algo-card');
            card.classList.toggle('flipped');
        });
    });
}

// ======== FORM SUBMIT ========
function initFormSubmit() {
    const form = document.getElementById('pathFinderForm');
    const resultsContainer = document.getElementById('pathResults');
    
    if (!form) {
        console.error('Path finder form not found');
        return;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form values
        const startCity = document.getElementById('startCity').value;
        const startState = document.getElementById('startState').value;
        const endCity = document.getElementById('endCity').value;
        const endState = document.getElementById('endState').value;
        const algorithm = document.getElementById('selectedAlgorithm')?.value || 'dijkstra';
        
        // Form validation
        if (!startCity || !startState || !endCity || !endState) {
            alert('Please fill in all fields');
            return;
        }
        
        // Show loading state
        const submitButton = form.querySelector('.btn-find');
        if (!submitButton) {
            console.error('Submit button not found');
            return;
        }
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Calculating...';
        submitButton.disabled = true;
        
        // Show loading overlay
        showLoading(`Finding best route from ${startCity} to ${endCity}...\nThis may take a few moments.`);
        
        try {
            // Create city IDs
            const start_id = formatCityId(startCity, startState);
            const end_id = formatCityId(endCity, endState);
            
            console.log('Sending request with:', {
                algorithm,
                start_id,
                end_id
            });
            
            // Make API call to backend with timeout
            let controller = new AbortController();
            let timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout
            
            const response = await fetch('/api/find_path', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    algorithm,
                    start_id,
                    end_id
                }),
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);

            const data = await response.json();
            
            // Debug: Log the full response
            console.log('Path API Response:', data);
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to find path');
            }
            
            // Check if we received the path data in expected format
            if (!data.path || !Array.isArray(data.path)) {
                console.error('Response is missing path data or it\'s not an array:', data.path);
                throw new Error('Invalid path data received from server');
            }
            
            // Debug: Log the first and last node in the path
            if (data.path.length > 0) {
                console.log('First node in path:', data.path[0]);
                console.log('Last node in path:', data.path[data.path.length - 1]);
            }
            
            // Format distance and time
            const distance = typeof data.distance === 'number' 
                ? `${(data.distance / 1000).toFixed(2)} km` 
                : 'N/A';
                
            const time = typeof data.time === 'number'
                ? `${Math.round(data.time)} minutes`
                : 'N/A';
            
            // Display results
            if (resultsContainer) {
                resultsContainer.style.display = 'block';
                
                // Store path data for map display
                console.log('Storing path data:', data.path);
                resultsContainer.__pathData = data.path || [];
                
                // Store city coordinates for use in the map display
                if (!window.cityCoordinates) {
                    window.cityCoordinates = {};
                }
                
                // Create a mapping from city IDs to coordinates
                if (data.coordinates) {
                    Object.entries(data.coordinates).forEach(([id, coords]) => {
                        window.cityCoordinates[id] = coords;
                    });
                }
                
                resultsContainer.innerHTML = `
                    <h3>Path Found using ${algorithm === 'dijkstra' ? 'Dijkstra\'s Algorithm' : 'A* Algorithm'}</h3>
                    <div class="path-details">
                        <div class="path-row">
                            <div class="path-label">From:</div>
                            <div class="path-value">${startCity}, ${startState}</div>
                        </div>
                        <div class="path-row">
                            <div class="path-label">To:</div>
                            <div class="path-value">${endCity}, ${endState}</div>
                        </div>
                        <div class="path-row">
                            <div class="path-label">Distance:</div>
                            <div class="path-value distance-value">${distance}</div>
                        </div>
                        <div class="path-row">
                            <div class="path-label">Estimated Time:</div>
                            <div class="path-value path-time">${time}</div>
                        </div>
                    </div>
                    <div class="path-visualization">
                        <svg viewBox="0 0 300 100">
                            <circle cx="30" cy="50" r="8" fill="rgba(138, 43, 226, 0.8)" />
                            <circle cx="270" cy="50" r="8" fill="rgba(138, 43, 226, 0.8)" />
                            <path d="M30,50 Q150,10 270,50" stroke="var(--primary)" stroke-width="3" fill="none" class="animated-path" />
                        </svg>
                    </div>
                    <div class="path-buttons">
                        <button type="button" id="viewOnMapBtn" class="btn-primary">
                            View on Map
                        </button>
                        <button type="button" onclick="resetForm()" class="btn-secondary">
                            Reset
                        </button>
                    </div>
                `;
                
                // Add event listener to View on Map button
                const viewOnMapBtn = document.getElementById('viewOnMapBtn');
                if (viewOnMapBtn) {
                    viewOnMapBtn.addEventListener('click', function() {
                        // Pass the path data to the showRoute function
                        showRoute(data.path);
                    });
                }
            }
            
        } catch (error) {
            console.error('Error:', error);
            let errorMessage = error.message;
            
            // Handle timeout separately
            if (error.name === 'AbortError') {
                errorMessage = 'The request took too long to complete. This could be due to network issues or server load.';
            }
            
            if (resultsContainer) {
                resultsContainer.style.display = 'block';
                resultsContainer.innerHTML = `
                    <div class="error-message">
                        <p>Error: ${errorMessage}</p>
                        <p>Please try again with different cities or contact support if the issue persists.</p>
                    </div>
                `;
            }
        } finally {
            // Reset button state
            submitButton.textContent = originalText;
            submitButton.disabled = false;
            
            // Hide loading overlay
            hideLoading();
        }
    });
}

// Function to format city ID - MUST match the backend formatting
function formatCityId(city, state) {
    // Convert to lowercase and remove spaces, periods, and hyphens
    const cityPart = city.toLowerCase().replace(/[\s\.\-]/g, '');
    const statePart = state.toLowerCase().replace(/[\s\.\-]/g, '');
    console.log(`Formatting ID: ${city}, ${state} -> ${cityPart}_${statePart}`);
    return `${cityPart}_${statePart}`;
}

// Function to show a route on the map
function showRoute(pathData) {
    console.log('showRoute called with:', pathData);
    
    // Store pending path data if map is not initialized yet
    if (!window.map || !window.directionsService || !window.directionsRenderer) {
        console.log('Map not initialized yet, storing path data for later');
        window.pendingPathData = pathData;
        
        // Try to initialize map if Google Maps API is loaded
        if (window.google && window.google.maps) {
            console.log('Google Maps API is loaded, initializing map now');
            if (initializeMap(pathData)) {
                // If initialization succeeded, clear pending data
                window.pendingPathData = null;
            } else {
                console.error('Map initialization failed');
                return;
            }
        } else {
            console.error('Google Maps API not loaded yet');
            alert('Google Maps API is not loaded yet. Please try again in a few seconds.');
            return;
        }
    }
    
    // Make sure map container is visible
    const mapContainer = document.querySelector('.map-container');
    if (mapContainer) {
        mapContainer.style.display = 'block';
        mapContainer.classList.add('active');
        
        // Show loading indicator
        const loadingIndicator = document.querySelector('.map-loading');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'flex';
        }
    } else {
        console.error('Map container not found!');
        return;
    }
    
    try {
        // Check if pathData has valid cities and coordinates
        if (!pathData || !Array.isArray(pathData) || pathData.length < 2) {
            console.error('Invalid path data:', pathData);
            alert('Invalid path data. Please try again with different cities.');
            
            // Hide loading indicator
            const loadingIndicator = document.querySelector('.map-loading');
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
            return;
        }
        
        // First try to get city names from path IDs
        const startCityId = pathData[0];
        const endCityId = pathData[pathData.length - 1];
        
        console.log('Path data available:', pathData);
        
        // Convert city IDs to display names (Lucknow, Uttar Pradesh format)
        function cityIdToDisplayName(cityId) {
            if (!cityId || typeof cityId !== 'string') return null;
            
            // Extract city and state parts
            const parts = cityId.split('_');
            if (parts.length !== 2) return null;
            
            // Capitalize first letter of each word
            const city = parts[0].replace(/\b\w/g, c => c.toUpperCase());
            const state = parts[1].replace(/\b\w/g, c => c.toUpperCase())
                .replace('uttarpradesh', 'Uttar Pradesh')
                .replace('madhyapradesh', 'Madhya Pradesh')
                .replace('tamilnadu', 'Tamil Nadu')
                .replace('westbengal', 'West Bengal');
                
            return `${city}, ${state}`;
        }
        
        const startCity = cityIdToDisplayName(startCityId);
        const endCity = cityIdToDisplayName(endCityId);
        
        console.log('Using city names for route:', { startCity, endCity });
        
        // If we have valid city names, use those for the route
        if (startCity && endCity) {
            calculateAndDisplayRoute(startCity, endCity);
            return;
        }
        
        // Fallback: Try to use coordinates if available
        console.log('Using path data coordinates for route');
        
        // Prepare waypoints from coordinates
        const waypoints = [];
        let validCoordinates = true;
        
        pathData.forEach((cityId, index) => {
            // Try to find the city coordinates
            const lat = window.cityCoordinates && window.cityCoordinates[cityId] ? 
                window.cityCoordinates[cityId].lat : null;
                
            const lng = window.cityCoordinates && window.cityCoordinates[cityId] ? 
                window.cityCoordinates[cityId].lng : null;
            
            if (lat && lng && !isNaN(lat) && !isNaN(lng)) {
                waypoints.push({ lat: parseFloat(lat), lng: parseFloat(lng), original: cityId });
            } else {
                console.error(`Invalid coordinates in path data: ${cityId}`);
                validCoordinates = false;
            }
        });
        
        if (!validCoordinates || waypoints.length < 2) {
            console.error('Not enough valid coordinates in path data');
            alert('Could not get valid coordinates for the selected cities. Please try different cities.');
            
            // Hide loading indicator
            const loadingIndicator = document.querySelector('.map-loading');
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
            return;
        }
        
        console.log('Coordinate points:', waypoints);
        
        // Use first and last waypoints as start and end
        const start = waypoints[0];
        const end = waypoints[waypoints.length - 1];
        
        calculateAndDisplayRoute(start, end, waypoints);
    } catch (error) {
        console.error('Error showing route:', error);
        alert('An error occurred while showing the route: ' + error.message);
        
        // Hide loading indicator
        const loadingIndicator = document.querySelector('.map-loading');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
    }
}

// Function to calculate and display route on the map
function calculateAndDisplayRoute(start, end, waypoints) {
    console.log('calculateAndDisplayRoute called with:', { start, end, waypoints });

    // Check if Google Maps is initialized
    if (!window.google || !window.google.maps) {
        console.error('Google Maps API not loaded yet');
        alert('Google Maps API could not be loaded. Please check your API key in config.py and restart the server.');
        
        // Hide loading indicator
        const loadingIndicator = document.querySelector('.map-loading');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        return;
    }
    
    // Check if directions services are initialized
    if (!window.directionsService || !window.directionsRenderer) {
        console.error('Google Maps services not initialized');
        alert('Map services are not initialized. Please ensure you have a valid Google Maps API key with Directions API enabled.');
        // Hide loading indicator
        const loadingIndicator = document.querySelector('.map-loading');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        return;
    }
    
    // Check if waypoints have valid coordinates
    if (waypoints && waypoints.length > 0) {
        let hasInvalidCoordinates = false;
        waypoints.forEach((point, index) => {
            if (!point || isNaN(point.lat) || isNaN(point.lng)) {
                console.error(`Invalid coordinate at index ${index}:`, point);
                hasInvalidCoordinates = true;
            }
        });
        
        if (hasInvalidCoordinates) {
            alert('Some coordinates could not be loaded. Please try selecting different cities or check your browser console for details.');
            // Hide loading indicator
            const loadingIndicator = document.querySelector('.map-loading');
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
            return;
        }
    }
    
    const useCoordinates = typeof start === 'object' && start.lat && start.lng;
    
    console.log('Route request configuration:', {
        useCoordinates,
        start: useCoordinates ? start : start + ", India",
        end: useCoordinates ? end : end + ", India",
        travelMode: 'DRIVING'
    });
    
    const request = {
        origin: useCoordinates ? start : start + ", India",
        destination: useCoordinates ? end : end + ", India",
        travelMode: google.maps.TravelMode.DRIVING
    };

    // Set timeout for directions request
    const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Directions request timed out')), 10000);
    });

    // Actual directions request
    const directionsPromise = new Promise((resolve, reject) => {
        window.directionsService.route(request, function(response, status) {
            if (status === 'OK') {
                resolve(response);
            } else {
                reject(new Error('Directions request failed: ' + status));
            }
        });
    });

    // Race the promises
    Promise.race([directionsPromise, timeoutPromise])
        .then(response => {
            // Show the map
            window.directionsRenderer.setMap(window.map);
            window.directionsRenderer.setDirections(response);
            
            // Update any distance/time display if needed
            if (response.routes && response.routes[0]) {
                const route = response.routes[0];
                const leg = route.legs[0];
                
                const distanceElement = document.querySelector('.distance-value');
                const timeElement = document.querySelector('.path-time');
                
                if (distanceElement && leg.distance) {
                    distanceElement.textContent = leg.distance.text;
                }
                
                if (timeElement && leg.duration) {
                    timeElement.textContent = leg.duration.text;
                }
            }
        })
        .catch(error => {
            console.error('Error calculating route:', error);
            
            // Fallback: Draw a simple line between points
            if (window.map && waypoints && waypoints.length >= 2) {
                const path = new google.maps.Polyline({
                    path: waypoints,
                    geodesic: true,
                    strokeColor: '#8A2BE2',
                    strokeOpacity: 1.0,
                    strokeWeight: 3
                });
                
                // Clear any existing directions
                window.directionsRenderer.setMap(null);
                
                // Draw the polyline
                path.setMap(window.map);
                
                // Fit bounds to the path
                const bounds = new google.maps.LatLngBounds();
                waypoints.forEach(point => bounds.extend(point));
                window.map.fitBounds(bounds);
            } else {
                alert('Could not display route on map. Please try again.');
            }
        })
        .finally(() => {
            // Hide loading indicator
            const loadingIndicator = document.querySelector('.map-loading');
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
        });
}

// Function to reset the form
function resetForm() {
    const form = document.getElementById('pathFinderForm');
    const resultsContainer = document.getElementById('pathResults');
    const mapContainer = document.querySelector('.map-container');
    
    if (form) {
        form.reset();
    }
    
    if (resultsContainer) {
        resultsContainer.style.display = 'none';
    }
    
    if (mapContainer) {
        mapContainer.style.display = 'none';
        mapContainer.classList.remove('active');
    }
    
    if (window.directionsRenderer) {
        window.directionsRenderer.setMap(null);
    }
}

// ======== SCROLL ANIMATIONS ========
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.fade-in, .slide-up');
    
    const checkVisibility = () => {
        const windowHeight = window.innerHeight;
        const offset = 100; // Offset to trigger animation before element is fully visible
        
        animatedElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            
            if (elementPosition < windowHeight - offset) {
                element.classList.add('visible');
            }
        });
    };
    
    // Initial check
    checkVisibility();
    
    // Check on scroll
    window.addEventListener('scroll', checkVisibility);
}

// Add fade-in and slide-up classes to elements when the page loads
window.addEventListener('load', function() {
    // About section animations
    document.querySelectorAll('.about-text p').forEach((p, index) => {
        p.classList.add('fade-in');
        p.style.animationDelay = `${0.2 * index}s`;
    });
    
    document.querySelector('.about-image').classList.add('slide-up');
    document.querySelector('.about-image').style.animationDelay = '0.4s';
    
    // Algorithm cards animations
    document.querySelectorAll('.algo-card-container').forEach((card, index) => {
        card.classList.add('slide-up');
        card.style.animationDelay = `${0.2 * index}s`;
    });
    
    // Path finder form animations
    document.querySelectorAll('.form-group').forEach((group, index) => {
        group.classList.add('fade-in');
        group.style.animationDelay = `${0.1 * index}s`;
    });
    
    document.querySelector('.form-actions').classList.add('slide-up');
    document.querySelector('.form-actions').style.animationDelay = '0.5s';
});

// ======== AUTOCOMPLETE ========
function initAutocomplete() {
    // List of Indian states for autocomplete
    const states = [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
        'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
        'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
        'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
        'Delhi', 'Jammu and Kashmir', 'Ladakh'
    ];

    // Cities organized by state
    const citiesByState = {
        'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Prayagraj', 'Varanasi', 'Ghaziabad', 'Noida'],
        'Madhya Pradesh': ['Bhopal', 'Indore', 'Gwalior', 'Jabalpur', 'Ujjain', 'Rewa'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Nashik', 'Aurangabad'],
        'Delhi': ['New Delhi', 'Delhi'],
        'Haryana': ['Gurgaon', 'Faridabad', 'Chandigarh'],
        'Karnataka': ['Bangalore', 'Mysore', 'Hubli'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai'],
        'Telangana': ['Hyderabad', 'Warangal'],
        'West Bengal': ['Kolkata', 'Howrah'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara'],
        'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur'],
        'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode'],
        'Bihar': ['Patna', 'Gaya'],
        'Odisha': ['Bhubaneswar', 'Cuttack', 'Puri']
    };

    // Populate state dropdowns
    function populateStateDropdown(selectElement) {
        states.forEach(state => {
            const option = document.createElement('option');
            option.value = state;
            option.textContent = state;
            selectElement.appendChild(option);
        });
    }

    // Populate city dropdown based on selected state
    function populateCityDropdown(citySelect, state) {
        // Clear existing options except the first one
        while (citySelect.options.length > 1) {
            citySelect.remove(1);
        }

        if (state && citiesByState[state]) {
            citySelect.disabled = false;
            citiesByState[state].forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        } else {
            citySelect.disabled = true;
        }
    }

    // Setup state dropdowns
    const startStateSelect = document.getElementById('startState');
    const endStateSelect = document.getElementById('endState');
    const startCitySelect = document.getElementById('startCity');
    const endCitySelect = document.getElementById('endCity');

    // Populate state dropdowns
    populateStateDropdown(startStateSelect);
    populateStateDropdown(endStateSelect);

    // Add change event listeners for state dropdowns
    startStateSelect.addEventListener('change', function() {
        populateCityDropdown(startCitySelect, this.value);
    });

    endStateSelect.addEventListener('change', function() {
        populateCityDropdown(endCitySelect, this.value);
    });

    // Add custom styling for dropdowns
    const style = document.createElement('style');
    style.textContent = `
        .form-input {
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238a2be2' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 10px center;
            background-size: 1em;
            padding-right: 2.5em;
        }

        .form-input:disabled {
            background-color: rgba(26, 26, 46, 0.5);
            cursor: not-allowed;
        }

        .form-input option {
            background-color: #1a1a2e;
            color: #fff;
        }
    `;
    document.head.appendChild(style);
}

// ======== MAP INITIALIZATION ========
// Map variables are declared in the HTML file
// let map;
// let directionsService;
// let directionsRenderer;

function initializeMap(pathData) {
    console.log('initializeMap called with path data:', pathData);
    
    // Check if we already have valid map instances
    if (window.map && window.directionsService && window.directionsRenderer) {
        console.log('Map already initialized, refreshing');
        google.maps.event.trigger(window.map, 'resize');
        return true;
    }
    
    // Check if Google Maps API is loaded
    if (!window.google || !window.google.maps) {
        console.error('Google Maps API not loaded yet!');
        alert('Google Maps API is not loaded. Please check your API key and internet connection.');
        return false;
    }
    
    console.log('Google Maps API available, initializing map');
    try {
        // Get the map element
        const mapElement = document.getElementById('map');
        if (!mapElement) {
            console.error('Map element not found!');
            return false;
        }
        
        // Check if the map container has dimensions
        const rect = mapElement.getBoundingClientRect();
        console.log('Map container dimensions:', rect);
        
        if (rect.width === 0 || rect.height === 0) {
            console.warn('Map container has zero dimension!');
            // Force a minimum height
            mapElement.style.height = '400px';
            mapElement.style.width = '100%';
        }
        
        // Initialize the map
        console.log('Creating new Google Map instance');
        window.map = new google.maps.Map(mapElement, {
            center: { lat: 20.5937, lng: 78.9629 }, // Center of India
            zoom: 5,
            styles: [
                { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
                { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
                { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
                {
                    featureType: "administrative.locality",
                    elementType: "labels.text.fill",
                    stylers: [{ color: "#d59563" }],
                },
                {
                    featureType: "road",
                    elementType: "geometry",
                    stylers: [{ color: "#38414e" }],
                },
                {
                    featureType: "road",
                    elementType: "geometry.stroke",
                    stylers: [{ color: "#212a37" }],
                },
                {
                    featureType: "road",
                    elementType: "labels.text.fill",
                    stylers: [{ color: "#9ca5b3" }],
                },
                {
                    featureType: "water",
                    elementType: "geometry",
                    stylers: [{ color: "#17263c" }],
                },
            ],
        });
        
        console.log('Creating directions service and renderer');
        window.directionsService = new google.maps.DirectionsService();
        window.directionsRenderer = new google.maps.DirectionsRenderer({
            map: window.map,
            suppressMarkers: false,
            polylineOptions: {
                strokeColor: '#8a2be2', // Purple color
                strokeWeight: 4
            }
        });
        
        console.log('Map initialized successfully');
        
        // Make the map container visible
        mapElement.style.display = 'block';
        mapElement.classList.add('active');
        
        return true;
    } catch (error) {
        console.error('Error initializing map:', error);
        alert('Failed to initialize map: ' + error.message);
        return false;
    }
}

// Show loading state
function showLoading(message = 'Processing...') {
    // Create loading overlay if it doesn't exist
    let loadingOverlay = document.getElementById('loadingOverlay');
    if (!loadingOverlay) {
        loadingOverlay = document.createElement('div');
        loadingOverlay.id = 'loadingOverlay';
        loadingOverlay.innerHTML = `
            <div class="loading-spinner"></div>
            <div class="loading-message"></div>
        `;
        document.body.appendChild(loadingOverlay);
        
        // Add CSS for the loading overlay
        const style = document.createElement('style');
        style.textContent = `
            #loadingOverlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(26, 26, 46, 0.8);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                z-index: 1000;
                backdrop-filter: blur(3px);
            }
            .loading-spinner {
                width: 50px;
                height: 50px;
                border: 5px solid rgba(138, 43, 226, 0.3);
                border-radius: 50%;
                border-top-color: #8a2be2;
                animation: spin 1s ease-in-out infinite;
            }
            .loading-message {
                margin-top: 20px;
                color: white;
                font-size: 16px;
                font-family: 'Poppins', sans-serif;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Set message
    loadingOverlay.querySelector('.loading-message').textContent = message;
    
    // Show the overlay
    loadingOverlay.style.display = 'flex';
}

// Hide loading state
function hideLoading() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
}

// Add event listener for close button
document.addEventListener('DOMContentLoaded', function() {
    const closeBtn = document.querySelector('.map-close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            const mapContainer = document.querySelector('.map-container');
            if (mapContainer) {
                mapContainer.classList.remove('active');
                mapContainer.style.display = 'none';
            }
        });
    }
}); 