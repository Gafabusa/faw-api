import os
import sqlite3
from database_schema import DetectionDatabase
from populate_districts import populate_uganda_districts

def setup_application():
    """Set up the application by creating necessary directories and database"""
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Initialize database
    db = DetectionDatabase()
    
    # Populate districts
    populate_uganda_districts()
    
    print("Application setup complete!")
    print("To run the application, execute: python app.py")

if __name__ == "__main__":
    setup_application()
