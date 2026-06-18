### 🚋 Subway Congestion Analytics Pipeline

---

### 프로젝트 소개

본 프로젝트는 출퇴근 시간대 발생하는 지하철 혼잡 및 배차 문제를 데이터 기반으로 분석하기 위해 구축한 데이터 엔지니어링 프로젝트입니다.

지하철 혼잡은 단순한 승객 증가뿐만 아니라 열차 지연, 배차 간격 불균형, 특정 구간의 열차 밀집 현상 등 다양한 요인이 복합적으로 작용하여 발생합니다.

이를 분석하기 위해 서울 열린데이터 API 기반의 승하차 인원 데이터, 실시간 열차 위치 데이터, 혼잡도 데이터를 수집하는 ETL Pipeline을 구축하였으며, Airflow를 활용하여 데이터 수집·전처리·적재 과정을 자동화했습니다.

또한 PostgreSQL 기반 데이터 저장 구조를 설계하여 역별 이용량, 시간대별 혼잡 패턴, 열차 운행 상태를 분석할 수 있는 환경을 구성했습니다.

<br>

### 프로젝트 목표

본 프로젝트의 목표는 단순히 지하철 혼잡 현상을 조회하는 것을 넘어, 혼잡이 발생하는 원인을 데이터 기반으로 설명할 수 있는 구조를 구축하는 것입니다.

이를 위해 다음과 같은 분석 데이터를 생성했습니다.

- 승하차 데이터 기반 역별 이용량 분석
- 시간대별 혼잡도 분석
- Headway(배차 간격) 분석을 통한 열차 간 운행 간격 확인
- Train Density(열차 밀집도) 분석을 통한 특정 구간 열차 집중 현상 분석

최종적으로 승객 흐름, 열차 운행 상태, 혼잡 패턴 데이터를 통합하여 "왜 특정 시간과 구간에서 혼잡이 발생하는가"를 설명할 수 있는 데이터 구조 구축을 목표로 합니다.

<br>

## Architecture
<div align="center">
  <img width="70%" alt="PipeLine Architecture" src="https://github.com/user-attachments/assets/bf6165c7-e93a-4c36-adb0-8a52742f8178" />
</div>


## Data Pipeline
서울 열린데이터 API 데이터를 기반으로 목적별 ETL Pipeline을 구성했습니다.

<div align="center">
  <img width="70%" alt="DataPipeline" src="https://github.com/user-attachments/assets/819e0cf9-39b2-4add-a597-a3bcfb534049" />
</div>



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



## Database Schema

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

## Troubleshooting

## 프로젝트 결과 및 회고
