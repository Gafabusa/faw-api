# Fall Armyworm Detection Map for Uganda

This application allows farmers to upload images of maize leaves for fall armyworm detection and displays the results on a map of Uganda, showing where different stages of fall armyworm have been detected.

## Features

- Image-based detection of fall armyworm on maize leaves
- Location tracking of detections across Uganda
- Interactive map showing detection hotspots
- Different colors for different stages of fall armyworm infestation
- Simple web interface for farmers to upload images

## Setup Instructions

1. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the setup script to create the database and populate districts:
   ```
   python setup.py
   ```

3. Start the application:
   ```
   python app.py
   ```

4. Open a web browser and navigate to:
   ```
   http://localhost:5000
   ```

## System Requirements

- Python 3.7 or higher
- TensorFlow Lite
- OpenCV
- Flask
- SQLite

## Project Structure

- `app.py` - Main application file
- `database_schema.py` - Database schema and operations
- `fall_armyworm_detector.py` - Original detector code
- `location_detector.py` - Location-aware detector wrapper
- `populate_districts.py` - Script to populate Uganda districts
- `setup.py` - Setup script
- `templates/` - HTML templates
- `uploads/` - Directory for uploaded images
- `detections.db` - SQLite database for storing detections
```

## Step 10: Create a file for the maize leaf classifier

Since your original code references a `MaizeLeafClassifier` class, we need to create this file:

```python:maize_leaf_detector.py
import cv2
import numpy as np
import tensorflow.lite as tflite
import os

class MaizeLeafClassifier:
    def __init__(self, model_path="maize_leaf_classifier.tflite"):
        self.model_path = model_path
        
        # Check if model exists
        if not os.path.exists(model_path):
            print(f"Warning: Maize leaf classifier model not found at {model_path}")
            print("Using dummy classifier for demonstration purposes")
            self.use_dummy = True
        else:
            self.use_dummy = False
            # Load the TFLite model
            self.interpreter = tflite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            # Get input and output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            # Get input shape
            self.input_shape = self.input_details[0]['shape']
            self.img_size = (self.input_shape[1], self.input_shape[2])
    
    def preprocess_image(self, image_path):
        """Preprocess the image for the model"""
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image at {image_path}")
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image to model input size
        image = cv2.resize(image, self.img_size)
        
        # Normalize pixel values
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def classify(self, image_path):
        """Classify if the image contains a maize leaf"""
        # If using dummy classifier, return a positive result most of the time
        if self.use_dummy:
            # For demonstration, return positive 90% of the time
            is_maize = np.random.random() < 0.9
            confidence = np.random.uniform(0.7, 0.99) if is_maize else np.random.uniform(0.5, 0.7)
            return {
                "is_maize": is_maize,
                "confidence": confidence
            }
        
        # Preprocess image
        image = self.preprocess_image(image_path)
        
        # Set input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        
        # Run inference
        self.interpreter.invoke()
        
        # Get output tensor
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        # Process output
        # Assuming binary classification (maize leaf or not)
        confidence = float(output[0][0])
        is_maize = confidence >= 0.5
        
        return {
            "is_maize": is_maize,
            "confidence": confidence
        }
```

## Running the Application

Now that you have all the necessary files, here's how to run the application:

1. First, run the setup script to initialize the database and populate districts:
```bash
python setup.py
```

2. Start the web application:
```bash
python app.py
