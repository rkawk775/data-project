# subway_etl_dag.py : Airflow DAG 구축
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from etl.ingestion.subway_api import fetch_realtime_train_data
from etl.processing.transform import transform_train_data
from etl.processing.headway import calculate_headway
from etl.storage.postgres import (
    save_data,
    save_headway_data
)


def run_etl():
    df = fetch_realtime_train_data()
    processed_df = transform_train_data
    save_data(processed_df)
    headway_df = calculate_headway(processed_df)
    save_headway_data(headway_df)


default_args = {
    "owner": "admin"
}

with DAG(
    dag_id = "subway_realtime_etl",
    default_args = default_args,
    start_data = datetime(2026,5,22),
    schedule="@minute",
    catchup=False
) as dag:
    
    etl_task = PythonOperator(
        task_id = "run_subway_etl",
        python_callable=run_etl
    )
