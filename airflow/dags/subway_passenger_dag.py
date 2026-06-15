# subway_passenger_dag.py
# 승하차 수집 → 전처리 → 혼잡도 계산 → PostgreSQL 저장
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from etl.ingestion import fetch_subway_data
from etl.processing import (
    transform_subway_data,
    calculate_passenger_congestion
)
from etl.storage import save_passenger_data



# Task 1 : API 수집

def fetch_passenger_task():

    print("Passenger Fetch Start")

    df = fetch_subway_data()
    print("수집 데이터:", len(df))

    return df.to_json()



# Task 2 : Transform
def transform_passenger_task(ti):

    print("Passenger Transform Start")

    data = ti.xcom_pull( task_ids="fetch_passenger_data")
    df = pd.read_json(data)
    df = transform_subway_data(df)
    df = calculate_passenger_congestion(df)

    print("전처리 데이터:", len(df))

    return df.to_json()



# Task 3 : Load
def load_passenger_task(ti):

    print("Passenger Load Start")

    data = ti.xcom_pull( task_ids="transform_passenger_data" )
    df = pd.read_json(data)
    save_passenger_data(df)


    print("Passenger ETL 완료")



with DAG(
    dag_id="subway_passenger_etl",
    start_date=datetime(2026,6,1),
    schedule="@daily",
    catchup=False,
    tags=["subway","passenger"]
) as dag:
    

    fetch_task = PythonOperator(
        task_id="fetch_passenger_data",
        python_callable=fetch_passenger_task
    )

    transform_task = PythonOperator(
        task_id="transform_passenger_data",
        python_callable=transform_passenger_task
    )

    load_task = PythonOperator(
        task_id="load_passenger_data",
        python_callable=load_passenger_task
    )

    fetch_task >> transform_task >> load_task