# main.py : 전체 ETL orchestration
from etl.ingestion.subway_api import fetch_realtime_train_data
from etl.processing.transform import transform_train_data
from etl.storage.postgres import save_data



# 실제 ETL 파이프라인 구축
df = fetch_realtime_train_data()
processed_df = transform_train_data(df)
save_data(processed_df)

print(processed_df.head())
print("ETL 완료")


# 반복 수집 : 실시간 데이터 누적 저장
# while True:
#     df = fetch_realtime_train_data()
#     processed_df = transform_train_data(df)
#     save_data(processed_df)
#     print("수집 완료")
#     time.sleep(5)