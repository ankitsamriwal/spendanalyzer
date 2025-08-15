import os, psycopg2, pandas as pd
from contextlib import contextmanager

PG_URL = os.getenv("PG_URL")

@contextmanager
def get_conn():
    if not PG_URL: raise RuntimeError("PG_URL not set")
    conn = psycopg2.connect(PG_URL)
    try:
        yield conn
    finally:
        conn.close()

def df_read(sql, params=None):
    with get_conn() as conn:
        return pd.read_sql(sql, conn, params=params)

def exec_sql(sql, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ()); conn.commit()

def categories(): return ['GROCERY','FOOD','ONLINE','OTHER']
