# headway.py : 배차 간격 계산
import pandas as pd


# 같은 역 + 같은 방향 기준 / 열차 간 시간 차 계산
def calculate_headway(df):
    df = df.copy()

    # 시간 컬럼 datetime 변환
    # unit='ms' 명시 필요
    df["recptnDt"] = pd.to_datetime(df["recptnDt"])

    # 역 + 방향 + 시간 기준 정렬
    df = df.sort_values(by=["statnNm", "updnLine", "recptnDt"])

    # 이전 열차 시간
    df["previous_time"] = (
        df.groupby(["statnNm", "updnLine"])["recptnDt"].shift(1)
    )

    # 배차 간격(초)
    df["HEADWAY_SECONDS"] = (
        df["recptnDt"] - df["previous_time"]
    ).dt.total_seconds()

    return df