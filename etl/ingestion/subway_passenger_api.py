# 호선/역별 승하차 인원 정보 : API 호출 (Extract)
import requests
import pandas as pd
from common.config import (
    PASSENGER_API_KEY,
    TARGET_LINE
    )
from common.logger import logger

TIMEOUT = 10
MAX_RETRIES = 3

def fetch_subway_data(date):
    url = (
        f"http://openapi.seoul.go.kr:8088/"
        f"{PASSENGER_API_KEY}/json/"
        f"CardSubwayStatsNew/1/100/{date}/{TARGET_LINE}"
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            data = response.json()

            # 응답 구조 검증
            if "CardSubwayStatsNew" not in data:
                raise ValueError(f"응답에 'CardSubwayStatsNew' 키 없음 : {data}")

            rows = data["CardSubwayStatsNew"].get("row")

            if not rows:
                raise ValueError("CardSubwayStatsNew.row 데이터 없음 (null 또는 빈 리스트)")

            df = pd.DataFrame(rows)

            logger.info(f"승하차 API 수집 성공 ({date}) : {len(df)} rows")

            return df

        except requests.exceptions.Timeout:
            logger.warning(f"승하차 API Timeout (시도 {attempt}/{MAX_RETRIES})")
        except requests.exceptions.ConnectionError:
            logger.warning(f"승하차 API 연결 오류 (시도 {attempt}/{MAX_RETRIES})")
        except requests.exceptions.HTTPError as e:
            logger.warning(f"승하차 API HTTP 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")
        except ValueError as e:
            logger.warning(f"승하차 API 응답 데이터 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")
        except Exception as e:
            logger.warning(f"승하차 API 알 수 없는 오류 : {e} (시도 {attempt}/{MAX_RETRIES})")

    raise RuntimeError(f"승하차 API {MAX_RETRIES}회 재시도 후 최종 실패")