# Mini Weather Tracker 🌤️
 
A beginner-friendly weather data pipeline that fetches live weather data,
saves it to a local database, prints a report, **and displays an interactive dashboard**.
 
---
 
## Features
 
✅ **ETL Pipeline** - Extract, Transform, Load weather data  
✅ **SQLite Database** - Store historical weather records  
✅ **CLI Reports** - Terminal-based weather summaries  
✅ **Interactive Dashboard** - Beautiful Streamlit web interface  
✅ **Data Visualization** - Charts, graphs, and metrics  
✅ **Multi-City Tracking** - Monitor weather across multiple cities  
 
---
 
## Setup (Quick Start)
 
### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```
 
Or install individually:
```bash
pip install requests python-dotenv streamlit plotly pandas
```
 
### Step 2 — Get a FREE API key
1. Go to https://openweathermap.org/api
2. Click "Sign Up" (free account)
3. After signing in, go to "API Keys" tab
4. Copy your key
### Step 3 — Create a `.env` file
Create a file named `.env` in the project folder and add:
```env
OPENWEATHER_API_KEY=your_api_key_here
```
 
Example:
```env
OPENWEATHER_API_KEY=a1b2c3d4exxxxxxxxxxxx
```
 
The script loads the API key securely using:
```python
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
```
 
---
 
## How to Use
 
### Option 1: Command Line (Terminal Report)
 
Run the data pipeline:
```bash
python mini_weather_tracker.py
```
 
This will:
- Create `weather.db` automatically (SQLite database)
- Fetch weather for all cities in the CITIES list
- Save results to the database
- Print a weather report in your terminal
**Output example:**
```
══════════════════════════════════════════════════════════
  WEATHER REPORT — 24 May 2026, 14:30
══════════════════════════════════════════════════════════
 
  📍 Mumbai, IN
     🌡  32.5°C  (feels like 36.2°C)
     💧 Humidity: 78%
     💨 Wind: 4.5 m/s
     ☁  Partly cloudy
 
──────────────────────────────────────────────────────────
  Hottest  → Mumbai at 32.5°C
  Coldest  → London at 15.3°C
  Average  → 24.6°C across 5 cities
══════════════════════════════════════════════════════════
```
 
---
 
### Option 2: Interactive Dashboard (Web Interface)
 
Launch the Streamlit dashboard:
```bash
streamlit run dashboard.py
```
 
Your browser will automatically open to `http://localhost:8501`
 
**Dashboard Features:**
- 🌡️ **Temperature comparison charts** - Bar charts showing all cities
- 💨 **Wind speed gauges** - Real-time wind measurements
- 📊 **Humidity vs Temperature** - Scatter plot analysis
- 📈 **Historical trends** - Track changes over time
- 🔄 **Auto-refresh** - Optional 60-second updates
- 📥 **Data export** - Download CSV of all weather data
- 🎨 **Beautiful UI** - Gradient cards and interactive charts
**Screenshot placeholders:**
```
┌─────────────────────────────────────────────────┐
│  🌤️ Weather Tracker Dashboard                  │
├─────────────────────────────────────────────────┤
│  🔥 Hottest    ❄️ Coldest    📊 Average        │
│  Mumbai        London         24.6°C            │
│  32.5°C        15.3°C                           │
├─────────────────────────────────────────────────┤
│  [Temperature Bar Chart]                        │
│  [Humidity vs Temp Scatter Plot]               │
│  [Historical Trends Line Graph]                │
└─────────────────────────────────────────────────┘
```
 
---
 
## Customize Cities
 
Open `mini_weather_tracker.py` and edit the CITIES list:
 
```python
CITIES = [
    "Jaipur",
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "London",
    "Tokyo",
    "New York",
    "Paris",
    # Add more cities here!
]
```
 
The dashboard will automatically display all cities you add.
 
---
## Project Structure
 
```
weather-tracker/
├── mini_weather_tracker.py   # Main ETL pipeline script
├── dashboard.py               # Streamlit web dashboard
├── requirements.txt           # Python dependencies
├── .env                       # API key (create this)
├── .gitignore                # Git ignore rules
├── weather.db                # SQLite database (auto-created)
└── README.md                 # This file
```
 
---

## Quick Reference
 
```bash
# Install dependencies
pip install -r requirements.txt
 
# Run pipeline (collect data)
python mini_weather_tracker.py
 
# Launch dashboard
streamlit run dashboard.py
 
# Deploy to Streamlit Cloud
```
 
---
