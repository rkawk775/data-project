# Subway ETL Pipeline

## 프로젝트 소개

## Architecture
<div align="Architecture">
  <img width="50%" alt="PipeLine Architecture" src="https://github.com/user-attachments/assets/bf6165c7-e93a-4c36-adb0-8a52742f8178" />
</div>


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

## Data Quality Check

- NULL 데이터 검증
- 중복 데이터 제거
- 수집 데이터 건수 검증
- API 응답 실패 처리

## Scheduling

- Passenger ETL : Daily
- Realtime ETL : Interval
- Congestion ETL : Daily

## 실행 방법

## 프로젝트 결과/회고
