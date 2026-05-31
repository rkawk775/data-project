# 호선/역별 승하차 인원 정보 : API 호출 (Extract)
import requests
import pandas as pd
from etl.common.config import PASSENGER_API_KEY


def fetch_subway_data(date: str):
    url = (
        f"http://openapi.seoul.go.kr:8088/"
        f"{PASSENGER_API_KEY}/json/"
        f"CardSubwayStatsNew/1/100/{date}/"
    )

    response = requests.get(url)
    data = response.json()

    rows = data['CardSubwayStatsNew']['row']

    df = pd.DataFrame(rows)

    return df