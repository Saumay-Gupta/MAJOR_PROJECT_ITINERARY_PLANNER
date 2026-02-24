import requests
import os
import math
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

destination = "Manali"
days = 5

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"

RADIUS = 50000  # 20 km simple fixed radius

# ===============================
# GET COORDINATES
# ===============================
def get_coordinates(place):
    res = requests.get(GEOCODE_URL, params={
        "address": place,
        "key": API_KEY
    }).json()

    loc = res["results"][0]["geometry"]["location"]
    return loc["lat"], loc["lng"]

# ===============================
# SIMPLE PLACE SCORE
# ===============================
def simple_score(place):
    rating = place.get("rating", 0)
    reviews = place.get("userRatingCount", 0)
    if rating == 0:
        return 0
    return rating * math.log(reviews + 1)

# ===============================
# FETCH PLACES
# ===============================
lat, lon = get_coordinates(destination)

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "places.id,places.displayName,places.rating,places.userRatingCount"
}

body = {
    "includedTypes": ["tourist_attraction"],
    "maxResultCount": 20,
    "locationRestriction": {
        "circle": {
            "center": {"latitude": lat, "longitude": lon},
            "radius": RADIUS
        }
    }
}

response = requests.post(NEARBY_URL, headers=headers, json=body)
places = response.json().get("places", [])

# ===============================
# SCORE + SORT
# ===============================
for p in places:
    p["score"] = simple_score(p)

places.sort(key=lambda x: x["score"], reverse=True)

# ===============================
# SELECT TOP N
# ===============================
max_places = min(len(places), days * 5)
selected = places[:max_places]

# ===============================
# DISTRIBUTE BY DAY
# ===============================
print(f"\n===== {days}-Day Itinerary for {destination} =====\n")

per_day = math.ceil(len(selected) / days)

for day in range(days):
    print(f"\nDay {day+1}:")
    start = day * per_day
    end = start + per_day
    for place in selected[start:end]:
        print("-", place["displayName"]["text"])