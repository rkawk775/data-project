# logger.py : 수집 상태 기록 
import logging

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger()
