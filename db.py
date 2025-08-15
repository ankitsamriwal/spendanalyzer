import os
import psycopg2
from contextlib import contextmanager

PG_URL = os.getenv("PG_URL")

@contextmanager
def get_conn():
    if not PG_URL:
        raise RuntimeError("PG_URL not set")
    conn = psycopg2.connect(PG_URL)
    try:
        yield conn
    finally:
        conn.close()

def exec_query(sql, params=None, fetch=False):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            rows = cur.fetchall() if fetch else None
            conn.commit()
            return rows
