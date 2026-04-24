import requests
import csv
from datetime import datetime

# --- EXTRACT ---
# This function fetches live weather data from a free public API
# Open-Meteo is free, no account needed, no API key required
def fetch_weather(city, latitude, longitude):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current_weather=true"
        f"&hourly=relative_humidity_2m"
    )
    response = requests.get(url)        # This is the API call
    data = response.json()              # Convert response to dictionary
    return data

# --- TRANSFORM ---
# This function cleans and reshapes the raw API response
def transform_weather(city, raw_data):
    current = raw_data["current_weather"]
    record = {
        "city":        city,
        "temperature": current["temperature"],
        "windspeed":   current["windspeed"],
        "condition":   "Hot" if current["temperature"] > 30 else "Comfortable",
        "fetched_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return record

# --- LOAD ---
# This function saves the cleaned data to a CSV file
def save_to_csv(records, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {len(records)} records to {filename}")

# --- PIPELINE ---
# This is the main function that runs everything in order
def run_pipeline():
    # List of cities with their coordinates
    cities = [
        {"name": "Hyderabad", "lat": 17.38,  "lon": 78.47},
        {"name": "Mumbai",    "lat": 19.07,  "lon": 72.88},
        {"name": "Delhi",     "lat": 28.67,  "lon": 77.22},
        {"name": "Bangalore", "lat": 12.97,  "lon": 77.59},
    ]

    all_records = []

    for city in cities:
        print(f"Fetching data for {city['name']}...")
        raw    = fetch_weather(city["name"], city["lat"], city["lon"])
        record = transform_weather(city["name"], raw)
        all_records.append(record)
        print(f"  → {record['temperature']}°C, Wind: {record['windspeed']} km/h")

    save_to_csv(all_records, "weather_data.csv")
    print("Pipeline complete!")

# Run it
run_pipeline()