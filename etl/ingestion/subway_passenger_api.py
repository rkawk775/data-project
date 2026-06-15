# 호선/역별 승하차 인원 정보 : API 호출 (Extract)
import requests
import pandas as pd
from common.config import (
    PASSENGER_API_KEY,
    PASSENGER_DATE,
    TARGET_LINE
    )


def fetch_subway_data():
    url = (
        f"http://openapi.seoul.go.kr:8088/"
        f"{PASSENGER_API_KEY}/json/"
        f"CardSubwayStatsNew/1/100/{PASSENGER_DATE}/{TARGET_LINE}"
    )

    response = requests.get(url)
    data = response.json()

    rows = data['CardSubwayStatsNew']['row']

    df = pd.DataFrame(rows)

    return df