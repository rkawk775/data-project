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

def run_congestion_etl():
    print("Congestion ETL Start")

    # 1. API 수집
    df = fetch_congestion_data()
    print("수집 데이터: ", len(df))

    # 2. 특정 호선 필터
    df = filter_line(df)
    print("호선 필터 후 : ",len(df))

    # 3. 평일 데이터만 추출
    df = filter_weekday(df)
    print("평일 필터 후: ", len(df))

    # 4. 최대 혼잡도 계산
    df = calculate_max_congestion(df)

    # 5. 최대 혼잡 시간 계산
    df = calculate_peak_time(df)
    print(df.head())

    # 6. PostgreSQL 저장
    save_congestion_data(df)
    print("Congestion ETL Complete")


with DAG(
    dag_id="subway_congestion_etl",
    start_date=datetime(2026,6,1),
    schedule="@daily",
    catchup=False,
    tags=[
        "subway",
        "congestion"
    ]
) as dag:
    
    congetion_task = PythonOperator(
        task_id="run_congestion_etl",
        python_callable=run_congestion_etl
    )