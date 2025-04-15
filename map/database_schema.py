import sqlite3
import os

class DetectionDatabase:
    def __init__(self, db_path="detections.db"):
        self.db_path = db_path
        self.initialize_db()
    
    def initialize_db(self):
        """Create the database and tables if they don't exist"""
        # Check if database file exists
        db_exists = os.path.exists(self.db_path)
        
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS districts (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY,
            district_id INTEGER NOT NULL,
            detection_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (district_id) REFERENCES districts (id)
        )
        ''')
        
        # If this is a new database, populate with Uganda districts
        if not db_exists:
            self.populate_uganda_districts(cursor)
        
        conn.commit()
        conn.close()
    
    def populate_uganda_districts(self, cursor):
        """Populate the database with Uganda districts and their coordinates"""
        # This is a simplified list - you should replace with complete and accurate data
        districts = [
            ("Kampala", 0.3476, 32.5825),
            ("Wakiso", 0.4033, 32.4708),
            ("Jinja", 0.4250, 33.2039),
            ("Mbarara", -0.6066, 30.6566),
            ("Gulu", 2.7747, 32.2990),
            # Add more districts here
        ]
        
        cursor.executemany(
            "INSERT INTO districts (name, latitude, longitude) VALUES (?, ?, ?)",
            districts
        )
    
    def add_detection(self, district_name, detection_type, confidence):
        """Add a new detection to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get district ID
        cursor.execute("SELECT id FROM districts WHERE name = ?", (district_name,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            raise ValueError(f"District '{district_name}' not found in database")
        
        district_id = result[0]
        
        # Insert detection
        cursor.execute(
            "INSERT INTO detections (district_id, detection_type, confidence) VALUES (?, ?, ?)",
            (district_id, detection_type, confidence)
        )
        
        conn.commit()
        conn.close()
    
    def get_all_detections(self):
        """Get all detections with district information"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT 
            districts.name as district, 
            districts.latitude, 
            districts.longitude, 
            detections.detection_type, 
            detections.confidence,
            detections.timestamp
        FROM detections
        JOIN districts ON detections.district_id = districts.id
        ORDER BY detections.timestamp DESC
        ''')
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_latest_detections_by_district(self):
        """Get the latest detection for each district"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        WITH LatestDetections AS (
            SELECT 
                district_id,
                MAX(timestamp) as latest_timestamp
            FROM detections
            GROUP BY district_id
        )
        SELECT 
            districts.name as district, 
            districts.latitude, 
            districts.longitude, 
            detections.detection_type, 
            detections.confidence,
            detections.timestamp
        FROM detections
        JOIN LatestDetections ON 
            detections.district_id = LatestDetections.district_id AND
            detections.timestamp = LatestDetections.latest_timestamp
        JOIN districts ON detections.district_id = districts.id
        ''')
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_all_districts(self):
        """Get all districts with their coordinates"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, latitude, longitude FROM districts")
    
        districts = []
        for row in cursor.fetchall():
            districts.append({
                'name': row[0],
                'latitude': row[1],
                'longitude': row[2]
            })
        
        return districts
