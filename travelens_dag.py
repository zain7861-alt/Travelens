from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="travellens_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False
) as dag:
    from airflow.operators.bash import BashOperator

from airflow.operators.python import PythonOperator

def extract_data():
    print("Reading flights.csv")
    print("Flight data extracted successfully")

extract = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data
)
def transform_data():
    print("Cleaning flight data")
    print("Handling missing delay values")
    print("Creating flight status")
    print("Flight data transformed successfully")


transform = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data
)
extract >> transform
def load_data():
    print("Loading transformed data into DuckDB")
    print("Table flights_cleaned created successfully")


load = PythonOperator(
    task_id="load_data",
    python_callable=load_data
)
extract >> transform >> load
def analyze_data():
    print("Calculating average delay by airline")
    print("Finding cancelled flights by airline")
    print("Finding busiest routes")
    print("Flight analysis completed successfully")


analyze = PythonOperator(
    task_id="analyze_data",
    python_callable=analyze_data
)
extract >> transform >> load >> analyze