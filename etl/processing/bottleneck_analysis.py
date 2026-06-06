# 병목 현상이 발생하는 역 분석
import pandas as pd

def analyze_bottleneck(df):
    df["BOTTLENECK_SCORE"] = (
        df["TOTAL_PASSENGERS"] *
        df["MAX_CONGESTION"]
    )

    return df


def get_top10_bottleneck(df):
    return (
        df.sort_values(
            by="BOTTLENECK_SCORE",
            ascending=False
        )
        .head(10)
    )