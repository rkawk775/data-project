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
from datetime import timedelta
from common.logger import logger



# Task 1 : API 수집
def fetch_passenger_task(**context):

    logger.info(f"Passenger Fetch Start")

    try:
        execution_date = (
            context["logical_date"]
            - timedelta(days=2)
        ).strftime("%Y%m%d")

        logger.info(f"조회 날짜 : {execution_date}")

        df = fetch_subway_data(execution_date)

        if df.empty:
            raise ValueError("Passenger API 응답 데이터 없음")

        logger.info(f"Passenger API 수집 완료 : {len(df)} rows")

        return df.to_json()
    
    except Exception as e:
        logger.error(f"Passenger API 실패 : {e}")
        raise


# Task 2 : Transform
def transform_passenger_task(ti):
    try: 
        logger.info(f"Passenger Transform Start")

        data = ti.xcom_pull( task_ids="fetch_passenger_data")
        if data is None:
            raise ValueError("fetch_passenger_data로부터 데이터 없음 (xcom_pull 결과 None)")
        
        df = pd.read_json(data)
        if df.empty:
            raise ValueError("JSON 파싱 후 데이터 없음")
        
        df = transform_subway_data(df)
        df = calculate_passenger_congestion(df)

        logger.info(f"전처리 데이터: {len(df)} rows")

        return df.to_json()
    
    except Exception as e:
        logger.error(f"Passenger Transform 실패 : {e}")
        raise



# Task 3 : Load
def load_passenger_task(ti):
    try:
        logger.info(f"Passenger Load Start")

        data = ti.xcom_pull( task_ids="transform_passenger_data" )
        if data is None:
            raise ValueError("transform_passenger_data로부터 데이터 없음 (xcom_pull 결과 None)")
        
        df = pd.read_json(data)
        if df.empty:
            raise ValueError("JSON 파싱 후 데이터 없음")
        
        save_passenger_data(df)

        logger.info(f"Passenger ETL 완료")
    
    except Exception as e:
        logger.error(f"Passenger Load 실패 : {e}")
        raise




default_args = {
    "owner" : "airflow",
    "retries" : 3,
    "retry_delay" : timedelta(minutes=5)
}

with DAG(
    dag_id="subway_passenger_etl",
    default_args=default_args,
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