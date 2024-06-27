import asyncio
import json
import random
import threading
import time

import requests
import websockets

bot_email = "bot1@bse.com"
bot_password = "Bananeneisistlecker"
url = "http://localhost:8000"
pair_id = 1


class Bot:
    websocket: websockets
    def __init__(self, bot_email, bot_password, pair_id, url):
        self.pair_id = pair_id
        self.url = url
        self.open = True

        # Try to register
        register_payload = {
            "email": bot_email,
            "password": bot_password
        }

        r = requests.post(url + "/register", json=register_payload)

        login_payload = {'grant_type': "password", 'username': bot_email, 'password': bot_password}
        token_response = requests.post(url + "/token", data=login_payload).json()

        self.token = token_response['access_token']
        self.auth_header = {"Authorization": "Bearer " + self.token}

        me = requests.get(url + "/me", headers=self.auth_header).json()
        self.user_id = me['user_id']

        print("Loading Trading pair")
        self.trading_pair = requests.get(url + "/trade-pairs/" + str(pair_id)).json()

        print("Loading balances")
        self.balance_base_asset = \
            requests.get(url + "/balance/" + str(self.trading_pair['base_asset']), headers=self.auth_header).json()[
                "balance"]
        self.balance_price_asset = \
            requests.get(url + "/balance/" + str(self.trading_pair['price_asset']), headers=self.auth_header).json()[
                "balance"]

        if self.balance_base_asset < 1000000:
            params = {"change": 1000000 - self.balance_base_asset, "asset_id": self.trading_pair["base_asset"]}
            requests.post(url + "/balance/update", headers=self.auth_header, params=params).json()

        if self.balance_price_asset < 1000000:
            params = {"change": 1000000 - self.balance_price_asset, "asset_id": self.trading_pair["price_asset"]}
            requests.post(url + "/balance/update", headers=self.auth_header, params=params).json()

        print("Loading Order book")
        self.orders = requests.get(url + "/orders/" + str(pair_id)).json()

        threading.Thread(target=asyncio.run, args=(self.websocket_updater(),)).start()

    async def websocket_updater(self):
        ws_url = self.url.replace('http', 'ws').replace('htpps', 'wss') + '/ws'
        self.websocket = await websockets.connect(ws_url)

        await self.websocket.send(json.dumps(
            {"type": "register", "user_id": self.user_id, "pair_id": self.pair_id}
        ))

        while self.open:
            try:
                message = await self.websocket.recv()

                if not self.open:
                    break

                data = json.loads(message)
                if "type" in data and data["type"] == "orderbook":
                    self.orders = data["data"]

                if "type" in data and data["type"] == "balances":
                    for balance in data["data"]:
                        if balance["asset_id"] == self.trading_pair['base_asset']:
                            self.balance_base_asset = balance["balance"]
                        elif balance["asset_id"] == self.trading_pair['price_asset']:
                            self.balance_price_asset = balance["balance"]

                if "type" in data and data["type"] == "ping":
                    await self.websocket.send(json.dumps({"type": "pong"}))

            except:
                pass

        await self.websocket.send(json.dumps(
            {"type": "leave", "user_id": self.state.user_id, "pair_id": self.pair_id}
        ))

        await self.websocket.close()

    def perform_trade(self):
        buy = random.choice([True, False])
        fullfill_order = random.choice([True, False])
        random_price = random.choice([True, False])

        print(f"Bot is {'buying' if buy else 'selling'} while {'fullfilling a' if fullfill_order else 'creating a new'} order")
        # Find order to fullfill
        orderbook = self.orders["sell" if buy else "buy"]

        if not orderbook:
            price = random.randint(1, 200)
            amount = 1
        elif fullfill_order:
            price = orderbook[0]['price']
            amount = 1
        elif not fullfill_order:
            price = random.randint(1, 200) if random_price else \
                (orderbook[0]['price'] + 1 if buy else orderbook[0]['price'] - 1)
            amount = 1

        our_order = {
            'trade_pair_id': self.pair_id,
            'amount': amount,
            'price': price,
            'buy': buy
        }

        r = requests.post(self.url + "/trade/create", json=our_order, headers=self.auth_header)
        print(r.json())


if __name__ == "__main__":
    bot = Bot(bot_email, bot_password, pair_id, url)
    while True:
        try:
            time.sleep(1)
            bot.perform_trade()
        except KeyboardInterrupt:
            exit()
        except:
            pass