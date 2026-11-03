import pandas as pd
from sqlalchemy import text
from db import get_engine

# 1. create database and table
with get_engine(with_db=False).begin() as conn:
    for stmt in open("sql/schema.sql", encoding="utf-8").read().split(";"):
        if stmt.strip():
            conn.execute(text(stmt))

# 2. insert cleaned data
df = pd.read_csv("data/cleaned_earthquakes.csv", parse_dates=["time", "updated"])
print("CSV shape:", df.shape)
df.to_sql("earthquakes", get_engine(), if_exists="append", index=False,
          chunksize=1000, method="multi")

# 3. verify
with get_engine().connect() as conn:
    n = conn.execute(text("SELECT COUNT(*) FROM earthquakes")).scalar()
print("Rows in MySQL:", n, "| Rows in CSV:", len(df))