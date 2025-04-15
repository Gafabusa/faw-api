from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import base64
import tempfile
from werkzeug.utils import secure_filename
from model_utils import detector
from map.detector_adapter import DetectorAdapter

app = Flask(__name__, 
            template_folder='map/templates',
            static_folder='map/static')

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize detector adapter
detector_adapter = DetectorAdapter()

@app.route('/')
def index():
    """Serve the main page with the map"""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Original detection endpoint without location tracking"""
    # Check if the file part is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    # Ensure that a file is uploaded
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Save the file temporarily
        temp_path = "temp_image.jpg"
        file.save(temp_path)
        
        # Run detection
        results = detector.detect(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/districts')
def get_districts():
    """Get all districts for the map"""
    districts = detector_adapter.get_all_districts()
    return jsonify(districts)

@app.route('/api/detections')
def get_detections():
    """Get detection data for the map"""
    detections = detector_adapter.get_detection_map_data()
    return jsonify(detections)

@app.route('/api/detect_with_location', methods=['POST'])
def detect_with_location():
    """
    Enhanced API endpoint for Flutter app that:
    1. Accepts image as base64 string
    2. Uses provided GPS coordinates to determine district
    """
    data = request.json
    
    # Check if all required data is provided
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Check for image data
    if 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400
    
    # Check for location data
    if 'latitude' not in data or 'longitude' not in data:
        return jsonify({"error": "Location data (latitude and longitude) is required"}), 400
    
    try:
        # Extract location data
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        
        # Find the nearest district based on coordinates
        district = detector_adapter.find_nearest_district(latitude, longitude)
        
        if not district:
            return jsonify({"error": "Could not determine district from coordinates"}), 400
        
        # Decode base64 image
        image_data = data['image']
        if 'data:image' in image_data:  # Handle data URI scheme
            image_data = image_data.split(',')[1]
        
        # Save image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(base64.b64decode(image_data))
            temp_path = temp_file.name
        
        # Run detection and record location
        result = detector_adapter.detect_and_record(temp_path, district)
        
        # Add district information to the result
        result['district'] = district
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
