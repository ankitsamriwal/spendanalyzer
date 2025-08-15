import os, json, requests
from datetime import datetime

TZ = os.getenv("TZ", "Asia/Dubai")

# WhatsApp via Meta Cloud API
WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_FROM = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_TO = os.getenv("WHATSAPP_TO_E164")  # e.g., +9715XXXXXXX

# Email via SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM = os.getenv("SENDGRID_FROM")
SENDGRID_TO = os.getenv("SENDGRID_TO")

def send_email(subject: str, html: str, to_addr: str = None):
    if not (SENDGRID_API_KEY and SENDGRID_FROM):
        return {"ok": False, "err": "SendGrid not configured"}
    to = to_addr or SENDGRID_TO
    if not to:
        return {"ok": False, "err": "No recipient configured"}
    url = "https://api.sendgrid.com/v3/mail/send"
    data = {
      "personalizations": [{"to": [{"email": to}]}],
      "from": {"email": SENDGRID_FROM},
      "subject": subject,
      "content": [{"type": "text/html", "value": html}]
    }
    r = requests.post(url, headers={"Authorization": f"Bearer {SENDGRID_API_KEY}", "Content-Type":"application/json"}, data=json.dumps(data), timeout=30)
    return {"ok": r.ok, "status": r.status_code, "resp": r.text}

# Twilio fallback (if Meta Cloud not configured)
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")  # e.g., 'whatsapp:+14155238886'

def send_whatsapp_twilio(text: str):
    if not (TWILIO_SID and TWILIO_TOKEN and TWILIO_WHATSAPP_FROM and WHATSAPP_TO):
        return {"ok": False, "err": "Twilio not configured"}
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    data = {"From": TWILIO_WHATSAPP_FROM, "To": f"whatsapp:{WHATSAPP_TO}", "Body": text}
    r = requests.post(url, data=data, auth=(TWILIO_SID, TWILIO_TOKEN), timeout=30)
    return {"ok": r.ok, "status": r.status_code, "resp": r.text}

def send_whatsapp(text: str):
    if WHATSAPP_TOKEN and WHATSAPP_FROM and WHATSAPP_TO:
        url = f"https://graph.facebook.com/v20.0/{WHATSAPP_FROM}/messages"
        payload = {"messaging_product":"whatsapp","to":WHATSAPP_TO,"type":"text","text":{"body":text}}
        r = requests.post(url, headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type":"application/json"}, data=json.dumps(payload), timeout=30)
        return {"ok": r.ok, "status": r.status_code, "resp": r.text}
    return send_whatsapp_twilio(text)

def format_daily_summary(dt: datetime, today_rows, mtd_rows):
    t = {r[0]: float(r[1]) for r in (today_rows or [])}
    m = {r[0]: float(r[1]) for r in (mtd_rows or [])}
    lines = [f"📊 Daily Spend – {dt.strftime('%d %b %Y')}"]
    for cat in ["GROCERY","FOOD","ONLINE","OTHER"]:
        lines.append(f"{cat.title()}: AED {t.get(cat,0):.2f} (MTD {m.get(cat,0):.2f})")
    lines.append(f"TOTAL today: AED {sum(t.values()):.2f} | MTD: AED {sum(m.values()):.2f}")
    return "\n".join(lines)
