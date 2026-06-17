# Subway ETL Pipeline

## 프로젝트 소개

## Architecture
API
 ↓
Airflow
 ↓
ETL
 ↓
PostgreSQL


## Data Pipeline

1. Passenger ETL
- 승하차 데이터 수집
- 혼잡도 계산
- PostgreSQL 저장

2. Realtime ETL
- 실시간 열차 위치 수집
- 배차 간격 분석
- 열차 밀집도 분석

3. Congestion ETL
- 혼잡도 데이터 수집
- 최대 혼잡 시간 분석


## Tech Stack

Python
Apache Airflow
PostgreSQL
Docker
DBeaver


## DAG Structure

subway_passenger_etl
(fetch)
 →
(transform)
 →
(load)


subway_realtime_etl
(fetch)
 →
(transform)
 →
(load)


## Database Tables

subway_passenger

realtime_train_location

train_headway

train_density

subway_congestion
