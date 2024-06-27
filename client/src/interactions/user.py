import requests


def get_balances(url, jwt_token):
    headers = {"Authorization": "Bearer " + jwt_token}
    r = requests.get(f"{url}/balance", headers=headers)
    if not r.ok:
        print(r.text)
        return None
    response_data = r.json()

    return {
        balance['ticker']: balance
        for balance in response_data["balances"]
    }


def get_me(url, jwt_token):
    headers = {"Authorization": "Bearer " + jwt_token}
    r = requests.get(f"{url}/me", headers=headers)
    if not r.ok:
        print(r.text)
        return None
    response_data = r.json()

    return response_data
