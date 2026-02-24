import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

BASE_URL = "https://places.googleapis.com/v1/places:searchText"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask":
    "places.id,places.displayName,places.editorialSummary"
}

body = {
    "textQuery": "Kashi Vishwanath Temple Varanasi",
    "maxResultCount": 5
}

response = requests.post(BASE_URL, headers=headers, json=body)
data = response.json()

for place in data.get("places", []):
    print("\nName:", place["displayName"]["text"])
    editorial = place.get("editorialSummary", {})
    if editorial:
        print("Editorial Summary:", editorial.get("text"))
    else:
        print("Editorial Summary: NOT AVAILABLE")
