# 호선/역별 승하차 인원 : 데이터 타입 정리 담당

def transform_subway_data(df):

    # 숫자형 변환
    df['GTON_TNOPE'] = df['GTON_TNOPE'].astype(int)
    df['GTOFF_TNOPE'] = df['GTOFF_TNOPE'].astype(int)

    return df