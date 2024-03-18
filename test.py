import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "property_id": 12345,
    "postal_code": 4260,
    "type_of_property": "APARTMENT",
    "subtype_of_property": "APARTMENT",
    "bedrooms": 2,
    "living_area": 80,
    "openfire": False,
    "terrace": True,
    "garden": False,
    "rooms": 3,
    "bathrooms": 1,
    "region": "Wallonie",
    "province": "Liège",
    "state_of_property": "GOOD",
    "facade_count": 1,
    "heating": "GAS",
    "kitchen": "INSTALLED",
    "furnished": False,
    "swimmingpool": False
}
response = requests.post(url, json=data)
print(response.json())
