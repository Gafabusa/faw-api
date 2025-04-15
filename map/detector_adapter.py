from model_utils import detector
from map.database_schema import DetectionDatabase
import math

class DetectorAdapter:
    def __init__(self):
        self.db = DetectionDatabase()
    
    def detect_and_record(self, image_path, district_name):
        """Run detection and record the result with location data"""
        # Run the detection using your existing detector
        detection_result = detector.detect(image_path)
        
        # Extract the detection type
        if "result" in detection_result:
            result_text = detection_result["result"]
            
            # Map the result text to a detection type for the database
            if "larval damage" in result_text.lower():
                detection_type = "fall-armyworm-larval-damage"
            elif "eggs" in result_text.lower():
                detection_type = "fall-armyworm-egg"
            elif "frass" in result_text.lower():
                detection_type = "fall-armyworm-frass"
            elif "healthy" in result_text.lower():
                detection_type = "healthy-maize"
            else:
                detection_type = "unknown"
            
            # Record in database
            confidence = detection_result.get("confidence", 0) / 100.0  # Convert from percentage
            self.db.add_detection(
                district_name=district_name,
                detection_type=detection_type,
                confidence=confidence
            )
        
        return detection_result
    
    def get_detection_map_data(self):
        """Get data for the detection map"""
        return self.db.get_latest_detections_by_district()
    
    def get_all_districts(self):
        """Get all districts for the map"""
        return self.db.get_all_districts()
    
    def find_nearest_district(self, latitude, longitude):
        """Find the nearest district based on GPS coordinates"""
        districts = self.db.get_all_districts()
        
        if not districts:
            return None
        
        # Calculate distance to each district
        nearest_district = None
        min_distance = float('inf')
        
        for district in districts:
            # Simple Euclidean distance (not perfect for Earth coordinates but sufficient for this purpose)
            dist = math.sqrt((district['latitude'] - latitude)**2 + (district['longitude'] - longitude)**2)
            
            if dist < min_distance:
                min_distance = dist
                nearest_district = district['name']
        
        return nearest_district
