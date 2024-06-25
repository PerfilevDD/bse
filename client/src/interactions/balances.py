import requests

import requests


def get_assets(url):
    r = requests.get(f"{url}/assets")
    if not r.ok:
        return None
    response_data = r.json()
    return response_data["assets"]
