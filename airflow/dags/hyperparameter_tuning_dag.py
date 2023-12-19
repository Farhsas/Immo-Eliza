from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.optuna import optuna_training
from datetime import datetime


def optuna_task():
    """
    Function to optimize hyperparameters.
    """
    optuna_training()


with DAG(
    dag_id="hyperparameter_tuning",
    start_date=datetime(2023, 12, 1),
    schedule_interval="0 0 */14 * *",
) as dag:
    hyperparameter_tuning = PythonOperator(
        task_id="tuning", python_callable=optuna_task
    )
    # Set the dependencies
    hyperparameter_tuning
