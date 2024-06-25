import requests


def get_trading_pairs(url):
    r = requests.get(f"{url}/trade-pairs")
    if not r.ok:
        return None
    response_data = r.json()
    return response_data["trade_pairs"]
