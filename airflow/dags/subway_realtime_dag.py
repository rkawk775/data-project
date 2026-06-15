# subway_realtime_dag.py 
# 실시간 열차 수집 → 전처리 → 배차간격 계산 → PostgreSQL 저장

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from etl.ingestion import fetch_realtime_train_data
from etl.processing import (
    transform_train_data,
    calculate_headway,
    cacluate_train_density
)
from etl.storage import (
    save_data,
    save_headway_data,
    save_density_data
)


def run_realtime_etl():
    
    # 1. API 수집
    df = fetch_realtime_train_data()
    print("수집 데이터: ", len(df))

    # 2. 데이터 전처리
    processed_df = transform_train_data(df)
    print("전처리 데이터: ", len(processed_df))

    # 3. 배차 간격 분석
    headway_df = calculate_headway(processed_df)
    print("배차 분석 데이터: ", len(headway_df))

    # 4. 열차 간 밀집도 분석
    density_df = cacluate_train_density(df)
    print("배차 분석 데이터: ", len(density_df))

    # 5. PostgreSQL 저장
    save_data(processed_df)
    save_headway_data(headway_df)
    save_density_data(density_df)
    print("Realtime ETL 완료")

with DAG(
    dag_id = "subway_realtime_etl",
    start_date=datetime(2026,6,1),
    schedule="@hourly",
    catchup=False,
    tags=["subway","realtime"]
) as dag:
    
    realtime_task = PythonOperator(
        task_id="run_realtime_etl",
        python_callable=run_realtime_etl
    )