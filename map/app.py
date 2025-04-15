from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from location_detector import LocationAwareDetector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize detector
detector = LocationAwareDetector()

@app.route('/')
def index():
    """Serve the main page with the map"""
    return render_template('index.html')

@app.route('/api/districts')
def get_districts():
    """Get all districts for the map"""
    districts = detector.get_all_districts()
    return jsonify(districts)

@app.route('/api/detections')
def get_detections():
    """Get detection data for the map"""
    detections = detector.get_detection_map_data()
    return jsonify(detections)

@app.route('/api/detect', methods=['POST'])
def detect_armyworm():
    """Handle image upload and detection"""
    # Check if district is provided
    if 'district' not in request.form:
        return jsonify({'error': 'District name is required'}), 400
    
    district_name = request.form['district']
    
    # Check if image is provided
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    if file:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Run detection and record location
        result = detector.detect_and_record(file_path, district_name)
        
        return jsonify(result)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
