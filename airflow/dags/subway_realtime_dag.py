# subway_realtime_dag.py
# 실시간 열차 수집 → 전처리 → 분석 → 저장
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
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


# Task 1 : API 수집
def fetch_realtime_task():

    print("Realtime Fetch Start")

    df = fetch_realtime_train_data()

    print("수집 데이터:", len(df))

    return df.to_json()


# Task 2 : Transform + 분석
def transform_realtime_task(ti):

    print("Realtime Transform Start")

    data = ti.xcom_pull( task_ids="fetch_realtime_data" )

    df = pd.read_json(data)

    processed_df = transform_train_data(df)
    headway_df = calculate_headway(processed_df)
    density_df = cacluate_train_density(processed_df)

    return {
        "processed": processed_df.to_json(),
        "headway": headway_df.to_json(),
        "density": density_df.to_json()
    }


# Task 3 : Load
def load_realtime_task(ti):
    print("Realtime Load Start")

    result = ti.xcom_pull(task_ids="transform_realtime_data")
    
    processed_df = pd.read_json(result["processed"])
    headway_df = pd.read_json(result["headway"])
    density_df = pd.read_json(result["density"])

    # XCom 직렬화로 인해 datetime이 밀리초 int로 변환됨 → 재변환 필요
    processed_df["recptnDt"] = pd.to_datetime(processed_df["recptnDt"])
    headway_df["recptnDt"] = pd.to_datetime(headway_df["recptnDt"])
    headway_df["previous_time"] = pd.to_datetime(headway_df["previous_time"])
    density_df["recptnDt"] = pd.to_datetime(density_df["recptnDt"])

    save_data(processed_df)
    save_headway_data(headway_df)
    save_density_data(density_df)

    print("Realtime ETL 완료")



with DAG(
    dag_id="subway_realtime_etl",
    start_date=datetime(2026,6,1),
    schedule="@hourly",
    catchup=False,
    tags=["subway","realtime"]
) as dag:


    fetch_task = PythonOperator(
        task_id="fetch_realtime_data",
        python_callable=fetch_realtime_task
    )

    transform_task = PythonOperator(
        task_id="transform_realtime_data",
        python_callable=transform_realtime_task
    )

    load_task = PythonOperator(
        task_id="load_realtime_data",
        python_callable=load_realtime_task
    )

    fetch_task >> transform_task >> load_task