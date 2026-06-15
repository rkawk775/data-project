# 호선/역별 승하차 인원 : 데이터 타입 정리 담당
from common.config import TARGET_LINE

def transform_subway_data(df):

    df = df[
        df["SBWY_ROUT_LN_NM"] == TARGET_LINE
    ].copy()


    # 데이터 품질 관리 
    df["SBWY_STNS_NM"] = (
        df["SBWY_STNS_NM"].replace({
            "청량리(서울시립대입구)": "청량리"
        })
    )

    
    # 숫자형 변환
    df['GTON_TNOPE'] = df['GTON_TNOPE'].astype(int)
    df['GTOFF_TNOPE'] = df['GTOFF_TNOPE'].astype(int)

    df["TOTAL_PASSENGERS"] = (
        df["GTON_TNOPE"] + 
        df["GTOFF_TNOPE"]
    )

    return df