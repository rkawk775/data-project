# 실시간 열차 위치 정보
import requests
import pandas as pd
from common.logger import logger
from common.config import(
    LOCATION_API_KEY, 
    BASE_URL, 
    TARGET_LINE
)

TIMEOUT = 10
MAX_RETRIES = 3

def fetch_realtime_train_data():
    url = f"{BASE_URL}/{LOCATION_API_KEY}/json/realtimePosition/0/5/{TARGET_LINE}"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            data = response.json()

            # 응답 구조 검증
            if "realtimePositionList" not in data:
                raise ValueError(f"응답에 'realtimePositionList' 키 없음 : {data}")

            realtime_data = data.get("realtimePositionList")

            if not realtime_data:
                raise ValueError("realtimePositionList 데이터 없음 (null 또는 빈 리스트)")

            df = pd.DataFrame(realtime_data)

            logger.info(f"실시간 열차 API 수집 성공 : {len(df)} rows")

            return df

        except requests.exceptions.Timeout:
            logger.warning(f"실시간 열차 API Timeout (시도 {attempt}/{MAX_RETRIES})")
        except requests.exceptions.ConnectionError:
            logger.warning(f"실시간 열차 API 연결 오류 (시도 {attempt}/{MAX_RETRIES})")
        except requests.exceptions.HTTPError as e:
            logger.warning(f"실시간 열차 API HTTP 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")
        except ValueError as e:
            logger.warning(f"실시간 열차 API 응답 데이터 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")
        except Exception as e:
            logger.warning(f"실시간 열차 API 알 수 없는 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")

    raise RuntimeError(f"실시간 열차 API {MAX_RETRIES}회 재시도 후 최종 실패")