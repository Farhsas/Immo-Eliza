from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.ml import model_training
from datetime import datetime


# Define the function for training the model
def training_model_task():
    """
    Function to train the machine learning model.
    """
    model_training()


with DAG(
    dag_id="model_training",
    start_date=datetime(2023, 12, 1),
    schedule_interval="@weekly",
) as dag:
    training_model = PythonOperator(
        task_id="training", python_callable=training_model_task
    )
    # Set the dependencies
    training_model
