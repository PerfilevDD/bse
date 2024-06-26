import requests


def server_auth_user(url, email, password):
    try:
        data = {'grant_type': "password", 'username': email, 'password': password}
        r = requests.post(f"{url}/token", data=data)
        r.raise_for_status()
        response_data = r.json()
        token = response_data['access_token']
        return token, response_data
    except requests.exceptions.RequestException as e:
        try:
            return "", r.json()['detail']
        except:
            return None, None
