# main.py : 전체 ETL orchestration
import time
from etl.common.config import COLLECT_INTERVAL
from etl.common.logger import logger
from etl.ingestion.subway_api import fetch_realtime_train_data
from etl.processing.transform import transform_train_data
from etl.processing.headway import calculate_headway
from etl.storage.postgres import (
    save_data,
    save_headway_data
)



# 실제 ETL 파이프라인 구축
df = fetch_realtime_train_data()
logger.info("실시간 데이터 수집 완료")

processed_df = transform_train_data(df)
logger.info("데이터 가공 완료")

save_data(processed_df)
logger.info("원본 데이터 저장 완료")

headway_df = calculate_headway(processed_df)
logger.info("Headway 계산 완료")

save_headway_data(headway_df)
logger.info("Headway 데이터 저장 완료")



# 반복 수집 : 실시간 데이터 누적 저장
while True:
    df = fetch_realtime_train_data()
    processed_df = transform_train_data(df)
    save_data(processed_df)
    logger.info("ETL완료")
    time.sleep(COLLECT_INTERVAL)