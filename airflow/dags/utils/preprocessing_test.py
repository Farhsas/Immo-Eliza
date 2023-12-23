import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
import pickle


# Function to filter rows with invalid postal codes
def filter_invalid_postal_codes(df, column_name):
    """
    Removes rows with invalid postal codes (not exactly 4 digits) from the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column containing postal codes.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    try:
        # Define the regular expression pattern for exactly 4 digits
        pattern = r"^\d{4}$"
        # Use str.match() to filter rows with invalid postal codes
        df = df[df[column_name].astype(str).str.match(pattern)]
    except Exception as e:
        print(f"Error filtering invalid postal codes in column '{column_name}': {e}")

    return df


# Function to perform one-hot encoding
def one_hot_encode(df, column_name):
    """
    Performs one-hot encoding on a categorical column in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to be one-hot encoded.

    Returns:
        pd.DataFrame: The DataFrame with the one-hot encoded column.
    """
    df[column_name] = df[column_name].astype("category")
    enc = OneHotEncoder()
    encoded_data = enc.fit_transform(df[[column_name]]).toarray()
    pickle.dump(enc, open(f"airflow/dags/model/{column_name}_encoded.pkl", "wb"))
    encoded_columns = enc.get_feature_names_out([column_name])
    enc_data = pd.DataFrame(encoded_data, columns=encoded_columns)
    df = pd.concat([df, enc_data], axis=1)
    return df


# Create a new feature Price per square meter per postal code
def new_features(df):
    """
    Create new features in a pandas DataFrame based on mean values by postal code.

    This function calculates the mean price and mean living area for each postal code
    and creates new features such as 'Price_mean/PostalCode' and 'LivingArea_mean/PostalCode'.
    It also computes the 'Price/SQMeter/PostalCode' feature by dividing the mean price by the mean living area.

    Parameters:
    - df (pd.DataFrame): The input pandas DataFrame with real estate data.

    Returns:
    - pd.DataFrame: A DataFrame with the added new features.
    """
    # Calculate mean price by postal code
    mean_price_by_postal = df.groupby("PostalCode")["Price"].mean().reset_index()
    # Calculate mean living area by postal code
    mean_living_area_by_postal = (
        df.groupby("PostalCode")["LivingArea"].mean().reset_index()
    )

    # Merge mean price and mean living area back into the DataFrame
    df = df.merge(
        mean_price_by_postal, on="PostalCode", suffixes=("", "_mean/PostalCode")
    )
    df = df.merge(
        mean_living_area_by_postal, on="PostalCode", suffixes=("", "_mean/PostalCode")
    )

    # Calculate 'Price/SQMeter/PostalCode' by dividing mean price by mean living area
    df["Price/SQMeter/PostalCode"] = (
        df["Price_mean/PostalCode"] / df["LivingArea_mean/PostalCode"]
    )

    df_encoded = df[
        [
            "PostalCode",
            "Price_mean/PostalCode",
            "LivingArea_mean/PostalCode",
            "Price/SQMeter/PostalCode",
        ]
    ].copy()

    df_encoded.drop_duplicates(inplace=True)

    pickle.dump(df_encoded, open("airflow/dags/model/preprocessed.pkl", "wb"))

    return df


# Function to perform preprocessing
def preprocessing(type):
    """
    Performs preprocessing on the input DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
    if type == "houses":
        df = pd.read_csv("airflow/dags/datasets/houses_data.csv", engine="pyarrow")
    elif type == "apartments":
        df = pd.read_csv(
            "airflow/dags/datasets/apartments_data.csv",
            engine="pyarrow",
        )

    df = df.drop("LocalityName", axis=1)
    df = df.dropna(subset="Price")
    df = df.dropna(subset="PostalCode")
    df = filter_invalid_postal_codes(df, "PostalCode")
    df = df.astype({"PostalCode": int})

    # Romvove outliers based on price using IQR
    Q1 = df["Price"].quantile(0.25)
    Q3 = df["Price"].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df["Price"] < (Q1 - 1.5 * IQR)) | (df["Price"] > (Q3 + 1.5 * IQR)))]
    print("Outliers removed")

    # Create the new feature Price per square meter per postal code
    df = new_features(df)

    df_temp = df[["TypeOfProperty", "SubtypeOfProperty", "StateOfBuilding"]].copy()
    enc = OneHotEncoder()
    encoded_data = enc.fit_transform(df_temp).toarray()
    pickle.dump(enc, open("airflow/dags/model/encoded.pkl", "wb"))

    df = df.drop(
        [
            "PropertyID",
            "TypeOfProperty",
            "SubtypeOfProperty",
            "StateOfBuilding",
            "TypeOfSale",
            "Unnamed: 0",
        ],
        axis=1,
    )
    df_temp = pd.DataFrame(
        encoded_data,
        columns=enc.get_feature_names_out(
            ["TypeOfProperty", "SubtypeOfProperty", "StateOfBuilding"]
        ),
    )
    df = pd.concat([df, df_temp], axis=1)

    print("Preprocessing Done")
    print(df.columns)

    return df
