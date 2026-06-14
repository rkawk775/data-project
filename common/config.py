import os

# Docker 환경에서는 env_file로 주입되므로 load_dotenv 불필요
# 로컬 개발 시에만 load_dotenv 사용
try:
    from dotenv import load_dotenv
    load_dotenv()  # 로컬에서는 동작, 컨테이너에선 무시됨
except ImportError:
    pass

# 서울 열림데이터 광장 API
# 지하철 실시간 열차 위치 정보 API
LOCATION_API_KEY = os.getenv("LOCATION_API_KEY")
BASE_URL ="http://swopenapi.seoul.go.kr/api/subway"

# 지하철 호선별 역별 승하차 인원 정보 (최근3개월)
PASSENGER_API_KEY = os.getenv("PASSENGER_API_KEY")

# 지하철 혼잡도 정보
CONGESTION_API_KEY =os.getenv("CONGESTION_API_KEY")

# 노선 설정
TARGET_LINE = "1호선"
# [승하차] 수집 날짜 설정
PASSENGER_DATE = "20260508"

# PostgreSQL 설정
POSTGRES_CONFIG = {
    "user":os.getenv("POSTGRES_USER"),
    "password":os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "database": os.getenv("POSTGRES_DB")
}

# 수집 설정
COLLECT_INTERVAL = 5

# 저장 테이블 이름
REALTIME_TABLE_NAME = "realtime_train_location" 
HEADWAY_TABLE_NAME = "train_headway"
PASSENGER_TABLE_NAME = "subway_passenger"
CONGESTION_TABLE_NAME = "subway_congestion"
BOTTLENECK_TABLE_NAME = "subway_bottleneck"
