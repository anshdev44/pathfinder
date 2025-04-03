import heapq
from typing import Dict, List, Tuple, Set, Optional
import googlemaps
from dataclasses import dataclass, field
from math import radians, sin, cos, sqrt, atan2
import time
import signal

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
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            raise ValueError("API key is missing or placeholder. Please provide a valid Google Maps API key.")
        try:
            self.gmaps = googlemaps.Client(key=api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Google Maps client: {e}")

        self.nodes: Dict[str, Node] = {}
        # Cache distances to avoid repeated API calls: (node1_id, node2_id) -> distance_meters
        self.distances: Dict[Tuple[str, str], Optional[float]] = {}
        # Define cities by state (You can expand this list)
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
            # Add more states and cities as needed
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
            # Add more coordinates as needed
        }
        self.initialize_nodes()

    def _format_id(self, city: str, state: str) -> str:
        """Creates a standardized ID from city and state."""
        city_part = city.lower().replace(' ', '').replace('.', '').replace('-', '')
        state_part = state.lower().replace(' ', '').replace('.', '').replace('-', '')
        city_id = f"{city_part}_{state_part}"
        print(f"Formatting ID: {city}, {state} -> {city_id}")
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
                    # print(f"Using known coordinates for {display_name}")
                else:
                    # print(f"Fetching coordinates for {display_name}...")
                    try:
                        geocode_result = self.gmaps.geocode(f"{city}, {state}, India")
                        if geocode_result:
                            location = geocode_result[0]['geometry']['location']
                            lat, lng = location['lat'], location['lng']
                            # print(f" -> Got coordinates: {lat}, {lng}")
                            # Add to known coordinates for future use (optional)
                            # self.known_coordinates[city_id] = {'lat': lat, 'lng': lng}
                        else:
                            print(f"Warning: Could not geocode {display_name}. Skipping.")
                            continue
                        time.sleep(0.05) # Small delay to respect API rate limits potentially
                    except Exception as e:
                        print(f"Error geocoding {display_name}: {e}. Skipping.")
                        continue

                if lat is not None and lng is not None:
                    self.nodes[city_id] = Node(id=city_id, name=display_name, lat=lat, lng=lng)
                    nodes_added += 1

        print(f"Node initialization complete. Added {nodes_added} nodes.")
        if not self.nodes:
            print("Warning: No nodes were initialized. Check city/state data and API key.")


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
        return distance_km * 1000 # Return distance in meters

    def get_driving_distance(self, node1: Node, node2: Node) -> Optional[float]:
        """Get driving distance in meters using Google Maps Distance Matrix API."""
        if node1.id == node2.id:
            return 0.0

        # Use tuple sorted by id for consistent caching key
        pair_key = tuple(sorted((node1.id, node2.id)))

        if pair_key in self.distances:
            # print(f"Cache hit for distance: {node1.name} <-> {node2.name}")
            return self.distances[pair_key]

        # Straight-line distance as initial approximation
        haversine_dist = self._haversine_distance(node1, node2)
        
        # For very far cities (e.g., > 1000km straight-line), don't even try the API call
        if haversine_dist > 1000000:  # 1000 km in meters
            print(f"Cities too far apart ({haversine_dist/1000:.1f} km), using Haversine: {node1.name} <-> {node2.name}")
            self.distances[pair_key] = haversine_dist
            return haversine_dist
            
        # print(f"API call for distance: {node1.name} <-> {node2.name}")
        try:
            # Set a timeout for the API call
            import threading
            import time
            
            class APITimeoutError(Exception):
                pass
                
            # Use a thread with timeout instead of signals (works on all systems)
            result_container = {'result': None, 'error': None}
            
            def api_call_thread():
                try:
                    result = self.gmaps.distance_matrix(
                        origins=[(node1.lat, node1.lng)],
                        destinations=[(node2.lat, node2.lng)],
                        mode='driving'
                    )
                    result_container['result'] = result
                except Exception as e:
                    result_container['error'] = e
            
            # Start thread for API call
            api_thread = threading.Thread(target=api_call_thread)
            api_thread.daemon = True
            api_thread.start()
            
            # Wait with timeout
            api_thread.join(timeout=5.0)  # 5 second timeout
            
            if api_thread.is_alive():
                # Thread still running after timeout
                print(f"API call timed out for {node1.name} to {node2.name}. Falling back to Haversine.")
                self.distances[pair_key] = haversine_dist
                return haversine_dist
                
            if result_container['error']:
                # Thread had an error
                raise result_container['error']
                
            # Process result
            result = result_container['result']
            if (result['status'] == 'OK' and
                result['rows'][0]['elements'][0]['status'] == 'OK'):
                distance_meters = result['rows'][0]['elements'][0]['distance']['value']
                self.distances[pair_key] = float(distance_meters)
                # print(f" -> Got distance: {distance_meters} m")
                return float(distance_meters)
            else:
                print(f"Warning: Distance Matrix API status not OK for {node1.name} to {node2.name}. Status: {result['rows'][0]['elements'][0]['status']}. Falling back to Haversine.")
                self.distances[pair_key] = haversine_dist  # Cache Haversine distance
                return haversine_dist
                
        except Exception as e:
            print(f"Error calling Distance Matrix API for {node1.name} to {node2.name}: {e}. Falling back to Haversine.")
            self.distances[pair_key] = haversine_dist  # Cache Haversine distance
            return haversine_dist

    def get_effective_distance(self, node1: Node, node2: Node) -> float:
        """Gets driving distance, falls back to Haversine if API fails or returns no route."""
        driving_dist = self.get_driving_distance(node1, node2)
        if driving_dist is not None:
            return driving_dist
        else:
            # Fallback to straight-line distance if driving distance fails
            return self._haversine_distance(node1, node2)


    def heuristic(self, node: Node, end_node: Node) -> float:
        """Heuristic function for A* (using Haversine distance as estimate)."""
        # Heuristic should estimate the *remaining* cost.
        # Using Haversine (straight-line) distance is a common admissible heuristic.
        return self._haversine_distance(node, end_node)

    def _reconstruct_path(self, end_node: Node) -> List[Node]:
        """Backtrack from end node to start node using parent pointers."""
        path = []
        current = end_node
        while current is not None:
            path.append(current)
            current = current.parent
        return list(reversed(path)) # Return path from start to end

    def dijkstra(self, start_id: str, end_id: str) -> List[Node]:
        """Find shortest path using Dijkstra's algorithm."""
        if start_id not in self.nodes or end_id not in self.nodes:
            raise ValueError(f"Start ({start_id}) or end ({end_id}) node not found in initialized nodes.")

        start_node = self.nodes[start_id]
        end_node = self.nodes[end_id]

        # Reset costs and parents for all nodes
        for node in self.nodes.values():
            node.g_cost = float('inf')
            node.parent = None
        start_node.g_cost = 0

        # Priority queue stores (cost, node_id)
        pq = [PriorityNode(priority=0, node_id=start_id)]
        visited: Set[str] = set() # Keep track of visited nodes by ID

        while pq:
            # Get node with the lowest cost
            current_priority_node = heapq.heappop(pq)
            current_cost = current_priority_node.priority
            current_node_id = current_priority_node.node_id

            # Optimization: If we already found a shorter path to this node, skip
            if current_node_id in visited or current_cost > self.nodes[current_node_id].g_cost:
                 continue

            current_node = self.nodes[current_node_id]
            visited.add(current_node_id)

            # If we reached the destination
            if current_node == end_node:
                break

            # Explore neighbors
            for neighbor_id, neighbor_node in self.nodes.items():
                if neighbor_id == current_node_id or neighbor_id in visited:
                    continue # Don't revisit self or already finalized nodes

                distance = self.get_effective_distance(current_node, neighbor_node)
                if distance == float('inf'): # Should not happen with fallback, but safety check
                    continue

                new_cost = current_node.g_cost + distance
                if new_cost < neighbor_node.g_cost:
                    neighbor_node.g_cost = new_cost
                    neighbor_node.parent = current_node
                    heapq.heappush(pq, PriorityNode(priority=new_cost, node_id=neighbor_id))

        # Reconstruct path if end node was reached
        if end_node.parent is None and start_node != end_node:
             print(f"Warning: Dijkstra could not find a path from {start_node.name} to {end_node.name}")
             return [] # No path found
        return self._reconstruct_path(end_node)


    def a_star(self, start_id: str, end_id: str) -> List[Node]:
        """Find shortest path using A* algorithm."""
        if start_id not in self.nodes or end_id not in self.nodes:
            raise ValueError(f"Start ({start_id}) or end ({end_id}) node not found in initialized nodes.")

        start_node = self.nodes[start_id]
        end_node = self.nodes[end_id]

        # Reset costs and parents
        for node in self.nodes.values():
            node.g_cost = float('inf')
            node.h_cost = 0
            node.parent = None
        start_node.g_cost = 0
        start_node.h_cost = self.heuristic(start_node, end_node) # Calculate heuristic for start

        # Priority queue stores (f_cost, node_id)
        # Using PriorityNode dataclass for clarity and stability if f_costs are equal
        open_set_pq = [PriorityNode(priority=start_node.f_cost, node_id=start_id)]
        # Set to keep track of nodes currently in the priority queue (by id) for quick lookups
        open_set_ids: Set[str] = {start_id}
        # Set to keep track of nodes already processed (by id)
        closed_set: Set[str] = set()

        while open_set_pq:
            # Get node with the lowest f_cost
            current_priority_node = heapq.heappop(open_set_pq)
            current_node_id = current_priority_node.node_id

            # If node already processed, skip
            if current_node_id in closed_set:
                continue

            current_node = self.nodes[current_node_id]

            # Goal reached
            if current_node == end_node:
                return self._reconstruct_path(end_node)

            # Move current node from open to closed set
            open_set_ids.remove(current_node_id)
            closed_set.add(current_node_id)

            # Explore neighbors
            for neighbor_id, neighbor_node in self.nodes.items():
                 if neighbor_id == current_node_id or neighbor_id in closed_set:
                    continue # Skip self and already processed nodes

                 distance = self.get_effective_distance(current_node, neighbor_node)
                 if distance == float('inf'): # Skip unreachable neighbors
                     continue

                 tentative_g_cost = current_node.g_cost + distance

                 # If this path to neighbor is better than any previous one
                 if tentative_g_cost < neighbor_node.g_cost:
                     neighbor_node.parent = current_node
                     neighbor_node.g_cost = tentative_g_cost
                     neighbor_node.h_cost = self.heuristic(neighbor_node, end_node)
                     # f_cost is calculated via property

                     # If neighbor not in open set, add it
                     if neighbor_id not in open_set_ids:
                         heapq.heappush(open_set_pq, PriorityNode(priority=neighbor_node.f_cost, node_id=neighbor_id))
                         open_set_ids.add(neighbor_id)
                     else:
                         # If already in open set, update its priority if this path is better
                         # This requires finding and updating the element in the heap, which is inefficient.
                         # A common optimization is to just push the new, lower-cost entry.
                         # The higher-cost entry will eventually be popped but skipped because
                         # the node will already be in closed_set or its g_cost will be higher.
                         heapq.heappush(open_set_pq, PriorityNode(priority=neighbor_node.f_cost, node_id=neighbor_id))


        print(f"Warning: A* could not find a path from {start_node.name} to {end_node.name}")
        return [] # No path found


    def get_path_details(self, path: List[Node]) -> Tuple[float, float]:
        """Calculate total distance (meters) and estimated time (minutes) for a given path."""
        if not path or len(path) < 2:
            return 0.0, 0.0 # No distance or time for empty or single-node path

        total_distance_meters = 0.0
        for i in range(len(path) - 1):
            dist = self.get_effective_distance(path[i], path[i+1])
            if dist == float('inf'):
                 print(f"Warning: Could not calculate distance between {path[i].name} and {path[i+1].name} in final path.")
                 # Decide how to handle this - maybe raise error or return infinity?
                 # For now, we'll add 0, but this indicates an issue.
                 dist = 0.0
            total_distance_meters += dist


        # Estimate time: very rough estimate, assumes avg 60 km/h driving speed
        # Google Distance Matrix API *can* return duration, but that's another API call per segment.
        # For simplicity here, we estimate based on distance.
        # Speed in m/min = 60 km/h * 1000 m/km / 60 min/h = 1000 m/min
        if total_distance_meters > 0:
             estimated_time_minutes = total_distance_meters / 1000.0
        else:
             estimated_time_minutes = 0.0

        return total_distance_meters, estimated_time_minutes

    def find_path(self, start_id: str, end_id: str, algorithm: str = 'dijkstra') -> Tuple[List[Dict], float, float]:
        """
        Find path between two nodes using specified algorithm.

        Returns:
            Tuple containing:
            - List of nodes in the path (dict with id, name, lat, lng)
            - Total distance in meters
            - Estimated time in minutes
        """
        print(f"Finding path from {start_id} to {end_id} using {algorithm}...")
        start_time = time.time()

        if algorithm.lower() == 'a_star':
            path_nodes = self.a_star(start_id, end_id)
        elif algorithm.lower() == 'dijkstra':
            path_nodes = self.dijkstra(start_id, end_id)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}. Choose 'dijkstra' or 'a_star'.")

        if not path_nodes:
            print("No path found.")
            return [], 0.0, 0.0 # Return empty path if none found

        total_distance, estimated_time = self.get_path_details(path_nodes)

        # Format path for JSON response
        path_for_json = [
            {"id": node.id, "name": node.name, "lat": node.lat, "lng": node.lng}
            for node in path_nodes
        ]

        end_time = time.time()
        print(f"Path found in {end_time - start_time:.4f} seconds. Distance: {total_distance/1000:.2f} km, Time: {estimated_time:.2f} min.")

        return path_for_json, total_distance, estimated_time

    def get_all_states(self) -> List[str]:
        """Get list of available states."""
        return sorted(self.states)

    def get_cities_by_state(self, state_name: str) -> List[str]:
        """Get list of cities for a given state."""
        return sorted(self.cities_by_state.get(state_name, []))

    def get_neighbors(self, node: Node) -> List[Tuple[Node, float]]:
        """Get all neighbors of a node with their distances.
        Optimization: Only consider nodes within a reasonable distance as neighbors.
        """
        MAX_NEIGHBORS = 5  # Limit to closest 5 neighbors
        MAX_DISTANCE_KM = 500  # Only consider cities within 500km as potential neighbors

        # First, filter potential neighbors using a quick distance calculation
        potential_neighbors = []
        for other_id, other_node in self.nodes.items():
            if other_id == node.id:
                continue
                
            # Quick distance check (straight-line) to filter distant nodes
            approx_dist = self._haversine_distance(node, other_node) / 1000  # Convert to km
            
            if approx_dist <= MAX_DISTANCE_KM:
                potential_neighbors.append((other_node, approx_dist))
        
        # Sort potential neighbors by approximate distance
        potential_neighbors.sort(key=lambda x: x[1])
        
        # Take only the closest MAX_NEIGHBORS
        closest_neighbors = potential_neighbors[:MAX_NEIGHBORS]
        
        # Now calculate actual driving distances for the closest neighbors
        neighbors_with_distances = []
        for neighbor_node, _ in closest_neighbors:
            distance = self.get_effective_distance(node, neighbor_node)
            neighbors_with_distances.append((neighbor_node, distance))
            
        return neighbors_with_distances

# Example Usage (optional - for testing)
if __name__ == "__main__":
    import config  # Assuming config.py is in the same directory

    if config.GOOGLE_MAPS_API_KEY == "AIzaSyCZ-ONBo_Q8bJRm8yAoF8N2m_I6wOnTtF0":
        print("Please set your Google Maps API key in config.py before running the example.")
    else:
        try:
            finder = PathFinder(config.GOOGLE_MAPS_API_KEY)

            # Example: Find path from Lucknow to Mumbai
            start_city_id = finder._format_id("Lucknow", "Uttar Pradesh")
            end_city_id = finder._format_id("Mumbai", "Maharashtra")

            if start_city_id in finder.nodes and end_city_id in finder.nodes:
                 print("\n--- Testing Dijkstra ---")
                 path_d, dist_d, time_d = finder.find_path(start_city_id, end_city_id, 'dijkstra')
                 print("\n--- Testing A* ---")
                 path_a, dist_a, time_a = finder.find_path(start_city_id, end_city_id, 'a_star')

            else:
                 print(f"Could not run example: Start node '{start_city_id}' or end node '{end_city_id}' not found.")
                 print("Available nodes:", list(finder.nodes.keys()))

        except ValueError as ve:
             print(f"Configuration Error: {ve}")
        except Exception as e:
             print(f"An error occurred during example execution: {e}") 