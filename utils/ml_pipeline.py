import pandas as pd
import numpy as np
import joblib

from preprocessing import preprocess

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer

from xgboost import XGBRegressor



def ml_pipeline():
    data = pd.read_csv("datasets/houses/houses_data.csv")

    num_cols = ["rooms", "facade_count"]
    cat_cols = ["type_of_property", "subtype_of_property", "state_of_property", "region", "province", "heating", "kitchen"]

    num_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="mean")),
        ("scale", MinMaxScaler())
    ])

    cat_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("one-hot", OneHotEncoder(handle_unknown="ignore"))
    ])

    col_trans = ColumnTransformer(transformers=[
        ("num_pipeline", num_pipeline, num_cols),
        ("cat_pipeline", cat_pipeline, cat_cols)
    ],
    remainder="drop",
    n_jobs=-1)

    regressor = XGBRegressor(
        n_estimators=1000,
        max_depth=7,
        eta=0.1,
        subsample=0.7,
        colsample_bytree=0.8
    )

    regression = Pipeline([
        ("col_trans", col_trans),
        ("regression", regressor)
    ])

    data = data.dropna(subset=["price"])

    X = data.drop("price", axis=1)
    y = data["price"].values

    model = regression.fit(X, y)

    joblib.dump(model, "models/pipeline.joblib")


if __name__ == "__main__":
    ml_pipeline()
