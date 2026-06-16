# subway_congestion_dag.py
# 혼잡도 API 수집 → 호선 필터 → 평일 필터 → 최대 혼잡도 계산 → 혼잡 시간 계산 → PostgreSQL 저장
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from etl.ingestion import fetch_congestion_data
from etl.processing import (
    filter_line,
    filter_weekday,
    calculate_max_congestion,
    calculate_peak_time
)
from etl.storage import save_congestion_data


# Task 1. API 수집
def fetch_congestion_task():
    
    df = fetch_congestion_data()
    
    print("혼잡도 수집 데이터: ", len(df))

    return df.to_json()


# Task 2. 전처리
def transform_congestion_task(ti):
    import pandas as pd

    data = ti.xcom_pull(task_ids="fetch_congestion_data")

    df = pd.read_json(data)

    # 1. 특정 호선 필터
    df = filter_line(df)

    # 2. 평일 필터
    df = filter_weekday(df)

    # 3. 최대 혼잡도 계산
    df = calculate_max_congestion(df)

    # 4. 최대 혼잡 시간 계산
    df = calculate_peak_time(df)

    print(df.head())

    return df.to_json()


# Task 3. DB 저장
def load_congestion_task(ti):
    import pandas as pd
    
    data = ti.xcom_pull(task_ids="transform_congestion_data")
    
    df = pd.read_json(data)

    save_congestion_data(df)

    print("Congestion ETL Complete")


with DAG(
    dag_id="subway_congestion_etl",
    start_date=datetime(2026,6,1),
    schedule="@daily",
    catchup=False,
    tags=[ "subway","congestion"]
) as dag:
    
    fetch_congestion_data_task = PythonOperator(
        task_id = "fetch_congestion_data",
        python_callable=fetch_congestion_task
    )

    transform_congestion_data_task = PythonOperator(
        task_id = "transform_congestion_data",
        python_callable=transform_congestion_task
    )

    load_congestion_data_task = PythonOperator(
        task_id = "load_congestion_data",
        python_callable=load_congestion_task
    )

    fetch_congestion_data_task >> transform_congestion_data_task >> load_congestion_data_task