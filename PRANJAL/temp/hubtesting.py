import pandas as pd
import requests
import math

API_KEY = "AIzaSyBnWH0vl2fCHKAqtW7tMm1RGFBxkElXfGw"

# -----------------------------
# CONFIG
# -----------------------------
MAX_DISTANCE = 150 # km
MAX_DURATION_MIN = 240  # 4 hours


# -----------------------------
# Load dataset
# -----------------------------
hub_df = pd.read_csv("india_cleaned_hub_network.csv")

hub_graph = {}
for _, row in hub_df.iterrows():
    source = row["source_hub"]
    destination = row["destination_hub"]

    if source not in hub_graph:
        hub_graph[source] = []

    hub_graph[source].append(destination)


# -----------------------------
# Geocoding
# -----------------------------
def get_coordinates(place):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": place + ", India",
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return (location["lat"], location["lng"])
    else:
        return None


# -----------------------------
# Bearing Calculation
# -----------------------------
def calculate_bearing(coord1, coord2):
    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])

    dlon = lon2 - lon1

    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (
        math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    )

    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360


# -----------------------------
# Convert Bearing to Direction
# -----------------------------
def get_direction_label(bearing):
    directions = [
        "North",
        "North-East",
        "East",
        "South-East",
        "South",
        "South-West",
        "West",
        "North-West"
    ]
    index = round(bearing / 45) % 8
    return directions[index]


# -----------------------------
# Distance Matrix (Batch)
# -----------------------------
def get_distances(origin, destinations):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": origin + ", India",
        "destinations": "|".join([d + ", India" for d in destinations]),
        "key": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []

    if data["status"] == "OK":
        elements = data["rows"][0]["elements"]

        for i, element in enumerate(elements):
            if element["status"] == "OK":
                distance_km = element["distance"]["value"] / 1000
                duration_min = element["duration"]["value"] / 60

                results.append({
                    "hub": destinations[i],
                    "distance": distance_km,
                    "duration_min": duration_min,
                    "duration_text": element["duration"]["text"]
                })

    return results


# -----------------------------
# USER INPUT
# -----------------------------
user_place = input("Enter a place: ").strip()

if user_place not in hub_graph:
    print("Place not found.")
    exit()

connected_hubs = hub_graph[user_place]

print(f"\nNearby hubs of {user_place} (filtered by distance & duration):\n")

# Get center coordinates once
center_coords = get_coordinates(user_place)

distance_data = get_distances(user_place, connected_hubs)

filtered_results = []

for item in distance_data:
    if item["distance"] <= MAX_DISTANCE and item["duration_min"] <= MAX_DURATION_MIN:

        hub_coords = get_coordinates(item["hub"])
        if hub_coords:
            bearing = calculate_bearing(center_coords, hub_coords)
            direction = get_direction_label(bearing)

            item["direction"] = direction
            item["bearing"] = bearing

            filtered_results.append(item)


# Sort by shortest duration
filtered_results.sort(key=lambda x: x["duration_min"])

for item in filtered_results:
    print(
        f"- {item['hub']} | {item['direction']} | "
        f"{round(item['distance'],1)} km | {item['duration_text']}"
    )