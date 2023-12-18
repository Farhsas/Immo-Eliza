# Real Estate Price Prediction Project

This project uses Python and the Airflow library to scrape real estate data and train a machine learning model to predict real estate prices.

## Project Structure

The main script of this project is `immo-eliza-dag.py`, which defines an Airflow DAG (Directed Acyclic Graph) for the data pipeline.

The pipeline consists of two main steps:

1. **Data Scraping**: The `houses_scraper_task` and `apartments_scraper_task` functions are used to scrape data about houses and apartments, respectively. These functions use the `houses_scraper` and `apartments_scraper` functions from the `utils.scraping` module.

2. **Model Training**: The `main_training` function from the `utils.ml` module is used to train a machine learning model on the scraped data.

## Installation

To install the necessary dependencies for this project, you can use pip:

```sh
pip install -r requirements.txt