import requests
import csv
from datetime import datetime

# NASA's EONET API endpoint
url = "https://eonet.gsfc.nasa.gov/api/v3/events"

# Fetch data from the API
response = requests.get(url)
data = response.json()

# Extract events
events = data.get("events", [])

# Prepare CSV file
csv_file = "eonet_events.csv"
headers = ["title", "category", "date", "longitude", "latitude"]

with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for event in events:
        title = event.get("title", "N/A")
        categories = event.get("categories", [])
        category = categories[0]["title"] if categories else "Unknown"
        geometries = event.get("geometry", [])

        for geo in geometries:
            date = geo.get("date", "N/A")
            coords = geo.get("coordinates", [None, None])
            if isinstance(coords, list) and len(coords) == 2:
                longitude, latitude = coords
                writer.writerow([title, category, date, longitude, latitude])

print(f"Saved {len(events)} events to {csv_file}")