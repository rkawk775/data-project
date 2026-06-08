from etl.ingestion.congestion_api import fetch_congestion_data
from etl.processing.bottleneck_analysis import analyze_bottleneck
from etl.processing.passenger_congestion_join import join_passenger_congestion
from etl.storage import (
    save_passenger_data,
    save_congestion_data,
    save_bottleneck_data
)
from etl.processing import(
    transform_subway_data,
    calculate_passenger_congestion,
    filter_line,
    filter_weekday,
    calculate_peak_time,
    calculate_max_congestion
)
from etl.ingestion import (
    fetch_subway_data,
)

# 승하차
passenger_df = fetch_subway_data()
passenger_df = transform_subway_data(passenger_df)
passenger_df = calculate_passenger_congestion(passenger_df)

# 혼잡도
congestion_df = fetch_congestion_data()
congestion_df = filter_line(congestion_df)
congestion_df = filter_weekday(congestion_df)
congestion_df = calculate_max_congestion(congestion_df)
congestion_df = calculate_peak_time(congestion_df)

# JOIN
merged_df = join_passenger_congestion(
    passenger_df,
    congestion_df
)

# 병목 분석
bottleneck_df = analyze_bottleneck(merged_df)

print()

print("==== 데이터 건수 확인 ====")

print("승하차 : ", len(passenger_df))
print("혼잡도 : ", len(congestion_df))
print("JOIN : ", len(merged_df))
print("병목 : ", len(bottleneck_df))

print()

print(
    merged_df[
        [
            "SBWY_STNS_NM",
            "TOTAL_PASSENGERS",
            "MAX_CONGESTION",
            "PEAK_TIME"
        ]
    ].head()
)

print()

passenger_station = set(passenger_df["SBWY_STNS_NM"])
congestion_station = set(congestion_df["DPTRE_STTN"])

print("승하차만 있는 역")
print(passenger_station - congestion_station)

print("혼잡도만 있는 역")
print(congestion_station - passenger_station)

print(passenger_station - congestion_station)
print(congestion_station - passenger_station)

# 저장
# save_passenger_data(passenger_df)
# save_congestion_data(congestion_df)
# save_bottleneck_data(bottleneck_df)
