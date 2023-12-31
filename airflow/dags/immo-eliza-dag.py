from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
from utils.scraping import houses_scraper, apartments_scraper
from utils.merge_data import merge_data
from utils.ml import houses_training, apartments_training
from utils.optuna import optuna
import os


# Define the current directory path
dag_path = os.getcwd()


# Define the function for scraping houses
def houses_scraper_task():
    """
    Function to scrape houses data.
    """
    houses_scraper()


# Define the function for scraping apartments
def apartments_scraper_task():
    """
    Function to scrape apartments data.
    """
    apartments_scraper()


def merge_houses_data():
    """
    Function to merge houses data.
    """
    merge_data("houses")


def merge_apartments_data():
    """
    Function to merge apartments data.
    """
    merge_data("apartments")


# Define the function for data cleaning during training
def data_cleaning_training_task():
    """
    Function for data cleaning during training.
    """
    pass


# Define the function for data cleaning during analysis
def data_cleaning_analysis_task():
    """
    Function for data cleaning during analysis.
    """
    pass


# Define the function for analysis dashboard
def analysis_dashboard_task():
    """
    Function for analysis dashboard.
    """
    pass


# Define the DAG (Directed Acyclic Graph)
with DAG(
    dag_id="immo-eliza", start_date=datetime(2023, 12, 1), schedule_interval="@daily"
) as dag:
    # Define TaskGroup for scraping tasks
    with TaskGroup("scraping", tooltip="Scraping") as section_1:
        # Define PythonOperator for scraping houses task
        scraping_houses = PythonOperator(
            task_id="scraping_house", python_callable=houses_scraper_task
        )
        # Define PythonOperator for scraping apartments task
        scraping_apartmetns = PythonOperator(
            task_id="scraping_apartments", python_callable=apartments_scraper_task
        )

    with TaskGroup("merging", tooltip="Merging") as section_2:
        # Define PythonOperator for merging houses task
        merge_houses = PythonOperator(
            task_id="merge_houses", python_callable=merge_houses_data
        )
        # Define PythonOperator for merging apartments task
        merge_apartments = PythonOperator(
            task_id="merge_apartments", python_callable=merge_apartments_data
        )

    # Define TaskGroup for data cleaning tasks
    with TaskGroup("data_cleaning", tooltip="Data cleaning") as section_3:
        # Define PythonOperator for data cleaning during training task
        data_cleaning_training = PythonOperator(
            task_id="training_cleaning", python_callable=data_cleaning_training_task
        )
        # Define PythonOperator for data cleaning during analysis task
        data_cleaning_analysis_dag = PythonOperator(
            task_id="analysis_cleaning", python_callable=data_cleaning_analysis_task
        )

    # Define TaskGroup for training and dashboard tasks
    with TaskGroup(
        "training_and_dashboard", tooltip="Training model & Dashboard"
    ) as section_4:
        # Define PythonOperator for analysis dashboard task
        analysis_dashboard_dag = PythonOperator(
            task_id="dashboard", python_callable=analysis_dashboard_task
        )

    # Set the dependencies between TaskGroups
    section_1 >> section_2 >> section_3 >> section_4
