# subway_passenger_dag.py
# 승하차 수집 → 승하차 전처리 → 혼잡도 수집 → 혼잡도 전처리 → JOIN → 병목 분석 → PostgreSQL 저장

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def run_passenger_etl():
    print("Passenger ETL Start")

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