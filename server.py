from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import traceback

try:
    import config  # Import the config file
    print("Successfully imported config module")
except Exception as e:
    print(f"Error importing config: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from pathfinding import PathFinder  # Import the PathFinder class
    print("Successfully imported PathFinder class")
except Exception as e:
    print(f"Error importing PathFinder: {e}")
    traceback.print_exc()
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
CORS(app)  # Enable Cross-Origin Resource Sharing

print("Flask app initialized")

# Initialize PathFinder
pathfinder_instance = None
try:
    print(f"Attempting to initialize PathFinder with API key: {config.GOOGLE_MAPS_API_KEY[:5]}...")
    pathfinder_instance = PathFinder(config.GOOGLE_MAPS_API_KEY)
    print("\n===== INITIALIZATION INFO =====")
    print("Available states:", pathfinder_instance.get_all_states())
    print("Example cities for Madhya Pradesh:", pathfinder_instance.get_cities_by_state("Madhya Pradesh"))
    print("First 10 node IDs:", list(pathfinder_instance.nodes.keys())[:10])
    print("==============================\n")
except ValueError as e:
    print(f"FATAL ERROR initializing PathFinder: {e}")
    traceback.print_exc()
    pathfinder_instance = None
except RuntimeError as e:
    print(f"FATAL ERROR initializing Google Maps client: {e}")
    traceback.print_exc()
    pathfinder_instance = None
except Exception as e:
    print(f"An unexpected FATAL ERROR occurred during PathFinder initialization: {e}")
    traceback.print_exc()
    pathfinder_instance = None

# Basic Page Routes
@app.route('/')
def index():
    # Pass API key to template if needed for frontend maps
    return render_template('index.html', google_maps_api_key=config.GOOGLE_MAPS_API_KEY)

@app.route('/about')
def about():
    return render_template('about.html', google_maps_api_key=config.GOOGLE_MAPS_API_KEY)

@app.route('/pathfinder')
def pathfinder_page():
    return render_template('pathfinder.html', google_maps_api_key=config.GOOGLE_MAPS_API_KEY)

@app.route('/learn')
def learn():
    return render_template('learn.html', google_maps_api_key=config.GOOGLE_MAPS_API_KEY)

# Serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# API Routes
@app.route('/api/states', methods=['GET'])
def get_states():
    """API endpoint to get the list of available states."""
    if not pathfinder_instance:
        return jsonify({"error": "Pathfinder service not available"}), 503
    try:
        states = pathfinder_instance.get_all_states()
        return jsonify(states)
    except Exception as e:
        print(f"Error in /api/states: {e}")
        return jsonify({"error": "Internal server error fetching states"}), 500

@app.route('/api/cities/<state_name>', methods=['GET'])
def get_cities(state_name):
    """API endpoint to get cities for a specific state."""
    if not pathfinder_instance:
        return jsonify({"error": "Pathfinder service not available"}), 503
    if not state_name:
        return jsonify({"error": "State name not provided"}), 400

    try:
        # Basic sanitization
        safe_state_name = state_name.strip()
        cities = pathfinder_instance.get_cities_by_state(safe_state_name)
        return jsonify(cities)
    except Exception as e:
        print(f"Error in /api/cities/{state_name}: {e}")
        return jsonify({"error": f"Internal server error fetching cities for {state_name}"}), 500

@app.route('/api/find_path', methods=['POST'])
def find_path_api():
    """API endpoint to find the path between two cities."""
    if not pathfinder_instance:
        return jsonify({"error": "Pathfinder service not available"}), 503

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    start_id = data.get('start_id')
    end_id = data.get('end_id')
    algorithm = data.get('algorithm', 'dijkstra')  # Default to dijkstra
    
    print(f"Received path request with start_id={start_id}, end_id={end_id}, algorithm={algorithm}")
    print(f"Available nodes: {list(pathfinder_instance.nodes.keys())[:10]}... (showing first 10)")

    # Input Validation
    required_fields = ['start_id', 'end_id']
    if not all(field in data for field in required_fields):
        missing = [field for field in required_fields if field not in data]
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    if not isinstance(start_id, str) or not isinstance(end_id, str):
        return jsonify({"error": "start_id and end_id must be strings"}), 400

    # Validate ID format (simple check)
    if '_' not in start_id or '_' not in end_id:
        return jsonify({"error": "Invalid ID format. Expected 'city_state'."}), 400

    if algorithm not in ['dijkstra', 'a_star']:
        return jsonify({"error": "Invalid algorithm. Choose 'dijkstra' or 'a_star'."}), 400

    print(f"API Request: Find path from {start_id} to {end_id} using {algorithm}")

    # Call Pathfinding Logic
    try:
        import threading
        import time
        
        # Check if the nodes exist first
        if start_id not in pathfinder_instance.nodes:
            print(f"Error: Start node '{start_id}' not found in initialized nodes.")
            potential_matches = [node_id for node_id in pathfinder_instance.nodes.keys() 
                               if node_id.startswith(start_id.split('_')[0])]
            suggestion = f"Did you mean one of: {', '.join(potential_matches[:3])}" if potential_matches else ""
            return jsonify({"error": f"Start city '{start_id}' not found. {suggestion}"}), 404
            
        if end_id not in pathfinder_instance.nodes:
            print(f"Error: End node '{end_id}' not found in initialized nodes.")
            potential_matches = [node_id for node_id in pathfinder_instance.nodes.keys() 
                               if node_id.startswith(end_id.split('_')[0])]
            suggestion = f"Did you mean one of: {', '.join(potential_matches[:3])}" if potential_matches else ""
            return jsonify({"error": f"End city '{end_id}' not found. {suggestion}"}), 404
        
        # Create a timeout mechanism
        result = {"path": None, "distance": 0, "time": 0, "error": None}
        
        def pathfind_with_timeout():
            try:
                print(f"Starting pathfinding with algorithm: {algorithm}")
                start_time = time.time()
                
                path, distance, time_mins = pathfinder_instance.find_path(
                    start_id=start_id,
                    end_id=end_id,
                    algorithm=algorithm
                )
                
                end_time = time.time()
                print(f"Pathfinding completed in {end_time - start_time:.2f} seconds")
                
                result["path"] = path
                result["distance"] = distance
                result["time"] = time_mins
            except Exception as e:
                result["error"] = str(e)
                print(f"Error in pathfinding thread: {e}")
                import traceback
                traceback.print_exc()
        
        # Start pathfinding in a thread with a timeout
        pathfinding_thread = threading.Thread(target=pathfind_with_timeout)
        pathfinding_thread.daemon = True
        pathfinding_thread.start()
        
        # Wait for the thread to complete (with timeout)
        max_wait_time = 60  # seconds (increased from 25)
        wait_interval = 0.5  # seconds
        elapsed = 0
        
        while pathfinding_thread.is_alive() and elapsed < max_wait_time:
            time.sleep(wait_interval)
            elapsed += wait_interval
            
        if pathfinding_thread.is_alive():
            # Thread is still running after timeout
            return jsonify({
                "error": "Path calculation timed out. The cities you selected might be too far apart or require a complex route. Try cities that are closer together or use the A* algorithm for better performance."
            }), 408
            
        if result["error"]:
            return jsonify({"error": result["error"]}), 500
            
        if not result["path"] and start_id != end_id:
            # Path finding returned empty, but wasn't start == end
            return jsonify({"error": f"No path found between {start_id} and {end_id}"}), 404

        # Prepare coordinates dictionary for the frontend
        coordinates = {}
        for node_id in result["path"]:
            if node_id in pathfinder_instance.nodes:
                node = pathfinder_instance.nodes[node_id]
                coordinates[node_id] = {
                    "lat": node.lat,
                    "lng": node.lng,
                    "name": node.name
                }

        return jsonify({
            "path": result["path"],
            "distance": result["distance"],  # In meters
            "time": result["time"],          # In minutes
            "coordinates": coordinates       # City coordinates for map display
        })

    except ValueError as e:
        # Handle errors like node not found from PathFinder
        print(f"ValueError in find_path: {e}")
        return jsonify({"error": str(e)}), 404  # Use 404 for 'not found' type errors
    except Exception as e:
        # Catch unexpected errors during pathfinding
        print(f"Unexpected error during find_path for {start_id} to {end_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred during path calculation."}), 500

# Run the App
if __name__ == '__main__':
    print("Starting Flask application...")
    # Set debug=False in production
    app.run(debug=True, host='0.0.0.0', port=5000) 