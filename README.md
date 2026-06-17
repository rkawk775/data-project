# Subway ETL Pipeline

## 프로젝트 소개

## Architecture
<div align="center">
  <img width="70%" alt="PipeLine Architecture" src="https://github.com/user-attachments/assets/bf6165c7-e93a-4c36-adb0-8a52742f8178" />
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

<div align="center">
  <img width="80%" alt="DAG Structure" src="https://github.com/user-attachments/assets/109b4783-0123-4b2e-a676-6f808dc35a10" />
</div>


| DAG                     | 데이터 기준                 | 역할                               | 분석 의미                                    | 실행 주기  |
| ----------------------- | ---------------------- | -------------------------------- | ---------------------------------------- | ------ |
| `subway_passenger_etl`  | 서울 열린데이터 승하차 인원 API    | 승하차 데이터 수집 및 이용량 분석              | **사람 수 기준 혼잡도** (어느 역에 승객이 많이 몰리는지 분석)   | Daily  |
| `subway_realtime_etl`   | 서울 열린데이터 실시간 열차 위치 API | 실시간 열차 위치 수집, 배차간격 계산, 열차 밀집도 분석 | **운행 상태 기반 분석** (열차 간격 및 특정 구간 밀집 여부 확인) | Hourly |
| `subway_congestion_etl` | 서울 열린데이터 혼잡도 API       | 혼잡도 데이터 수집 및 시간대 분석              | **시간대별 혼잡률/혼잡 구간 분석** (언제 가장 붐비는지 분석)    | Daily  |



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


## 실행 방법

## 프로젝트 결과/회고
