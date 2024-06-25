import requests


def get_trading_pairs(url):
    r = requests.get(f"{url}/trade-pairs")
    if not r.ok:
        return None
    response_data = r.json()
    return response_data["trade_pairs"]


def get_trading_pair(url, pair_id):
    r = requests.get(f"{url}/trade-pairs/{pair_id}")
    if not r.ok:
        return None
    response_data = r.json()
    return response_data


def get_orders(url, pair_id):
    r = requests.get(f"{url}/orders/{pair_id}")
    if not r.ok:
        return None
    response_data = r.json()
    return response_data
