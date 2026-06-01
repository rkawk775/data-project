# 호선/역별 승하차 인원 : 데이터 타입 정리 담당
from etl.common.config import TARGET_LINE

def transform_subway_data(df):

    df = df[
        df["SBWY_ROUT_LN_NM"] == TARGET_LINE
    ].copy()

    # 숫자형 변환
    df['GTON_TNOPE'] = df['GTON_TNOPE'].astype(int)
    df['GTOFF_TNOPE'] = df['GTOFF_TNOPE'].astype(int)

    df["TOTAL_PASSENGERS"] = (
        df["GTON_TNOPE"] + 
        df["GTOFF_TNOPE"]
    )

    return df