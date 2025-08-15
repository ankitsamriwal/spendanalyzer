import re

MERCHANT_MAP = {
    "talabat.com": ("Talabat", "FOOD"),
    "deliveroo.ae": ("Deliveroo", "FOOD"),
    "zomato.com": ("Zomato", "FOOD"),
    "instashop.ae": ("Instashop", "GROCERY"),
    "carrefouruae.com": ("Carrefour", "GROCERY"),
    "kibsons.com": ("Kibsons", "GROCERY"),
    "noon.com": ("Noon", "ONLINE"),
    "amazon.ae": ("Amazon", "ONLINE"),
    "careem.com": ("Careem", "FOOD"),
}

KEYWORD_MAP = [
    (re.compile(r"talabat", re.I), ("Talabat", "FOOD")),
    (re.compile(r"deliveroo", re.I), ("Deliveroo", "FOOD")),
    (re.compile(r"insta(shop|mart)", re.I), ("Instashop", "GROCERY")),
    (re.compile(r"carrefour", re.I), ("Carrefour", "GROCERY")),
    (re.compile(r"kibsons", re.I), ("Kibsons", "GROCERY")),
    (re.compile(r"noon", re.I), ("Noon", "ONLINE")),
    (re.compile(r"amazon", re.I), ("Amazon", "ONLINE")),
    (re.compile(r"careem", re.I), ("Careem", "FOOD")),
]

def classify(from_addr: str, subject: str, html: str):
    from_addr = (from_addr or "").lower()
    subject = subject or ""
    for k,(name,cat) in MERCHANT_MAP.items():
        if k in from_addr:
            return name, cat
    for rx,(name,cat) in KEYWORD_MAP:
        if rx.search(from_addr) or rx.search(subject):
            return name, cat
    return "Unknown", "OTHER"
