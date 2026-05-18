# transform.py : 컬럼 정리, 데이터 가공 (Transform)

def transform_train_data(df):

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
        ]
    ]

    return selected_df