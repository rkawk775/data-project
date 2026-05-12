from etl.ingestion import fetch_data
from etl.processing import tranform_data
from etl.storage import save_data

data = fetch_data()

df = tranform_data(data)

save_data(df)