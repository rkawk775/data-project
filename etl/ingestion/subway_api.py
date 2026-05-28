# subway_api.py : API 호출 (Extract)
import requests
import pandas as pd
from etl.common.config import(
    LOCATION_API_KEY, 
    BASE_URL, 
    TARGET_LINE,
    PASSENGER_API_KEY
)



def fetch_realtime_train_data():
    
    url = f"{BASE_URL}/{LOCATION_API_KEY}/json/realtimePosition/0/5/{TARGET_LINE}"
    response = requests.get(url)
    data = response.json()
    realtime_data = data["realtimePositionList"]
    df = pd.DataFrame(realtime_data)
    
    return df

def fetch_subway_data(date: str):
    url = (
        f"http://openapi.seoul.go.kr:8088/"
        f"{PASSENGER_API_KEY}/json/"
        f"CardSubwayStatsNew/1/100/{date}/"
    )

    response = requests.get(url)

    data = response.json()

    return data