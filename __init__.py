import json
from shared.db import exec_query
from shared.classifier import classify
from . import merchant_parsers as mp

def main(msg: str):
    data = json.loads(msg)
    user_email = data.get("user_email")
    from_addr = data.get("from","")
    subject = data.get("subject","")
    received_at = data.get("received_at")
    html = data.get("html","")

    # Ensure user exists
    exec_query("""
    insert into app_user(email) values (%s)
    on conflict (email) do update set email=excluded.email
    """, (user_email,))

    uid = exec_query("select id from app_user where email=%s", (user_email,), fetch=True)[0][0]

    # raw event
    payload = json.dumps(data)
    exec_query("""
    insert into raw_event(user_id, source, payload, received_at)
    values (%s, %s, %s::jsonb, %s)
    """, (uid, data.get("source","EMAIL"), payload, received_at))

    # classify + merchant specific parsing
    merchant_name, category = classify(from_addr, subject, html)
    parsed = None
    low = (from_addr + " " + subject).lower()
    if "talabat" in low: parsed = mp.parse_talabat(html, received_at)
    elif "insta" in low: parsed = mp.parse_instashop(html, received_at)
    elif "amazon" in low: parsed = mp.parse_amazon(html, received_at)
    elif "deliveroo" in low: parsed = mp.parse_deliveroo(html, received_at)
    elif "noon" in low: parsed = mp.parse_noon(html, received_at)
    elif "carrefour" in low: parsed = mp.parse_carrefour(html, received_at)
    elif "kibsons" in low: parsed = mp.parse_kibsons(html, received_at)

    amount = 0.0
    ordered_at = received_at
    if parsed:
        merchant_name = parsed['merchant']
        category = parsed['category']
        amount = parsed.get('amount_aed') or 0.0
        ordered_at = parsed.get('ordered_at') or received_at

    # upsert merchant
    exec_query("""
    insert into merchant(name, normalized, category)
    values (%s, %s, %s)
    on conflict (normalized) do update set category=excluded.category
    """, (merchant_name, merchant_name.upper(), category))

    mid = exec_query("select id from merchant where normalized=%s", (merchant_name.upper(),), fetch=True)[0][0]

    # txn
    exec_query("""
    insert into txn(user_id, event_id, merchant_id, merchant_text, category, amount_aed, ordered_at)
    values (
      %s,
      (select id from raw_event where user_id=%s order by received_at desc limit 1),
      %s, %s, %s, %s, %s
    )
    """, (uid, uid, mid, merchant_name, category, amount, ordered_at))
