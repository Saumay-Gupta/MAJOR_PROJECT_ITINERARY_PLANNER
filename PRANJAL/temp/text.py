import requests
import os
import math
from dotenv import load_dotenv

# ===============================
# LOAD API KEY
# ===============================
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

BASE_URL = "https://places.googleapis.com/v1/places:searchNearby"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

# ===============================
# USER INPUT
# ===============================
destination = "Goa"
interests = [
    "Scenic & Nature",
    "Historical & Heritage",
    "Adventure & Outdoor"
]
days = 5
terrain = "plain"

# ===============================
# CONFIG
# ===============================
BASE_RADIUS_MAP = {"plain": 45000, "coastal": 40000, "mountain": 30000}
MAX_RADIUS = 50000

radius = min(BASE_RADIUS_MAP.get(terrain, 40000) + (days - 1) * 5000, MAX_RADIUS)

# realistic activity count
if terrain == "mountain":
    per_day = 4
else:
    per_day = 6

TARGET_ACTIVITY_POOL = min(days * per_day, 60)

ANCHOR_RADIUS = 30000  # 30km per anchor
MIN_REVIEWS = 300      # remove weak places

print("\n===== CONFIG =====")
print("Radius:", radius)
print("Activity Target:", TARGET_ACTIVITY_POOL)
print("==================\n")

# ===============================
# INTEREST MAP
# ===============================
INTEREST_TYPE_MAP = {
    "Adventure & Outdoor": [
        "hiking_area", "adventure_sports_center",
        "sports_activity_location", "campground",
        "wildlife_park", "national_park"
    ],
    "Historical & Heritage": [
        "historical_landmark", "monument",
        "museum", "fortress"
    ],
    "Spiritual & Religious": [
        "hindu_temple", "mosque",
        "church", "monastery",
        "buddhist_temple"
    ],
    "Scenic & Nature": [
        "park", "garden",
        "lake", "waterfall"
    ]
}

# ===============================
# STRICT EXCLUSIONS
# ===============================
EXCLUDE_TYPES = [
    "hotel", "lodging", "resort_hotel",
    "restaurant", "cafe", "bar",
    "wedding_venue", "banquet_hall",
    "private_guest_room",
    "car_rental", "vehicle_rental",
    "travel_agency", "tour_agency",
    "transportation_service",
    "real_estate_agency",
    "finance", "atm",
    "store", "shopping_mall"
]

# ===============================
# HELPERS
# ===============================
def get_coordinates(place):
    params = {"address": place, "key": API_KEY}
    res = requests.get(GEOCODE_URL, params=params).json()
    if res["status"] == "OK":
        loc = res["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None, None


def generate_anchors(lat, lon, days):
    anchors = [(lat, lon)]
    spread_km = min(days * 6, 40)
    delta = spread_km / 111

    offsets = [
        (delta, 0), (-delta, 0),
        (0, delta), (0, -delta),
        (delta, delta), (-delta, -delta),
        (delta, -delta), (-delta, delta)
    ]

    for i in range(min(days, 8)):
        dlat, dlon = offsets[i]
        anchors.append((lat + dlat, lon + dlon))

    return anchors


def fetch_places(lat, lon, types):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask":
        "places.id,places.displayName,places.types,"
        "places.location,places.rating,"
        "places.userRatingCount"
    }

    body = {
        "includedTypes": types,
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},
                "radius": ANCHOR_RADIUS
            }
        }
    }

    response = requests.post(BASE_URL, headers=headers, json=body)
    data = response.json()
    return data.get("places", [])


def is_noise(place):
    types = place.get("types", [])

    # remove excluded types
    if any(t in EXCLUDE_TYPES for t in types):
        return True

    # remove generic listings
    if types == ["point_of_interest", "establishment"]:
        return True

    # remove low review count
    if place.get("userRatingCount", 0) < MIN_REVIEWS:
        return True

    return False


def activity_score(place):
    rating = place.get("rating", 0) / 5
    reviews = math.log(place.get("userRatingCount", 0) + 1) / 12
    return 0.5 * rating + 0.5 * reviews


# ===============================
# ENGINE
# ===============================
lat, lon = get_coordinates(destination)
if not lat:
    print("Geocoding failed.")
    exit()

anchors = generate_anchors(lat, lon, days)

activities = {}

for a_lat, a_lon in anchors:

    # interest-based search
    for interest in interests:
        types = INTEREST_TYPE_MAP.get(interest, [])
        results = fetch_places(a_lat, a_lon, types)
        for p in results:
            if not is_noise(p):
                activities[p["id"]] = p

    # general tourist fallback
    fallback = fetch_places(a_lat, a_lon, ["tourist_attraction"])
    for p in fallback:
        if not is_noise(p):
            activities[p["id"]] = p

# ===============================
# SORT & LIMIT
# ===============================
activity_list = list(activities.values())
activity_list.sort(key=lambda x: activity_score(x), reverse=True)
activity_list = activity_list[:TARGET_ACTIVITY_POOL]

# ===============================
# OUTPUT
# ===============================
print("\n===== FINAL ACTIVITY POOL =====\n")
print("Total:", len(activity_list), "\n")

for i, p in enumerate(activity_list, 1):
    print(f"{i}. {p['displayName']['text']} "
          f"(⭐ {p.get('rating')} | Reviews {p.get('userRatingCount')})")
