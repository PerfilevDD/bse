
import requests
from datetime import datetime


def get_graph_data(url):
    r = requests.get(f"{url}/orders/all")
    if not r.ok:
        return None
    response_data = r.json()
    orders = response_data.get("order", [])

    time_data = []
    price_data = []

    for order in orders:
        timestamp = int(order["completed_timestamp"]) // 1000
        time_data.append(datetime.fromtimestamp(timestamp))
        price_data.append(order["price"])

    return time_data, price_data