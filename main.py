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
raw_data = fetch_subway_data(date)
# 2. 데이터 변환
df = transform_subway_data(raw_data)
# 3. 혼잡도 계산
df = calculate_passenger_congestion(df)
# 4. 결과 확인
print(df.head())
# 5. 저장
# save_subway_csv(df,"subway_congestion.csv")
save_subway_postgres(df)





# # 실제 ETL 파이프라인 구축
# df = fetch_realtime_train_data()
# logger.info("실시간 데이터 수집 완료")

# processed_df = transform_train_data(df)
# logger.info("데이터 가공 완료")

# save_data(processed_df)

# headway_df = calculate_headway(processed_df)
# logger.info("Headway 계산 완료")

# save_headway_data(headway_df)


# # 반복 수집 : 실시간 데이터 누적 저장
# while True:
#     df = fetch_realtime_train_data()
#     processed_df = transform_train_data(df)
#     save_data(processed_df)
#     logger.info("ETL완료")
#     time.sleep(COLLECT_INTERVAL)