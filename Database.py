import sqlite3

def db_conn():
    conn = sqlite3.connect('Weather_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            location TEXT NOT NULL,
            country TEXT NOT NULL,
            temperature REAL,
            temp_min REAL,
            temp_max REAL,
            weather_icons TEXT,
            weather_descriptions TEXT,
            wind_speed REAL,
            wind_degree REAL,
            pressure REAL,
            humidity REAL,
            cloudcover REAL,
            feelslike REAL,
            visibility REAL,
            rain REAL
        )
    ''')
    conn.commit()
    conn.close()
