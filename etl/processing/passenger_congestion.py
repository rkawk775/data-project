# 호선/역별 승하차 인원 전용 : 분석 컬럼 생성 담당
import pandas as pd


def calculate_passenger_congestion(df):
    # 총 승객 수
    df["TOTAL_PASSENGERS"] = (
        df["GTON_TNOPE"] + 
        df["GTOFF_TNOPE"]
    )

    # 혼잡도 등급
    df["CONGESTION_LEVEL"] = pd.cut(
        df["TOTAL_PASSENGERS"],
        bins = [0,20000,50000,100000,999999],
        labels = ["LOW","MID","HIGH","VERY_HIGH"]
    )
    return df