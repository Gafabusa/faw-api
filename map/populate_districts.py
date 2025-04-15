import sqlite3

def populate_uganda_districts(db_path="detections.db"):
    """
    Populate the database with all Uganda districts and their coordinates.
    """
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if districts table exists and create it if not
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS districts (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    )
    ''')
    
    # Check if districts table already has data
    cursor.execute("SELECT COUNT(*) FROM districts")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"Database already contains {count} districts. Clearing existing data.")
        cursor.execute("DELETE FROM districts")
    
    # Comprehensive list of Uganda districts with approximate coordinates
    districts = [
        ("Abim", 2.7061, 33.6667),
        ("Adjumani", 3.3667, 31.7833),
        ("Agago", 3.0333, 33.3333),
        ("Alebtong", 2.2333, 33.3500),
        ("Amolatar", 1.6167, 32.8667),
        ("Amudat", 1.8000, 34.9000),
        ("Amuria", 2.0333, 33.6500),
        ("Amuru", 2.8000, 32.0000),
        ("Apac", 1.9833, 32.5333),
        ("Arua", 3.0200, 30.9100),
        ("Budaka", 1.0000, 33.9333),
        ("Bududa", 1.0000, 34.3333),
        ("Bugiri", 0.5667, 33.7500),
        ("Bugweri", 0.5500, 33.6000),
        ("Buhweju", -0.3333, 30.3000),
        ("Buikwe", 0.3167, 33.0000),
        ("Bukedea", 1.3167, 34.0500),
        ("Bukomansimbi", -0.1500, 31.6000),
        ("Bukwo", 1.2833, 34.7500),
        ("Bulambuli", 1.1667, 34.3833),
        ("Buliisa", 2.1167, 31.4167),
        ("Bundibugyo", 0.7000, 30.0667),
        ("Bunyangabu", 0.5000, 30.3000),
        ("Bushenyi", -0.5333, 30.2167),
        ("Busia", 0.4667, 34.0833),
        ("Butaleja", 0.9333, 33.9500),
        ("Butambala", 0.1667, 32.1333),
        ("Butebo", 1.1667, 33.9000),
        ("Buvuma", -0.3833, 33.2500),
        ("Buyende", 1.2333, 33.1250),
        ("Dokolo", 1.9167, 33.1667),
        ("Gomba", 0.2167, 31.6667),
        ("Gulu", 2.7747, 32.2990),
        ("Hoima", 1.4333, 31.3500),
        ("Ibanda", -0.1333, 30.5000),
        ("Iganga", 0.6167, 33.4833),
        ("Isingiro", -0.9167, 30.8333),
        ("Jinja", 0.4250, 32.2039),
        ("Kaabong", 3.5167, 34.1333),
        ("Kabale", -1.2500, 30.0000),
        ("Kabarole", 0.6700, 30.2800),
        ("Kaberamaido", 1.7500, 33.1500),
        ("Kagadi", 0.9333, 30.8167),
        ("Kakumiro", 0.7833, 31.3333),
        ("Kalaki", 1.7000, 33.3700),
        ("Kalangala", -0.3167, 32.2500),
        ("Kaliro", 0.9000, 33.5000),
        ("Kalungu", -0.1000, 31.8333),
        ("Kampala", 0.3476, 32.5825),
        ("Kamuli", 0.9500, 33.1167),
        ("Kamwenge", 0.1833, 30.4500),
        ("Kanungu", -0.9500, 29.7833),
        ("Kapchorwa", 1.4000, 34.4500),
        ("Kapelebyong", 2.0500, 33.8000),
        ("Karenga", 3.3000, 33.5000),
        ("Kasanda", 0.5000, 31.8000),
        ("Kasese", 0.1833, 30.0833),
        ("Katakwi", 1.9000, 33.9667),
        ("Kayunga", 0.7000, 32.8833),
        ("Kazo", -0.0500, 30.7000),
        ("Kibaale", 0.8000, 30.7000),
        ("Kiboga", 0.9167, 31.7667),
        ("Kibuku", 1.0500, 33.8333),
        ("Kikuube", 1.3500, 31.4167),
        ("Kiruhura", -0.1944, 30.8056),
        ("Kiryandongo", 1.8667, 32.0667),
        ("Kisoro", -1.2833, 29.6833),
        ("Kitagwenda", 0.0833, 30.2500),
        ("Kitgum", 3.2833, 32.8833),
        ("Koboko", 3.4167, 30.9667),
        ("Kole", 2.4000, 32.8000),
        ("Kotido", 2.9800, 34.1333),
        ("Kumi", 1.4667, 33.9333),
        ("Kwania", 1.7333, 32.6333),
        ("Kyankwanzi", 1.0000, 31.6000),
        ("Kyegegwa", 0.5000, 31.0500),
        ("Kyenjojo", 0.6333, 30.6167),
        ("Kyotera", -0.6167, 31.5167),
        ("Lamwo", 3.5333, 32.8000),
        ("Lira", 2.2499, 32.9000),
        ("Luuka", 0.7000, 33.3000),
        ("Luwero", 0.8500, 32.4667),
        ("Lwengo", -0.4167, 31.4000),
        ("Lyantonde", -0.4000, 31.1667),
        ("Madi-Okollo", 2.9000, 31.0000),
        ("Manafwa", 0.9000, 34.3333),
        ("Maracha", 3.2833, 30.9333),
        ("Masaka", -0.3333, 31.7333),
        ("Masindi", 1.6744, 31.7150),
        ("Mayuge", 0.4500, 33.4833),
        ("Mbale", 1.0750, 34.1750),
        ("Mbarara", -0.6066, 30.6566),
        ("Mitooma", -0.6167, 30.0333),
        ("Mityana", 0.4167, 32.0333),
        ("Moroto", 2.5333, 34.6667),
        ("Moyo", 3.6500, 31.7167),
        ("Mpigi", 0.2167, 32.3000),
        ("Mubende", 0.5833, 31.3667),
        ("Mukono", 0.3533, 32.7550),
        ("Nabilatuk", 2.0500, 34.6500),
        ("Nakapiripirit", 1.9167, 34.7833),
        ("Nakaseke", 0.7333, 32.4500),
        ("Nakasongola", 1.3167, 32.4500),
        ("Namayingo", 0.2833, 33.8833),
        ("Namisindwa", 0.9000, 34.4000),
        ("Namutumba", 0.8833, 33.6833),
        ("Napak", 2.3000, 34.3000),
        ("Nebbi", 2.4833, 31.0833),
        ("Ngora", 1.5000, 33.7667),
        ("Ntoroko", 1.0500, 30.4000),
        ("Ntungamo", -0.8833, 30.2667),
        ("Nwoya", 2.6333, 32.0000),
        ("Obongi", 3.4667, 31.6000),
        ("Omoro", 2.7167, 32.4833),
        ("Otuke", 2.5000, 33.0833),
        ("Oyam", 2.2333, 32.5000),
        ("Pader", 2.8000, 33.1333),
        ("Pakwach", 2.4667, 31.5000),
        ("Pallisa", 1.1333, 33.7000),
        ("Rakai", -0.7167, 31.5333),
        ("Rubanda", -1.1833, 29.8500),
        ("Rubirizi", -0.3000, 30.1000),
        ("Rukiga", -1.1333, 30.0667),
        ("Rukungiri", -0.8333, 29.9333),
        ("Rwampara", -0.5500, 30.5000),
        ("Sembabule", 0.0833, 31.4667),
        ("Serere", 1.5000, 33.5500),
        ("Sheema", -0.6000, 30.4000),
        ("Sironko", 1.2333, 34.2500),
        ("Soroti", 1.7167, 33.6167),
        ("Terego", 3.0500, 30.7500),
        ("Tororo", 0.7000, 34.1833),
        ("Wakiso", 0.4033, 32.4708),
        ("Yumbe", 3.4650, 31.2467),
        ("Zombo", 2.5167, 30.9000),
    ]
    
    # Insert districts
    try:
        cursor.executemany(
            "INSERT INTO districts (name, latitude, longitude) VALUES (?, ?, ?)",
            districts
        )
        conn.commit()
        print(f"Successfully populated database with {len(districts)} Uganda districts")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting districts: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    populate_uganda_districts()
