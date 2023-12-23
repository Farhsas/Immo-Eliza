from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from utils.ml import houses_training, apartments_training
from datetime import datetime


# Define the function for training the model
def houses_model_task():
    """
    Function to train the machine learning model.
    """
    houses_training()


def apartments_model_task():
    """
    Function to train the machine learning model.
    """
    apartments_training()


with DAG(
    dag_id="model_training",
    start_date=datetime(2023, 12, 1),
    schedule_interval="@weekly",
) as dag:
    # Define TaskGroup for training tasks
    with TaskGroup("training", tooltip="Training") as section_1:
        # Define PythonOperator for training houses task
        training_houses = PythonOperator(
            task_id="training_house", python_callable=houses_model_task
        )
        # Define PythonOperator for training apartments task
        training_apartments = PythonOperator(
            task_id="training_apartment", python_callable=apartments_model_task
        )

    section_1
