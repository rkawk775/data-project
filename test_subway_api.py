import requests
import pandas as pd

#USE_YMD
#SBWY_ROUT_LN_NM
#SBWY_STNS_NM
#GTON_TNOPE
#GTOFF_TNOPE
#REG_YMD

API_KEY = "74426c50726462733739414e654541"

url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/json/CardSubwayStatsNew/1/100/20260507"

response = requests.get(url)

data = response.json()

rows = data['CardSubwayStatsNew']['row']

for col in rows[0].keys():
    print(col)