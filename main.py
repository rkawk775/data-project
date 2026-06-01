# main.py : 전체 ETL orchestration
from etl.common.logger import logger
from etl.ingestion import (
    fetch_realtime_train_data,
    fetch_subway_data
)
from etl.processing import (
    transform_train_data,
    transform_subway_data,
    calculate_passenger_congestion,
    get_top10_stations,
    calculate_headway
)
from etl.storage import (
    save_subway_csv,
    save_data,
    save_headway_data,
    save_subway_postgres
)


# 승하차 데이터
date ="20260508"
# 1. 데이터 수집
raw_data = fetch_subway_data()
# 2. 데이터 변환
df = transform_subway_data(raw_data)
# 3. 혼잡도 계산
df = calculate_passenger_congestion(df)
# 4. 결과 확인
#print(df.head())
# 5. 저장
# save_subway_csv(df,"subway_congestion.csv")
# save_subway_postgres(df)
print(
    get_top10_stations(df)[
        [
            "SBWY_ROUT_LN_NM",
            "SBWY_STNS_NM",
            "TOTAL_PASSENGERS",
            "CONGESTION_LEVEL"
        ]
    ]
)
print(df["SBWY_ROUT_LN_NM"].value_counts())


