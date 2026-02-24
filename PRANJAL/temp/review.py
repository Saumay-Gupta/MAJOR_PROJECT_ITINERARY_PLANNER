import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

place_id = "ChIJFwuU7iEujjkRE3v7zU8OYEg"

url = f"https://places.googleapis.com/v1/places/{place_id}"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "displayName,reviews"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    reviews = data.get("reviews", [])

    print("\n===== REVIEWS =====\n")

    for i, review in enumerate(reviews[:3], 1):
        print(f"{i}. Rating:", review.get("rating"))
        print("   Author:", review.get("authorAttribution", {}).get("displayName"))
        print("   Text:", review.get("text", {}).get("text"))
        print("-" * 60)
else:
    print("Error:", response.status_code)