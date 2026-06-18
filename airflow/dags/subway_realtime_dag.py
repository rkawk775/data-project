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
from datetime import timedelta
from common.logger import logger


# Task 1 : API 수집
def fetch_realtime_task():
    try:
        logger.info("Realtime Fetch Start")

        df = fetch_realtime_train_data()

        if df.empty:
            raise ValueError("API 응답 데이터 없음")
        
        logger.info(f"수집 데이터: {len(df)} rows")

        return df.to_json()
    
    except Exception as e:
        logger.error(f"Realtime Fetch 실패 : {e}")
        raise


# Task 2 : Transform + 분석
def transform_realtime_task(ti):
    try:
        logger.info("Realtime Transform Start")

        data = ti.xcom_pull( task_ids="fetch_realtime_data" )
        if data is None:
            raise ValueError("fetch_realtime_data로부터 데이터 없음 (xcom_pull 결과 None)")
    
        df = pd.read_json(data)
        if df.empty:
            raise ValueError("JSON 파싱 후 데이터 없음")

        processed_df = transform_train_data(df)
        headway_df = calculate_headway(processed_df)
        density_df = cacluate_train_density(processed_df)

        logger.info(f"Transform 완료 - processed: {len(processed_df)}, headway: {len(headway_df)}, density: {len(density_df)}")

        return {
            "processed": processed_df.to_json(),
            "headway": headway_df.to_json(),
            "density": density_df.to_json()
        }
    
    except Exception as e:
        logger.error(f"Realtime Transform 실패 : {e}")
        raise


# Task 3 : Load
def load_realtime_task(ti):
    try:
        logger.info("Realtime Load Start")

        result = ti.xcom_pull(task_ids="transform_realtime_data")
        if result is None:
            raise ValueError("transform_realtime_data로부터 데이터 없음 (xcom_pull 데이터 없음)")
        
        processed_df = pd.read_json(result["processed"])
        headway_df = pd.read_json(result["headway"])
        density_df = pd.read_json(result["density"])

        if processed_df.empty or headway_df.empty or density_df.empty:
            raise ValueError(f"JSON 파싱 후 데이터 없음 -  processed: {len(processed_df)}, headway: {len(headway_df)}, density: {len(density_df)}")

        # XCom 직렬화로 인해 datetime이 밀리초 int로 변환됨 → 재변환 필요
        processed_df["recptnDt"] = pd.to_datetime(processed_df["recptnDt"])
        headway_df["recptnDt"] = pd.to_datetime(headway_df["recptnDt"])
        headway_df["previous_time"] = pd.to_datetime(headway_df["previous_time"])
        density_df["recptnDt"] = pd.to_datetime(density_df["recptnDt"])

        save_data(processed_df)
        save_headway_data(headway_df)
        save_density_data(density_df)

        logger.info("Realtime ETL 완료")

    except Exception as e:
        logger.error(f"Realtime Load 실패: {e}")
        raise


default_args = {
    "owner" : "airflow",
    "retries" : 3 ,
    "retry_delay" : timedelta(minutes=5)
}


with DAG(
    dag_id="subway_realtime_etl",
    default_args=default_args,
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