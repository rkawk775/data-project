# 혼잡도 API 전처리
from etl.common.config import TARGET_LINE

# 특정 호선만 추출
def filter_line(df):

    df = df[
        df["LINE"] == TARGET_LINE
    ]

    return df


# 평일 데이터만 추출
def filter_weekday(df):

    df = df[
        df["DOW_SE"] == "평일"
    ]
    return df


# 시간대 최대 혼잡도 계산
def calculate_max_congestion(df):

    time_colums = [
        col for col in df.columns
        if col.startswith("TIME")
    ]

    df["MAX_CONGESTION"] = (
        df[time_colums].max(axis=1)
    )

    return df


# 최대 혼잡 시간 계산
def calculate_peak_time(df):

    time_colums = [
        col for col in df.columns
        if col.startswith("TIME")
    ]

    df["PEAK_TIME"] = (
        df[time_colums].idxmax(axis=1)
    )

    return df