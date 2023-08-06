import json
import hmac
import hashlib
from time import time
from typing import Optional, Dict, Literal

Method = Literal['GET', 'POST', 'DELETE', 'PUT']


def create_300k_signature(ts: int, method: Method, path: str, api_secret: str, post_data: Optional[Dict] = None) -> str:
    if post_data is not None and method != 'GET' and len(post_data.keys()) > 0:
        encode_body = json.dumps(post_data, separators=(',', ':'))
    else:
        encode_body = ''
    signature = hmac.new(api_secret.encode(), f"{ts}{method.upper()}{path}{encode_body}".encode(),
                         hashlib.sha256).hexdigest()

    return signature


def create_300k_header(method: Method, path: str, api_key: str, api_secret: str, post_data: Optional[Dict] = None,
                       ts: Optional[int] = None):
    ts_final = round(time() * 1000) if ts is None else ts
    return {
        'X-APIKEY': api_key,
        'X-TS': str(ts_final),
        'X-SIGNATURE': create_300k_signature(ts_final, method, path, api_secret, post_data)
    }
