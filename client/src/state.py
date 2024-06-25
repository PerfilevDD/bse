class WindowState:
    url = "http://localhost:8000"
    token = ''
    user_id = 0;
    user_email = ''
    balancePOEUR = 0
    currency = ""
    currency_balance = 0

    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    current_orders = set()


state = WindowState()
