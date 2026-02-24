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
