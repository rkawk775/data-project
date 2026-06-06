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
    calculate_passenger_congestion
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
congestion_df = transform_congestion_data(congestion_df)

# JOIN
merged_df = join_passenger_congestion(
    passenger_df,
    congestion_df
)

# 병목 분석
bottleneck_df = analyze_bottleneck(merged_df)

# 저장
save_passenger_data(passenger_df)
save_congestion_data(congestion_df)
save_bottleneck_data(bottleneck_df)
