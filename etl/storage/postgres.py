# postgres.py : PostgreSQL 저장 (Load)
from sqlalchemy import create_engine
from common.logger import logger
from common.config import (
    POSTGRES_CONFIG,
    REALTIME_TABLE_NAME,
    HEADWAY_TABLE_NAME,
    PASSENGER_TABLE_NAME,
    CONGESTION_TABLE_NAME,
    BOTTLENECK_TABLE_NAME,
    DENSITY_TABLE_NAME
)

DATABASE_URL = (
    f"postgresql://"
    f"{POSTGRES_CONFIG['user']}:"
    f"{POSTGRES_CONFIG['password']}@"
    f"{POSTGRES_CONFIG['host']}:"
    f"{POSTGRES_CONFIG['port']}/"
    f"{POSTGRES_CONFIG['database']}"
)

engine = create_engine(DATABASE_URL)


# [실시간 열차] 지하철 실시간 열차 위치 정보
def save_data(df):

    df.to_sql(
        name=REALTIME_TABLE_NAME,
        con=engine,
        if_exists="append",
        index=False 
    )
    logger.info("PostgreSQL 저장 완료 : (원본) 지하철 실시간 열차 위치 정보")


# [실시간 열차] 지하철 배차 분석 결과 저장
def save_headway_data(df):

    df.to_sql(
        name=HEADWAY_TABLE_NAME,
        con=engine,
        if_exists="append",
        index=False
    )
    logger.info("PostgreSQL 저장 완료 : 지하철 배차 분석 결과")


# [승하차] 지하철 승하차 데이터 저장
def save_passenger_data(df):
    
    df.to_sql(
        name = PASSENGER_TABLE_NAME,
        con=engine,
        if_exists="replace",
        index=False
    )
    logger.info("PostgreSQL 저장 완료 : 승하차 분석 결과")


# [혼잡도] 지하철 혼잡도 데이터 저장
def save_congestion_data(df):
    
    df.to_sql(
        name=CONGESTION_TABLE_NAME,
        con=engine,
        if_exists="replace",
        index=False
    )
    logger.info("PostgreSQL 저장 완료 : (원본) 혼잡도 데이터")


# 병목 분석 결과 저장
def save_bottleneck_data(df):

    df.to_sql(
        name=BOTTLENECK_TABLE_NAME,
        con=engine,
        if_exists="replace",
        index=False
    )
    logger.info("PostgreSQL 저장 완료 : 병목 분석 결과")


# 열차 밀집도 분석 결과 저장
def save_density_data(df):

    df.to_sql(
        name=DENSITY_TABLE_NAME,
        con=engine,
        if_exists="replace",
        index=False
    )

    logger.info("PostgreSQL 저장 완료 : 열차 밀집도 분석 결과")


# ===================================================

# [승하차] 지하철 승하차 데이터
def save_subway_csv(df, filename):
    df.to_csv(
        filename,
        index=False,
        encoding='utf-8-sig'
    )
    logger.info("CSV 저장 완료 : [승하차] 지하철 승하차 데이터")
