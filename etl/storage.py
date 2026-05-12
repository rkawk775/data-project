# storage.py : DB 저장 (Load)

from sqlalchemy import create_engine

def save_data(df):

    engine = create_engine(
        "postgresql://admin:admin123@localhost:5432/realestate"
    )

    df.to_sql(
        name="apartment_price",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("PostgreSQL 저장 완료")