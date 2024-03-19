import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder



def filter_invalid_postal_code(df, column_name):
    try:
        pattern = r"^\d{4}$"
        df = df[df[column_name].astype(str).str.match(pattern)]

    except Exception as er:
        print(f"Error filtering postal codes: {er}")

    return df

def one_hot_encoding(df, type):
    i = type
    df_act = df
    df_temp = df_act[["type_of_property", "subtype_of_property", "state_of_property", "region", "province", "heating", "kitchen"]]
    print(df_act)

    enc = OneHotEncoder()
    encoded_data = enc.fit_transform(df_temp).toarray()
    pickle.dump(enc, open(f"models/preprocessing_{i}.pkl", "wb"))

    df = df.drop([
        "property_id",
        "type_of_property",
        "subtype_of_property",
        "state_of_property",
        "region",
        "province",
        "heating",
        "kitchen"
    ],
    axis=1)

    df_temp = pd.DataFrame(
        encoded_data,
        columns=enc.get_feature_names_out(
            ["type_of_property", "subtype_of_property", "state_of_property", "region", "province", "heating", "kitchen"]
    ))

    df = pd.concat([df, df_temp], axis=1)

    return df

def set_boolean(df, column_name):
    df[column_name] = df[column_name].fillna(value=False)

    return df


def preprocess(df):
    df = df.dropna(subset=["postal_code"])
    df = filter_invalid_postal_code(df, "postal_code")
    df = df.astype({"postal_code": int})

    Q1 = df["price"].quantile(0.25)
    Q3 =  df["price"].quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR

    df = df[(df["price"] > lower) & (df["price"] < upper)]

    print("Preprocessing Done!")

    return df
