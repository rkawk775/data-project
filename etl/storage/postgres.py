# postgres.py : PostgreSQL 저장 (Load)
from sqlalchemy import create_engine
from etl.common.config import (
    POSTGRES_CONFIG,
    REALTIME_TABLE_NAME,
    HEADWAY_TABLE_NAME
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

# 지하철 실시간 열차 위치 정보
def save_data(df):

    df.to_sql(
        name=REALTIME_TABLE_NAME,
        con=engine,
        if_exists="append",
        index=False 
    )


# 지하철 배차 분석 결과 저장
def save_headway_data(df):

    df.to_sql(
        name=HEADWAY_TABLE_NAME,
        con=engine,
        if_exists="append",
        index=False
    )


# 지하철 승하차 데이터
def save_subway_csv(df, filename):
    df.to_csv(
        filename,
        index=False,
        encoding='utf-8-sig'
    )

# def save_subway_postgres(df)