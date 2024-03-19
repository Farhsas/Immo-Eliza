import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "property_id": 13540,
    "postal_code": 4350,
    "type_of_property": "HOUSE",
    "subtype_of_property": "HOUSE",
    "bedrooms": 4,
    "living_area": 300,
    "openfire": True,
    "terrace": True,
    "garden": True,
    "rooms": 10,
    "bathrooms": 2,
    "region": "Wallonie",
    "province": "Liège",
    "state_of_property": "AS_NEW",
    "facade_count": 4,
    "heating": "FUELOIL",
    "kitchen": "HYPER_EQUIPPED",
    "furnished": True,
    "swimmingpool": True
}
response = requests.post(url, json=data)
print(response.json())
