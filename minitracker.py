"""MINI WEATHER TRACKER PIPELINE"""
import requests
import sqlite3
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("API KEY:", API_KEY)
CITIES = [
    "Jaipur",
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "London",
]
DB_FILE = "weather.db"
#database setup

def setup_database():
    """Create the database and table if they don't exist yet."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            city        TEXT    NOT NULL,
            country     TEXT,
            temperature REAL,
            feels_like  REAL,
            humidity    INTEGER,
            description TEXT,
            wind_speed  REAL,
            fetched_at  TEXT
        )
    """)
 
    conn.commit()
    conn.close()
    print("✓ Database ready (weather.db)")

# data fetch from the API
def extract(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather"
 
    params = {
        "q":     city_name,   # City name
        "appid": API_KEY,     # Your API key
        "units": "metric",    # Celsius
    }
 
    try:
        response = requests.get(url, params=params, timeout=10)
 
        if response.status_code == 200:
            return response.json()  # Raw JSON from the API
 
        elif response.status_code == 401:
            print(f"  ✗ Invalid API key! Please update API_KEY in the script.")
            return None
 
        elif response.status_code == 404:
            print(f"  ✗ City '{city_name}' not found.")
            return None
 
        else:
            print(f"  ✗ API error {response.status_code} for {city_name}")
            return None
 
    except requests.exceptions.Timeout:
        print(f"  ✗ Request timed out for {city_name}")
        return None
 
    except requests.exceptions.ConnectionError:
        print(f"  ✗ No internet connection!")
        return None    
    
 # TRANSFORMATION OF THE MESSY DATA;   
    
def transform(raw_data):
    clean = {
        "city":        raw_data["name"],
        "country":     raw_data["sys"]["country"],
        "temperature": round(raw_data["main"]["temp"], 1),
        "feels_like":  round(raw_data["main"]["feels_like"], 1),
        "humidity":    raw_data["main"]["humidity"],
        "description": raw_data["weather"][0]["description"].capitalize(),
        "wind_speed":  raw_data["wind"]["speed"],
        "fetched_at":  datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }
 
    return clean
 
 
# LOADING OF THE DATA IN THE DB;
 
def load(clean_data):
    """Insert one weather record into the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
 
    cursor.execute("""
        INSERT INTO weather
            (city, country, temperature, feels_like, humidity, description, wind_speed, fetched_at)
        VALUES
            (:city, :country, :temperature, :feels_like, :humidity, :description, :wind_speed, :fetched_at)
    """, clean_data)  # clean_data is a dict — Python matches keys to :placeholders
 
    conn.commit()
    conn.close()
 
#ANALYZE THE DATA;
 
def analyze():
    """Query the database and print a simple weather report."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
 
    # Get all records from the LATEST run (grouped by city)
    cursor.execute("""
        SELECT city, country, temperature, feels_like, humidity, description, wind_speed, fetched_at
        FROM weather
        WHERE fetched_at = (
            SELECT MAX(fetched_at) FROM weather WHERE city = weather.city
        )
        ORDER BY temperature DESC
    """)
 
    rows = cursor.fetchall()
 
    if not rows:
        print("No data yet.")
        conn.close()
        return
 
    print("\n" + "═" * 58)
    print("  WEATHER REPORT —", datetime.now().strftime("%d %b %Y, %H:%M"))
    print("═" * 58)
 
    temps = []
    for row in rows:
        city, country, temp, feels, humidity, desc, wind, fetched = row
        temps.append(temp)
        print(f"\n  📍 {city}, {country}")
        print(f"     🌡  {temp}°C  (feels like {feels}°C)")
        print(f"     💧 Humidity: {humidity}%")
        print(f"     💨 Wind: {wind} m/s")
        print(f"     ☁  {desc}")
 
    # Simple stats
    print("\n" + "─" * 58)
    print(f"  Hottest  → {rows[0][0]} at {rows[0][2]}°C")
    print(f"  Coldest  → {rows[-1][0]} at {rows[-1][2]}°C")
    avg = round(sum(temps) / len(temps), 1)
    print(f"  Average  → {avg}°C across {len(rows)} cities")
    print("═" * 58)
 
    conn.close()
 
 
## MAIN FUNCTION
 
def run_pipeline():
    print("\n🌤  WEATHER PIPELINE STARTING\n")
 
    # Stage 0: Make sure the database exists
    setup_database()

    # # DELETE OLD DATA
    # conn = sqlite3.connect(DB_FILE)
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM weather")
    # conn.commit()
    # conn.close()

 
    # Stages 1–3: For each city, Extract → Transform → Load
    print("\n[Fetching weather data...]")
    success_count = 0
 
    for city in CITIES:
        print(f"  → {city}")
 
        raw  = extract(city)           # Stage 1
        if raw is None:
            continue                   # Skip this city if the API call failed
 
        clean = transform(raw)         # Stage 2
        load(clean)                    # Stage 3
 
        print(f"     ✓ {clean['temperature']}°C, {clean['description']}")
        success_count += 1
 
    print(f"\n  Saved {success_count}/{len(CITIES)} cities to database.")
 
    # Stage 4: Show the report
    analyze()
 
    print("\n✅ Pipeline complete!\n")
 
 
if __name__ == "__main__":
    run_pipeline()    