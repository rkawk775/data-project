### 🚋 Subway Congestion Analytics Pipeline

---

### 프로젝트 소개

본 프로젝트는 출퇴근 시간대 지하철 혼잡 및 배차 문제를 데이터 기반으로 분석하기 위해 수행한 데이터 엔지니어링 프로젝트입니다.

지하철 혼잡은 단순한 승객 증가뿐 아니라 열차 지연, 배차 간격 불균형, 특정 구간의 열차 밀집 현상 등 다양한 요인이 복합적으로 작용하여 발생합니다.

이를 분석하기 위해 서울 열린데이터 API의 승하차 인원 데이터, 실시간 열차 위치 데이터, 혼잡도 데이터를 수집하는 ETL Pipeline을 구축하였으며, Airflow를 활용하여 데이터 수집·전처리·적재 과정을 자동화했습니다.

또한 배차 간격(Headway), 열차 밀집도(Train Density), 시간대별 혼잡도 분석 데이터를 생성하여 역별 이용량, 열차 운행 상태, 혼잡 패턴을 분석할 수 있는 데이터 환경을 구성했습니다.

최종적으로 본 프로젝트는 단순한 혼잡 현상 조회를 넘어, **"왜 특정 시간과 구간에서 혼잡이 발생하는가"를 설명할 수 있는 데이터 구조를 구축** 하는 것을 목표로 합니다.


## 프로젝트 목표


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
