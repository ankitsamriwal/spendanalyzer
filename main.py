from fastapi import FastAPI
from pydantic import BaseModel
from shared.db import exec_query
from shared.notify import send_whatsapp, send_email
from datetime import datetime, timezone

app = FastAPI(title="Spend Tracker API")

class BudgetIn(BaseModel):
    month: str   # '2025-08-01'
    category: str
    limit_aed: float

@app.post("/budget/set")
def set_budget(b: BudgetIn):
    sql = """
    insert into budget(user_id, month, category, limit_aed)
    values (
      (select id from app_user order by created_at limit 1),
      %s, %s, %s
    )
    on conflict (user_id, month, category) do update set limit_aed = excluded.limit_aed
    """
    exec_query(sql, (b.month, b.category, b.limit_aed))
    return {"ok": True}

@app.get("/summary/daily")
def daily_summary():
    uid = exec_query("select id from app_user order by created_at limit 1", fetch=True)[0][0]
    today_sql = """
    select category, sum(amount_aed) as spent
    from txn
    where user_id = %s and ordered_at::date = current_date
    group by category
    """
    mtd_sql = """
    select category, sum(amount_aed) as spent
    from txn
    where user_id = %s and ordered_at >= date_trunc('month', now())
    group by category
    """
    today = exec_query(today_sql, (uid,), fetch=True) or []
    mtd = exec_query(mtd_sql, (uid,), fetch=True) or []
    return {"today": today, "mtd": mtd}

@app.post("/notify/test")
def notify_test(kind: str = "WHATSAPP"):
    if kind.upper() == "WHATSAPP":
        r = send_whatsapp("Test message from Spend Tracker ✅")
    else:
        r = send_email("Test Spend Tracker", "<b>Hello from Spend Tracker</b>")
    return r
