import pickle
import pandas as pd

from preprocessing import preprocess
from xgboost import XGBRegressor


def regression(type):
    if type == "houses":
        df = pd.read_csv("datasets/houses/houses_cleaned.csv")
        print(df["price"].isna().sum())
        print("Training on Houses data!")
    elif type == "apartments":
        df = pd.read_csv("datasets/apartments/apartments_cleaned.csv")
        print(df["price"].isna().sum())
        print("Training on Apartments data!")
    else:
        return

    X = df.drop("price", axis=1)
    y = df["price"].values

    xgb = XGBRegressor(
       n_estimators=1000,
       max_depth=7,
       eta=0.1,
       subsample=0.7,
       colsample_bytree=0.8
    )
    model = xgb.fit(X, y)
    print("Training Done!")

    if type == "houses":
        pickle.dump(model, open("models/xgb_houses.pkl", "wb"))
    elif type == "apartments":
        pickle.dump(model, open("models/xgb_apartments.pkl", "wb"))

if __name__ == "__main__":
    regression("houses")
    regression("apartments")
