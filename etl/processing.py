# processing.py : 데이터 정리/가공 (Transform)

import pandas as pd

def tranform_data(data):
    df = pd.DataFrame(data)

    df["price"] = df["price"].astype(int)

    return df