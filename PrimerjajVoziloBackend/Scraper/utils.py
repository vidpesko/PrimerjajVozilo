import re
from urllib.parse import urlparse, parse_qs


def extract_url_param(url: str, param_key: str):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return params.get(param_key, [None])[0]


def get_id(url: str) -> int | None:
    return extract_url_param(url, "id")


def remove_repeated_spaces(val: str) -> str:
    return re.sub(r"[ ]+", " ", val).strip()
