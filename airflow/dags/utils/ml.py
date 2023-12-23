import pandas as pd
import catboost as cb
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from utils.preprocessing_test import preprocessing
import pickle


def training(df, type):
    """
    Trains a CatBoostRegressor model using the provided dataframe.

    Args:
        df (pandas.DataFrame): The dataframe containing the training data.

    Returns:
        dict: A dictionary containing the evaluation scores of the trained model.
            The dictionary has the following keys:
            - 'r2': The R-squared score of the model on the test set.
            - 'mae': The mean absolute error of the model on the test set.
    """
    immo = df

    X = immo.drop("Price", axis=1)
    y = immo["Price"].values
    print(X.shape, y.shape)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    training_set = cb.Pool(X_train, y_train)
    test_set = cb.Pool(X_test, y_test)

    catboost = cb.CatBoostRegressor(
        n_estimators=2000,
        depth=10,
        learning_rate=0.05,
        subsample=0.5,
        colsample_bylevel=0.5,
        min_data_in_leaf=50,
    )

    model = catboost.fit(training_set, eval_set=test_set)

    if type == "houses":
        pickle.dump(model, open("airflow/dags/ML_Models/catboost_houses.pkl", "wb"))

    elif type == "apartments":
        pickle.dump(model, open("airflow/dags/ML_Models/catboost_apartments.pkl", "wb"))

    scores = {
        "r2": catboost.score(test_set),
        "mae": mean_absolute_error(y_test, catboost.predict(test_set)),
    }
    return scores


def houses_training():
    df = preprocessing(type="houses")
    df.dropna(subset="Price", inplace=True)

    model = training(df, "houses")


def apartments_training():
    df = preprocessing(type="apartments")
    df.dropna(subset="Price", inplace=True)

    model = training(df, "apartments")
