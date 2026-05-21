# Mini Weather Tracker
 
A simple beginner pipeline that fetches live weather data,
saves it to a local database, and prints a report.
 
---
 
## Setup (3 steps)
 
### Step 1 — Install the one dependency
```
pip install requests
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
 
## Run it
```
python weather_pipeline.py
```
 
That's it! The script will:
- Create `weather.db` automatically (SQLite database file)
- Fetch weather for all cities in the CITIES list
- Save results to the database
- Print a weather report
---
 
## Customise cities
Open `weather_pipeline.py` and edit the CITIES list:
 
```python
CITIES = [
    "Jaipur",
    "Mumbai",
    "Tokyo",
    "New York",
]
```
 
---
 
## Files created
| File | What it is |
|---|---|
| `weather_pipeline.py` | The main script |
| `weather.db` | SQLite database (auto-created on first run) |
| `requirements.txt` | List of pip packages |
 
---
 
## What each stage does
| Stage | Code | What happens |
|---|---|---|
| Extract | `extract()` | Calls the OpenWeatherMap API |
| Transform | `transform()` | Cleans and flattens the raw JSON |
| Load | `load()` | Saves the row to weather.db |
| Analyze | `analyze()` | Queries the DB and prints a report |
 
