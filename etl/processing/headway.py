#headway.py : 배차 간격 계산
import pandas as pd

# 같은 역+같은 방향 기준 / 열차 간 시간 차 계산
def  calculate_headway(df):

    # 시간 컬럼 datetime 변환
    df["recptnDt"] = pd.to_datetime(df["recptnDt"])

    # 역+방향+시간 기준 정렬
    df = df.sort_values(
        by=["statnNm", "updnLine", "recptnDt"]
    )

    # 이전 열차 시간 가져오기
    df["previous_time"] = df.groupby(
        ["statnNm","updnLine"]
    )["recptnDt"].shift(1)

    # Headway 계산 (초 단위)
    df["headway_set"] = (
        df["recptnDt"] - df["previous_time"]
    ).dt.total_seconds()

    # 간단 혼잡 정수
    df['CONGESTION_SCORE'] =(
        df['TOTAL_PASSENGERS'] / 1000
    )

    # 환승 병목 점수
    df['TRANSFER_SCORE'] = (
        df['GTON_TNOPE'] * df['GTOFF_TNOPE']
    )

    return df

# 혼잡도 계산, 배차 간격 분석, 지연 분석
# def calculate_congestion(df):
#     df['TOTAL_PASSENGERS'] = (
#         df['GTON_TNOPE'] + 
#         df['GTOFF_TNOPE']
#     )

#     return df