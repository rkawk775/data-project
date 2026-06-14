# subway_passenger_dag.py
# 승하차 수집 → 승하차 전처리 → 혼잡도 수집 → 혼잡도 전처리 → JOIN → 병목 분석 → PostgreSQL 저장

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from etl.ingestion import fetch_subway_data
from etl.processing import (
    transform_subway_data,
    calculate_passenger_congestion
)
from etl.storage import save_passenger_data


def run_passenger_etl():
    print("Passenger ETL Start")

    # 1. API 수집
    df = fetch_subway_data()
    print("수집 데이터: ", len(df))

    # 2. 전처리
    df = transform_subway_data(df)
    print("전처리 데이터: ", len(df))

    # 3. 혼잡 분석 컬럼 생성
    df = calculate_passenger_congestion(df)
    print(df.head())

    # 4. PostgreSQL 생성
    save_passenger_data(df)
    print("Passenger ETL 완료")

with DAG(
    dag_id="subway_passenger_etl",
    start_date=datetime(2026,6,1),
    schedule="@daily",
    catchup=False,
    tags=["subway","passenger"]
) as dag:
    
    passenger_task = PythonOperator(
        task_id="run_passenger_etl",
        python_callable=run_passenger_etl
    )