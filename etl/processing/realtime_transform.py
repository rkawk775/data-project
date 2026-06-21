# 실시간 열차 위치
import pandas as pd

def transform_train_data(df):
    
    # 방향명 컬럼 추가
    df["direction"] = df["updnLine"].map({ 0:"상행", 1:"하행" })

    selected_df = df[
        [
            "trainNo",      #열차번호
            "subwayId",     #노선ID
            "subwayNm",     #노선명
            "statnId",      #역ID
            "statnNm",      #현재 역 이름
            "updnLine",     #상행/하행 방향
            "trainSttus",   #열차 상태
            "recptnDt",     #현재 데이터 수집 시각
            "lastRecptnDt", #이전 수신 시각
            "directAt",     #급행 여부
            "direction",    #방향명 (상행/하행)
        ]
    ]

    return selected_df