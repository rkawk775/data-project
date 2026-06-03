# 지하철 혼잡도 정보
import requests
import pandas as pd
from etl.common.config import(
    CONGESTION_API_KEY,
    PASSENGER_DATE,
    TARGET_LINE
)

def fetch_congestion_data():
    
    url = (
        f"http://openapi.seoul.go.kr:8088/"
        f"{CONGESTION_API_KEY}/json/"
        f"subwConfusion/1/2000/{PASSENGER_DATE}/{TARGET_LINE}"
        )
    
    response = requests.get(url)
    data = response.json()

    rows = data['subwConfusion']['row']

    df = pd.DataFrame(rows)

    return df