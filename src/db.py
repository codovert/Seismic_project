import os
import pandas as pd
from functools import lru_cache
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

DB = dict(user="root", password=os.getenv("DB_PASSWORD"), host="localhost", port=3306, name="seismic")

@lru_cache
def get_engine(with_db=True):
    db = f"/{DB['name']}" if with_db else ""
    return create_engine(f"mysql+pymysql://{DB['user']}:{quote_plus(DB['password'])}@{DB['host']}:{DB['port']}{db}")

def run_query(sql, params=None):
    with get_engine().connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)