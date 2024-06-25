import requests


def get_assets(url):
    r = requests.get(f"{url}/assets")
    if not r.ok:
        return None
    response_data = r.json()
    return {a["asset_id"]: {
        "name": a["name"],
        "ticker": a["ticker"],
    } for a in response_data["assets"]}
