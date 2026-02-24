import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"

destination = "Varanasi"
interests = [
    "Spiritual & Worship",
    "Nature & Sightseeing",
    "Cultural & Heritage",
    "Nightlife & Entertainment"
]
INTEREST_TYPE_MAP = {
    "Adventure": [
        "adventure_sports_center",
        "amusement_park",
        "water_park",
        "roller_coaster",
        "off_roading_area",
        "hiking_area",
        "ski_resort",
        "cycling_park",
        "race_course",
        "ice_skating_rink",
        "skateboard_park",
        "mountain_peak"
    ],

    "Nature & Sightseeing": [
        "beach",
        "lake",
        "island",
        "nature_preserve",
        "river",
        "scenic_spot",
        "woods"
    ],

    "Spiritual & Worship": [
        "buddhist_temple",
        "church",
        "hindu_temple",
        "mosque",
        "shinto_shrine",
        "synagogue"
    ],

    "Cultural & Heritage": [
        "art_gallery",
        "art_museum",
        "museum",
        "history_museum",
        "historical_place",
        "monument",
        "castle",
        "cultural_landmark",
        "performing_arts_theater",
        "sculpture"
    ],

    "Shopping & Souvenirs": [
        "shopping_mall",
        "market",
        "farmers_market",
        "flea_market",
        "gift_shop",
        "jewelry_store",
        "book_store",
        "clothing_store",
        "department_store",
        "toy_store",
        "thrift_store"
    ],

    "Nightlife & Entertainment": [
        "night_club",
        "live_music_venue",
        "karaoke",
        "comedy_club",
        "dance_hall"
    ]
}
# ----------------------------
# Get Coordinates (Geocoding)
# ----------------------------

def get_coordinates(place_name):
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": place_name,
        "key": API_KEY
    }
    res = requests.get(geo_url, params=params).json()
    
    # Check if results exist
    if res.get("results") and len(res["results"]) > 0:
        location = res["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        raise Exception(f"Could not find coordinates for {place_name}")

center_lat, center_lon = get_coordinates(destination)

# ----------------------------
# Simple Nearby Search
# ----------------------------

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask":
        "places.id,"
        "places.displayName,"
        "places.types,"
        "places.rating,"
        "places.userRatingCount,"
        "places.location"
}

body = {
    "includedTypes": INTEREST_TYPE_MAP[interests[3]],
    "maxResultCount": 20,
    "locationRestriction": {
        "circle": {
            "center": {
                "latitude": center_lat,
                "longitude": center_lon
            },
            "radius": 50000
        }
    }
}

response = requests.post(NEARBY_URL, headers=headers, json=body)
data = response.json()
print("\nTotal places in this page:", len(data.get("places", [])))

next_token = data.get("nextPageToken")

if next_token:
    print("More pages available ✅")
    print("Next Page Token:", next_token)
else:
    print("No more pages ❌ (Only one page exists)")

# Check if places exist in response
if "places" not in data:
    print("No places found in response")
    print("Response:", data)
    exit()

destinations = []
for place in data.get("places", []):
    loc = place.get("location", {})
    place_lat = loc.get("latitude")
    place_lon = loc.get("longitude")

    if place_lat is not None and place_lon is not None:
        destinations.append({
            "waypoint": {
                "location": {
                    "latLng": {
                        "latitude": place_lat,
                        "longitude": place_lon
                    }
                }
            }
        })

# Only proceed if we have destinations
if not destinations:
    print("No valid destinations found")
    exit()

# ----------------------------
# OLD DISTANCE MATRIX (Simple)
# ----------------------------

DISTANCE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

# Build destination coordinate string
destination_coords = []
for place in data.get("places", []):
    loc = place.get("location", {})
    place_lat = loc.get("latitude")
    place_lon = loc.get("longitude")

    if place_lat is not None and place_lon is not None:
        destination_coords.append(f"{place_lat},{place_lon}")

if not destination_coords:
    print("No valid destinations found")
    exit()

params = {
    "origins": f"{center_lat},{center_lon}",
    "destinations": "|".join(destination_coords),
    "mode": "driving",
    "key": API_KEY
}

response = requests.get(DISTANCE_URL, params=params)
matrix_data = response.json()

# ----------------------------
# Clean Output Format
# ----------------------------

print("\n===== RAW CLEAN OUTPUT =====\n")

elements = matrix_data["rows"][0]["elements"]

for idx, place in enumerate(data.get("places", []), 1):

    name = place.get("displayName", {}).get("text", "N/A")
    rating = place.get("rating", "N/A")
    reviews = place.get("userRatingCount", "N/A")
    types = place.get("types", [])

    distance_km = "N/A"
    duration_min = "N/A"

    if idx - 1 < len(elements):
        element = elements[idx - 1]

        if element.get("status") == "OK":
            distance_km = round(element["distance"]["value"] / 1000, 2)
            duration_min = round(element["duration"]["value"] / 60)

    print(f"{idx}. {name}")
    print(f"   Rating: {rating}")
    print(f"   Reviews: {reviews}")
    print(f"   Types: {types}")
    print(f"   Distance: {distance_km} km")
    print(f"   Duration: {duration_min} minutes")
    print("-" * 60)