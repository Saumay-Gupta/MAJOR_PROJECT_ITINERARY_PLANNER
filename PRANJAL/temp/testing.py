import requests
import os
import math
from dotenv import load_dotenv

# ===============================
# CONFIG
# ===============================
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

destination = "Varanasi"
interests = [
    "Spiritual & Worship",
    "Nature & Sightseeing",
    "Cultural & Heritage",
]
days = 5
terrain = "plain"   # plain, coastal, mountain

# Base radius by terrain (km)
BASE_RADIUS_MAP = {"plain": 30, "coastal": 25, "mountain": 20}

# Growth factor per day (km/day)
BASE_OFFSET_MAP = {"plain": 12, "coastal": 10, "mountain": 8}

# Calculate radius
BASE_RADIUS = BASE_RADIUS_MAP.get(terrain, 30)
OFFSET_KM = BASE_OFFSET_MAP.get(terrain, 10)

TOTAL_RADIUS_KM = BASE_RADIUS + days * OFFSET_KM
TOTAL_RADIUS_M = TOTAL_RADIUS_KM * 1000

NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


# ===============================
# INTEREST MAP
# ===============================
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
        "bar",
        "pub",
        "sports_bar",
        "cocktail_bar",
        "wine_bar",
        "live_music_venue",
        "karaoke",
        "comedy_club",
        "dance_hall"
    ]
}
EXCLUDE_TYPES = {
    "hotel","lodging","restaurant","cafe",
    "bus_station","train_station","transit_station",
    "stadium","dam","government_office","intersection",
    "route","street_address","train_station","subway_station","airport"
}

# ===============================
# UTIL FUNCTIONS
# ===============================
def get_coordinates(place):
    res = requests.get(GEOCODE_URL, params={"address": place,"key": API_KEY}).json()
    loc = res["results"][0]["geometry"]["location"]
    return loc["lat"], loc["lng"]

def generate_centers(lat, lon, offset_km):
    """
    Generate center + 4 surrounding search points
    using accurate latitude & longitude conversions.
    """

    # Latitude: almost constant
    delta_lat = offset_km / 111.0

    # Longitude: depends on latitude
    delta_lon = offset_km / (111.0 * math.cos(math.radians(lat)))

    return [
        (lat, lon),                      # Center
        (lat + delta_lat, lon),          # North
        (lat - delta_lat, lon),          # South
        (lat, lon + delta_lon),          # East
        (lat, lon - delta_lon)           # West
    ]
def classify_weather(place):

    types_set = set(place.get("types", []))
    name = place["displayName"]["text"].lower()

    outdoor_types = {
        "amusement_park", "water_park", "roller_coaster",
        "off_roading_area", "hiking_area", "ski_resort",
        "cycling_park", "race_course", "skateboard_park",
        "mountain_peak", "beach", "lake", "island",
        "nature_preserve", "river", "scenic_spot", "woods"
    }

    indoor_types = {
        "adventure_sports_center", "ice_skating_rink",
        "buddhist_temple", "church", "hindu_temple",
        "mosque", "shinto_shrine", "synagogue",
        "art_gallery", "art_museum", "museum",
        "history_museum", "performing_arts_theater"
    }

    if types_set & outdoor_types:
        return "Outdoor"

    if types_set & indoor_types:
        return "Indoor"

    outdoor_keywords = [
        "fort", "ghat", "waterfall", "falls", "park", "river",
        "lake", "garden", "valley", "mountain", "peak"
    ]

    indoor_keywords = [
        "temple", "mandir", "museum", "gallery", "palace",
        "church", "mosque", "monastery"
    ]

    if any(word in name for word in outdoor_keywords):
        return "Outdoor"

    if any(word in name for word in indoor_keywords):
        return "Indoor"

    return "Outdoor"
# Bayesian average rating with logarithmic review bonus
GLOBAL_AVG_RATING = 4.2
MIN_REVIEWS = 200

def enhanced_place_score(place):
    """
    Combines Bayesian reasoning with logarithmic scaling
    Best of both worlds!
    """
    rating = place.get("rating", 0)
    reviews = place.get("userRatingCount", 0)
    
    if rating == 0:
        return 0
    
    # 1. Bayesian weighted rating (handles confidence)
    weighted_rating = (
        (reviews / (reviews + MIN_REVIEWS)) * rating +
        (MIN_REVIEWS / (reviews + MIN_REVIEWS)) * GLOBAL_AVG_RATING
    )
    
    # 2. Normalize to 0-1
    bayesian_score = weighted_rating / 5
    
    # 3. Review count bonus (diminishing returns)
    # More reviews = more confidence, but 1000 reviews not 10x better than 100
    review_bonus = min(math.log10(reviews + 1) / 3, 0.2)  # Max +0.2 bonus
    
    # 4. Final score (0 to 1.2 range, but we'll cap)
    final_score = bayesian_score + review_bonus
    
    return final_score  # Cap at 1.0 between 0 and 1

# ===============================
# MAIN SEARCH
# ===============================
lat, lon = get_coordinates(destination)
anchors = generate_centers(lat, lon, OFFSET_KM)

activities = {}

for a_lat, a_lon in anchors:
    for interest in interests:
        headers = {
            "Content-Type":"application/json",
            "X-Goog-Api-Key":API_KEY,
            "X-Goog-FieldMask":"places.id,places.displayName,places.types,places.rating,places.userRatingCount"}
        
        body = {
            "includedTypes":["tourist_attraction"],
            "maxResultCount": 20,
            "locationRestriction":{
                "circle":{
                    "center":{
                        "latitude":a_lat,
                        "longitude":a_lon
                        },
                        "radius":50000
                    }
                }
            }
        
        res = requests.post(NEARBY_URL, headers=headers, json=body)

        for p in res.json().get("places",[]):
            if set(p.get("types",[])) & EXCLUDE_TYPES: continue
            
            activities[p["id"]] = p

activity_list = list(activities.values())

# ===============================
# EMBEDDING + ENRICHMENT
# ===============================

for place in activity_list:
    place["final_score"] = enhanced_place_score(place)
    place["weather"] = classify_weather(place)

activity_list.sort(key=lambda x:x["final_score"], reverse=True)
activity_list = activity_list[:days*5]  # Top N based on days

# ===============================
# OUTPUT
# ===============================
print("\n===== FINAL RESULTS =====\n")
for i,p in enumerate(activity_list,1):
    print(f"{i}. {p['displayName']['text']}")
    print("Score:",p["final_score"])
    print("Weather:",p["weather"])
    print("-"*80)