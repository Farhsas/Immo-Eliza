import pandas as pd
import datetime


def merge_data(type):
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    if type == "houses":
        try:
            df = pd.read_csv(
                f"airflow/dags/datasets/houses_data/houses_data_{yesterday}.csv"
            )
        except:
            df = pd.read_csv(
                f"airflow/dags/datasets/houses_data/houses_data_{today}.csv"
            )

        df2 = pd.read_csv(f"airflow/dags/datasets/houses_data.csv")

        df_final = df.merge(df2, how="outer")
        df_final.to_csv("airflow/dags/datasets/houses_data.csv", index=False)

    elif type == "apartments":
        try:
            df = pd.read_csv(
                f"airflow/dags/datasets/apartments_data/apartments_data_{yesterday}.csv"
            )
        except:
            df = pd.read_csv(
                f"airflow/dags/datasets/apartments_data/apartments_data_{today}.csv"
            )

        df2 = pd.read_csv(f"airflow/dags/datasets/apartments_data.csv")

        df_final = df.merge(df2, how="outer")
        df_final.to_csv("airflow/dags/datasets/apartments_data.csv", index=False)
