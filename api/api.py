from flask import Flask, request, jsonify

import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("models/pipeline.joblib")

def make_estimation(data):
    df = pd.DataFrame.from_dict(data, orient='index').T

    estimation = model.predict(df)

    return estimation

@app.route("/", methods=["GET"])
def home():
    return "I'm still standing"


@app.route("/predict", methods=["POST"])
def predict():
    expected_fields=["property_id", "postal_code", "type_of_property", "subtype_of_property",
           "bedrooms", "living_area", "openfire", "terrace", "garden",
           "rooms", "bathrooms", "region", "province", "state_of_property",
           "facade_count", "heating", "kitchen", "furnished", "swimmingpool"]
    data = request.json

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    for field in expected_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    estimation = make_estimation(data)
    return jsonify(str(estimation[0]))
