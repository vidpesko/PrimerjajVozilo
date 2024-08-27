# Parsers for all data field on vehicle page

def name_parser(val) -> str | None:
    if not val:
        return None
    return str(val).replace('\xa0', ' ')

def price_parser(val) -> int:
    val = str(val).replace("\n", "").replace("€", "").replace(".", "").strip()
    return int(val)
