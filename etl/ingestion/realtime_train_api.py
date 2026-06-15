# 실시간 열차 위치 정보
import requests
import pandas as pd
from common.config import(
    LOCATION_API_KEY, 
    BASE_URL, 
    TARGET_LINE
)


def fetch_realtime_train_data():
    
    url = f"{BASE_URL}/{LOCATION_API_KEY}/json/realtimePosition/0/5/{TARGET_LINE}"
    response = requests.get(url)
    data = response.json()
    realtime_data = data["realtimePositionList"]
    df = pd.DataFrame(realtime_data)

    return df