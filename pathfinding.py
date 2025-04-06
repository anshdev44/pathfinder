import heapq
from typing import Dict, List, Tuple, Set, Optional
import googlemaps
from dataclasses import dataclass, field
from math import radians, sin, cos, sqrt, atan2
import time
import signal
import sys

@dataclass(order=True)
class PriorityNode:
    priority: float
    node_id: str = field(compare=False)

@dataclass
class Node:
    id: str  # Unique identifier (e.g., "lucknow_uttarpradesh")
    name: str # Display name (e.g., "Lucknow, Uttar Pradesh")
    lat: float
    lng: float
    g_cost: float = float('inf')  # Cost from start to current node
    h_cost: float = 0             # Heuristic cost (estimated cost to end)
    parent: Optional['Node'] = None

    @property
    def f_cost(self) -> float:
        """Total estimated cost (A*)."""
        return self.g_cost + self.h_cost

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

class PathFinder:
    def __init__(self, api_key: str):
        """Initialize the path finder with Google Maps API key."""
        if not api_key or api_key == "YOUR_API_KEY_HERE" or api_key == "PLACEHOLDER_API_KEY":
            raise ValueError("API key is missing or placeholder. Please provide a valid Google Maps API key.")
        try:
            self.gmaps = googlemaps.Client(key=api_key)
            # Test the API key with a simple request
            self.gmaps.geocode("Delhi, India")
            print("Google Maps API connection successful")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Google Maps client: {e}")

        self.nodes: Dict[str, Node] = {}
        # Cache distances to avoid repeated API calls: (node1_id, node2_id) -> distance_meters
        self.distances: Dict[Tuple[str, str], Optional[float]] = {}
        # Define cities by state
        self.cities_by_state = {
            'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Noida', 'Ghaziabad'],
            'Madhya Pradesh': ['Bhopal', 'Indore', 'Gwalior', 'Jabalpur', 'Ujjain', 'Rewa'],
            'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Nashik', 'Aurangabad'],
            'Delhi': ['New Delhi', 'Delhi'],
            'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum'],
            'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Trichy', 'Salem'],
            'Haryana': ['Gurgaon', 'Faridabad', 'Panipat', 'Ambala', 'Rohtak'],
            'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar'],
            'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer'],
            'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol', 'Siliguri'],
            'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Karimnagar'],
            'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Tirupati'],
            'Kerala': ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Thrissur'],
            'Bihar': ['Patna', 'Gaya', 'Muzaffarpur', 'Bhagalpur'],
            'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Puri'],
        }
        self.states = list(self.cities_by_state.keys())

        # Store known coordinates to reduce Geocoding API calls
        self.known_coordinates = {
            'newdelhi_delhi': {'lat': 28.6139, 'lng': 77.2090},
            'delhi_delhi': {'lat': 28.7041, 'lng': 77.1025},
            'mumbai_maharashtra': {'lat': 19.0760, 'lng': 72.8777},
            'pune_maharashtra': {'lat': 18.5204, 'lng': 73.8567},
            'nagpur_maharashtra': {'lat': 21.1458, 'lng': 79.0882},
            'thane_maharashtra': {'lat': 19.2183, 'lng': 72.9781},
            'nashik_maharashtra': {'lat': 19.9975, 'lng': 73.7898},
            'bangalore_karnataka': {'lat': 12.9716, 'lng': 77.5946},
            'mysore_karnataka': {'lat': 12.2958, 'lng': 76.6394},
            'chennai_tamilnadu': {'lat': 13.0827, 'lng': 80.2707},
            'lucknow_uttarpradesh': {'lat': 26.8467, 'lng': 80.9462},
            'kanpur_uttarpradesh': {'lat': 26.4499, 'lng': 80.3319},
            'agra_uttarpradesh': {'lat': 27.1767, 'lng': 78.0081},
            'varanasi_uttarpradesh': {'lat': 25.3176, 'lng': 82.9739},
            'noida_uttarpradesh': {'lat': 28.5355, 'lng': 77.3910},
            'ghaziabad_uttarpradesh': {'lat': 28.6692, 'lng': 77.4538},
            'bhopal_madhyapradesh': {'lat': 23.2599, 'lng': 77.4126},
            'indore_madhyapradesh': {'lat': 22.7196, 'lng': 75.8577},
            'gwalior_madhyapradesh': {'lat': 26.2183, 'lng': 78.1828},
            'jabalpur_madhyapradesh': {'lat': 23.1815, 'lng': 79.9864},
            'ujjain_madhyapradesh': {'lat': 23.1765, 'lng': 75.7885},
            'rewa_madhyapradesh': {'lat': 24.5362, 'lng': 81.3037},
            'kolkata_westbengal': {'lat': 22.5726, 'lng': 88.3639},
            'howrah_westbengal': {'lat': 22.5958, 'lng': 88.2636},
            'hyderabad_telangana': {'lat': 17.3850, 'lng': 78.4867},
            'ahmedabad_gujarat': {'lat': 23.0225, 'lng': 72.5714},
            'surat_gujarat': {'lat': 21.1702, 'lng': 72.8311},
            'jaipur_rajasthan': {'lat': 26.9124, 'lng': 75.7873},
            'patna_bihar': {'lat': 25.5941, 'lng': 85.1376},
            'gurgaon_haryana': {'lat': 28.4595, 'lng': 77.0266},
            'faridabad_haryana': {'lat': 28.4089, 'lng': 77.3178},
        }
        self.initialize_nodes()

    def _format_id(self, city: str, state: str) -> str:
        """Creates a standardized ID from city and state."""
        city_part = city.lower().replace(' ', '').replace('.', '').replace('-', '')
        state_part = state.lower().replace(' ', '').replace('.', '').replace('-', '')
        city_id = f"{city_part}_{state_part}"
        return city_id

    def initialize_nodes(self):
        """Populate nodes using cities_by_state and fetch coordinates if needed."""
        print("Initializing nodes...")
        nodes_added = 0
        for state, cities in self.cities_by_state.items():
            for city in cities:
                city_id = self._format_id(city, state)
                display_name = f"{city}, {state}"
                lat, lng = None, None

                if city_id in self.known_coordinates:
                    coords = self.known_coordinates[city_id]
                    lat, lng = coords['lat'], coords['lng']
                else:
                    try:
                        print(f"Fetching coordinates for {display_name}...")
                        geocode_result = self.gmaps.geocode(f"{city}, {state}, India")
                        if geocode_result:
                            location = geocode_result[0]['geometry']['location']
                            lat, lng = location['lat'], location['lng']
                            # Add to known coordinates for future use
                            self.known_coordinates[city_id] = {'lat': lat, 'lng': lng}
                            print(f"Got coordinates for {display_name}: {lat}, {lng}")
                        else:
                            print(f"Warning: Could not geocode {display_name}. Skipping.")
                            continue
                        time.sleep(0.05)  # Small delay to respect API rate limits
                    except Exception as e:
                        print(f"Error geocoding {display_name}: {e}")
                        continue

                if lat is not None and lng is not None:
                    self.nodes[city_id] = Node(id=city_id, name=display_name, lat=lat, lng=lng)
                    nodes_added += 1

        print(f"Node initialization complete. Added {nodes_added} nodes.")
        if not self.nodes:
            print("WARNING: No nodes were initialized. Check city/state data and API key.")
            raise ValueError("Failed to initialize any nodes. Check Google Maps API key.")

    def _haversine_distance(self, node1: Node, node2: Node) -> float:
        """Calculate straight-line distance (km) between two points using Haversine formula."""
        R = 6371.0  # Earth radius in kilometers

        lat1, lon1 = radians(node1.lat), radians(node1.lng)
        lat2, lon2 = radians(node2.lat), radians(node2.lng)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance_km = R * c
        return distance_km * 1000  # Return distance in meters

    def get_driving_distance(self, node1: Node, node2: Node) -> Optional[float]:
        """Get driving distance in meters using Google Maps Distance Matrix API."""
        if node1.id == node2.id:
            return 0.0

        # Use tuple sorted by id for consistent caching key
        pair_key = tuple(sorted((node1.id, node2.id)))

        if pair_key in self.distances:
            return self.distances[pair_key]

        # Straight-line distance as initial approximation
        haversine_dist = self._haversine_distance(node1, node2)
        
        # For very far cities, don't try the API call
        if haversine_dist > 500000:  # 500 km in meters - reduced from 1000km for better performance
            print(f"Cities too far apart ({haversine_dist/1000:.1f} km), using Haversine: {node1.name} <-> {node2.name}")
            self.distances[pair_key] = haversine_dist
            return haversine_dist
            
        try:
            # Use Distance Matrix API to get actual driving distance
            result = self.gmaps.distance_matrix(
                origins=[(node1.lat, node1.lng)],
                destinations=[(node2.lat, node2.lng)],
                mode="driving",
                units="metric"
            )
            
            # Check if we got a valid result
            if result['status'] == 'OK':
                element = result['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    distance = element['distance']['value']  # Distance in meters
                    self.distances[pair_key] = distance
                    return distance
            
            # If API call fails or returns no route, fall back to haversine
            print(f"No driving route found, using straight-line: {node1.name} <-> {node2.name}")
            self.distances[pair_key] = haversine_dist
            return haversine_dist
                
        except Exception as e:
            print(f"Error fetching driving distance: {e}")
            self.distances[pair_key] = haversine_dist
            return haversine_dist

    def find_path(self, start_id: str, end_id: str, algorithm: str = 'dijkstra') -> Tuple[List[str], float, float]:
        """Find the shortest path between two nodes.
        
        Args:
            start_id: The ID of the starting node
            end_id: The ID of the ending node
            algorithm: 'dijkstra' or 'a_star'
            
        Returns:
            Tuple of (path_node_ids, total_distance_meters, estimated_time_minutes)
        """
        print(f"find_path called with algorithm: '{algorithm}'")
        
        if start_id not in self.nodes:
            raise ValueError(f"Start node '{start_id}' not found")
        if end_id not in self.nodes:
            raise ValueError(f"End node '{end_id}' not found")
            
        # Same node - return immediately
        if start_id == end_id:
            return [start_id], 0, 0
            
        # Select algorithm
        if algorithm == 'a_star':
            print("Using A* algorithm")
            return self._a_star_search(start_id, end_id)
        else:  # Default to Dijkstra
            print("Using Dijkstra algorithm")
            return self._dijkstra_search(start_id, end_id)

    def _dijkstra_search(self, start_id: str, end_id: str) -> Tuple[List[str], float, float]:
        """Implement Dijkstra's algorithm for pathfinding."""
        print(f"Starting Dijkstra search from {start_id} to {end_id}")
        start_time = time.time()
        
        # Reset node costs
        for node in self.nodes.values():
            node.g_cost = float('inf')
            node.parent = None
            
        start_node = self.nodes[start_id]
        end_node = self.nodes[end_id]
        
        # Set start node cost to 0
        start_node.g_cost = 0

        # Priority queue for nodes to visit
        open_set = []
        heapq.heappush(open_set, PriorityNode(priority=0, node_id=start_id))
        
        # Keep track of visited nodes
        closed_set = set()
        
        # Performance optimization: Only consider cities within a reasonable distance
        # Calculate straight-line distance between start and end
        direct_distance = self._haversine_distance(start_node, end_node)
        # Set a max radius to consider (1.5x the direct distance)
        max_radius = max(direct_distance * 1.5, 500000)  # At least 500km radius
        
        # Build a list of candidate nodes that are within reasonable distance
        candidate_nodes = {}
        for node_id, node in self.nodes.items():
            # Always include start and end nodes
            if node_id == start_id or node_id == end_id:
                candidate_nodes[node_id] = node
                continue
                
            # Check if this node is within reasonable distance from either start or end
            dist_to_start = self._haversine_distance(start_node, node)
            dist_to_end = self._haversine_distance(end_node, node)
            
            # If node is within reasonable distance of either start or end, include it
            if dist_to_start <= max_radius or dist_to_end <= max_radius:
                candidate_nodes[node_id] = node
                
        print(f"Considering {len(candidate_nodes)} nodes out of {len(self.nodes)} total nodes")
        
        nodes_processed = 0
        while open_set:
            # Get node with lowest cost
            current_id = heapq.heappop(open_set).node_id
            nodes_processed += 1
            
            # Performance check - if taking too long, report progress
            if nodes_processed % 10 == 0:
                elapsed = time.time() - start_time
                if elapsed > 10:  # If more than 10 seconds have passed
                    print(f"Processed {nodes_processed} nodes, current distance: {self.nodes[current_id].g_cost/1000:.1f}km")
            
            # Skip if already processed
            if current_id in closed_set:
                 continue

            current_node = self.nodes[current_id]

            # Reached end node
            if current_id == end_id:
                print(f"Path found! Processed {nodes_processed} nodes in {time.time() - start_time:.2f} seconds")
                break

            # Mark as visited
            closed_set.add(current_id)
            
            # Explore neighbors (only consider candidates within our radius)
            for neighbor_id, neighbor_node in candidate_nodes.items():
                if neighbor_id in closed_set:
                    continue

                # Get distance between current and neighbor
                distance = self.get_driving_distance(current_node, neighbor_node)
                if distance is None:
                    continue  # Skip if no valid distance
                    
                # Calculate new cost
                new_cost = current_node.g_cost + distance
                
                # Update if better path found
                if new_cost < neighbor_node.g_cost:
                    neighbor_node.g_cost = new_cost
                    neighbor_node.parent = current_node
                    heapq.heappush(open_set, PriorityNode(priority=new_cost, node_id=neighbor_id))
        
        # Reconstruct path
        if end_node.parent is None and start_id != end_id:
            print(f"No path found after processing {nodes_processed} nodes")
            return [], 0, 0  # No path found
            
        path = []
        current = end_node
        total_distance = end_node.g_cost
        
        while current:
            path.append(current.id)
            current = current.parent
            
        # Reverse to get path from start to end
        path.reverse()
        
        # Estimate time (assuming average speed of 50 km/h = 833.33 m/min)
        avg_speed_meters_per_min = 833.33
        estimated_time_mins = total_distance / avg_speed_meters_per_min
        
        print(f"Path found with {len(path)} nodes, {total_distance/1000:.1f}km, {estimated_time_mins:.1f} minutes")
        return path, total_distance, estimated_time_mins

    def _a_star_search(self, start_id: str, end_id: str) -> Tuple[List[str], float, float]:
        """Implement A* algorithm for pathfinding."""
        print(f"Starting A* search from {start_id} to {end_id}")
        start_time = time.time()
        
        # Reset node costs
        for node in self.nodes.values():
            node.g_cost = float('inf')
            node.h_cost = 0
            node.parent = None
            
        start_node = self.nodes[start_id]
        end_node = self.nodes[end_id]
        
        # Set start node cost to 0
        start_node.g_cost = 0
        # Set heuristic for start node (straight-line distance to end)
        start_node.h_cost = self._haversine_distance(start_node, end_node)
        
        # Priority queue for nodes to visit
        open_set = []
        heapq.heappush(open_set, PriorityNode(priority=start_node.f_cost, node_id=start_id))
        
        # Keep track of visited nodes
        closed_set = set()
        
        # Performance optimization: Only consider cities within a reasonable distance
        # Calculate straight-line distance between start and end
        direct_distance = self._haversine_distance(start_node, end_node)
        # Set a max radius to consider (1.5x the direct distance)
        max_radius = max(direct_distance * 1.5, 500000)  # At least 500km radius
        
        # Build a list of candidate nodes that are within reasonable distance
        candidate_nodes = {}
        for node_id, node in self.nodes.items():
            # Always include start and end nodes
            if node_id == start_id or node_id == end_id:
                candidate_nodes[node_id] = node
                continue

            # Check if this node is within reasonable distance from either start or end
            dist_to_start = self._haversine_distance(start_node, node)
            dist_to_end = self._haversine_distance(end_node, node)
            
            # If node is within reasonable distance of either start or end, include it
            if dist_to_start <= max_radius or dist_to_end <= max_radius:
                candidate_nodes[node_id] = node
                
        print(f"Considering {len(candidate_nodes)} nodes out of {len(self.nodes)} total nodes")
        
        nodes_processed = 0
        while open_set:
            # Get node with lowest f_cost
            current_id = heapq.heappop(open_set).node_id
            nodes_processed += 1
            
            # Performance check - if taking too long, report progress
            if nodes_processed % 10 == 0:
                elapsed = time.time() - start_time
                if elapsed > 10:  # If more than 10 seconds have passed
                    print(f"Processed {nodes_processed} nodes, current distance: {self.nodes[current_id].g_cost/1000:.1f}km")
            
            # Skip if already processed
            if current_id in closed_set:
                     continue

            current_node = self.nodes[current_id]
            
            # Reached end node
            if current_id == end_id:
                print(f"Path found! Processed {nodes_processed} nodes in {time.time() - start_time:.2f} seconds")
                break
                
            # Mark as visited
            closed_set.add(current_id)
            
            # Explore neighbors (only consider candidates within our radius)
            for neighbor_id, neighbor_node in candidate_nodes.items():
                if neighbor_id in closed_set:
                    continue
                    
                # Get distance between current and neighbor
                distance = self.get_driving_distance(current_node, neighbor_node)
                if distance is None:
                    continue  # Skip if no valid distance
                    
                # Calculate new cost
                new_g_cost = current_node.g_cost + distance
                
                # Update if better path found
                if new_g_cost < neighbor_node.g_cost:
                    neighbor_node.g_cost = new_g_cost
                    # Set heuristic (straight-line distance to end)
                    neighbor_node.h_cost = self._haversine_distance(neighbor_node, end_node)
                    neighbor_node.parent = current_node
                    heapq.heappush(open_set, PriorityNode(priority=neighbor_node.f_cost, node_id=neighbor_id))
        
        # Reconstruct path
        if end_node.parent is None and start_id != end_id:
            print(f"No path found after processing {nodes_processed} nodes")
            return [], 0, 0  # No path found
            
        path = []
        current = end_node
        total_distance = end_node.g_cost
        
        while current:
            path.append(current.id)
            current = current.parent
            
        # Reverse to get path from start to end
        path.reverse()
        
        # Estimate time (assuming average speed of 50 km/h = 833.33 m/min)
        avg_speed_meters_per_min = 833.33
        estimated_time_mins = total_distance / avg_speed_meters_per_min
        
        print(f"Path found with {len(path)} nodes, {total_distance/1000:.1f}km, {estimated_time_mins:.1f} minutes")
        return path, total_distance, estimated_time_mins

    def get_all_states(self) -> List[str]:
        """Return a list of all available states."""
        return self.states

    def get_cities_by_state(self, state_name: str) -> List[str]:
        """Return a list of cities for a given state."""
        if state_name not in self.cities_by_state:
            return []
        return self.cities_by_state[state_name] 