# 지하철 혼잡도 정보
import requests
import pandas as pd
from common.config import(CONGESTION_API_KEY)
from common.logger import logger

TIMEOUT = 10
MAX_RETRIES = 3

def fetch_congestion_data():
    
    url = (
        f"http://openapi.seoul.go.kr:8088/"
        f"{CONGESTION_API_KEY}/json/"
        f"subwConfusion/1/500"
        )
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            data = response.json()

            # 응답 구조 검증
            if "subwConfusion" not in data:
                raise ValueError(f"응답에 'subwConfusion' 키 없음 : {data}")

            rows = data["subwConfusion"].get("row")

            if not rows:
                raise ValueError("subwConfusion.row 데이터 없음 (null 또는 빈 리스트)")

            df = pd.DataFrame(rows)

            logger.info(f"혼잡도 API 수집 성공 : {len(df)} rows")

            return df
        
        except requests.exceptions.Timeout:
            logger.warning(f"혼잡도 API Timeout (시도 {attempt}/{MAX_RETRIES})")
        except requests.exceptions.ConnectionError:
            logger.warning(f"혼잡도 API 연결 오류 (시도 {attempt}/{MAX_RETRIES})")
        except requests.exceptions.HTTPError as e:
            logger.warning(f"혼잡도 API HTTP 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")
        except ValueError as e:
            logger.warning(f"혼잡도 API 응답 데이터 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")
        except Exception as e:
            logger.warning(f"혼잡도 API 알 수 없는 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")

    raise RuntimeError(f"혼잡도 API {MAX_RETRIES}회 재시도 후 최종 실패")