# 승하차 데이터와 혼잡도 데이터를 join하는 파일
import pandas as pd

def join_passenger_congestion(passenger_df, congestion_df):
    merged_df = pd.merge(
        passenger_df,
        congestion_df,
        left_on="SBWY_STNS_NM",
        right_on="DPTRE_STTN",
        how="inner"
    )
    return merged_df

# 혼잡도 최대값 컬럼 생성