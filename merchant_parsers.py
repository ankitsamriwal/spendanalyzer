import re
from email.utils import parsedate_to_datetime
AED_REGEX = r"AED\s*([0-9]+(?:\.[0-9]{1,2})?)"

def _amount(html):
    m = re.search(r"(?:Grand\s*Total|Order\s*Total|Total).*?"+AED_REGEX, html, re.I | re.S)
    return float(m.group(1)) if m else None

def parse_talabat(html: str, received_at: str):
    return {"merchant":"Talabat","category":"FOOD","amount_aed":_amount(html),"ordered_at": received_at}

def parse_instashop(html: str, received_at: str):
    return {"merchant":"Instashop","category":"GROCERY","amount_aed":_amount(html),"ordered_at": received_at}

def parse_amazon(html: str, received_at: str):
    return {"merchant":"Amazon","category":"ONLINE","amount_aed":_amount(html),"ordered_at": received_at}

def parse_deliveroo(html: str, received_at: str):
    return {"merchant":"Deliveroo","category":"FOOD","amount_aed":_amount(html),"ordered_at": received_at}

def parse_noon(html: str, received_at: str):
    return {"merchant":"Noon","category":"ONLINE","amount_aed":_amount(html),"ordered_at": received_at}

def parse_carrefour(html: str, received_at: str):
    return {"merchant":"Carrefour","category":"GROCERY","amount_aed":_amount(html),"ordered_at": received_at}

def parse_kibsons(html: str, received_at: str):
    return {"merchant":"Kibsons","category":"GROCERY","amount_aed":_amount(html),"ordered_at": received_at}
