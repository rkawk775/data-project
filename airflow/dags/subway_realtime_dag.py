# subway_realtime_dag.py 
# 실시간 열차 수집 → 전처리 → 배차간격 계산 → PostgreSQL 저장

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def run_realtime_etl():
    print("Realtime ETL Start")

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