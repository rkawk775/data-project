# 실시간 열차 위치 혼잡도 
# 같은 역 근처에 몇 대의 열차가 존재하는지 분석
# : headway_sec, 지연 분석, 배차 간격
import pandas as pd

def cacluate_train_density(df):
    
    # 시간 변환
    df["recptnDt"] = pd.to_datetime(df["recptnDt"])

    # 같은 시간대 + 같은 역 기준 열차 개수
    density = (
        df.groupby(
            [
                "statnNm",
                "updnLine",
                pd.Grouper(
                    key="recptnDt",
                    freq="1min"
                )
            ]
        )
        .size()
        .reset_index(name="TRAIN_COUNT")
    )

    # 밀집도 점수
    density["DENSITY_SCORE"] = ( density["TRAIN_COUNT"] / 5 )

    return density