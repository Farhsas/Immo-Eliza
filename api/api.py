from flask import Flask, request, jsonify
from flask.helpers import _prepare_send_file_kwargs

import pandas as pd
import pickle

app = Flask(__name__)

preprocess_apart = pickle.load(open("models/preprocessing_apartments.pkl", "rb"))
preprocess_houses = pickle.load(open("models/preprocessing_houses.pkl", "rb"))

model_apart = pickle.load(open("models/xgb_apartments.pkl", "rb"))
model_houses = pickle.load(open("models/xgb_houses.pkl", "rb"))


def make_estimation(data):
    df = pd.DataFrame.from_dict(data, orient='index').T

    df_temp = df[["type_of_property", "subtype_of_property", "state_of_property", "region", "province", "heating", "kitchen"]]
    encoded_data = preprocess_apart.transform(df_temp).toarray()

    df_encoded = pd.DataFrame(
        encoded_data,
        columns=preprocess_apart.get_feature_names_out(
            input_features=["type_of_property", "subtype_of_property", "state_of_property", "region", "province", "heating", "kitchen"]
        )
    )

    df = pd.concat([df, df_encoded], axis=1)
    df = df.drop(["property_id", "type_of_property", "subtype_of_property", "state_of_property", "region", "province", "heating", "kitchen"], axis=1)
    df["postal_code"] = df["postal_code"].astype(int)
    df["bedrooms"] = df["bedrooms"].astype(int)
    df["living_area"] = df["living_area"].astype(float)
    df["openfire"] = df["openfire"].astype(bool)
    df["terrace"] = df["terrace"].astype(bool)
    df["garden"] = df["garden"].astype(bool)
    df["rooms"] = df["rooms"].astype(int)
    df["bathrooms"] = df["bathrooms"].astype(int)
    df["facade_count"] = df["facade_count"].astype(int)
    df["furnished"] = df["furnished"].astype(bool)
    df["swimmingpool"] = df["swimmingpool"].astype(bool)

    estimation = model_apart.predict(df)
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
    return jsonify({"estimation": str(estimation)})


if __name__ == "__main__":
    app.run(debug=True)
