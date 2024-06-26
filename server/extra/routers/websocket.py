import json

from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
import uuid

from BSE import User as BSEUser, Database, TradePair, Order

class WebsocketManager:
    def __init__(self):
        self.connected_sockets = {}
        self.clients_for_pair_id = {}
        self.db = Database()

    def add_client(self, client: WebSocket):
        session_id = str(uuid.uuid4())
        self.connected_sockets[session_id] = client
        return session_id

    def remove_client(self, session_id):
        self.connected_sockets.pop(session_id, None)
        to_remove = []
        for pair_id, sessions in self.clients_for_pair_id.items():
            for session in sessions:
                if session[0] == session_id:
                    to_remove.append((pair_id, session_id, session[1]))

        for remove in to_remove:
            self.clients_for_pair_id[remove[0]].remove((remove[1], remove[2]))


    def register_client_for_pair_id(self, session_id, user_id, pair_id):
        if pair_id not in self.clients_for_pair_id:
            self.clients_for_pair_id[pair_id] = []

        if (session_id, user_id) not in self.clients_for_pair_id[pair_id]:
            self.clients_for_pair_id[pair_id].append((session_id, user_id))

    def remove_client_for_pair_id(self, session_id, user_id, pair_id):
        if pair_id not in self.clients_for_pair_id:
            self.clients_for_pair_id[pair_id] = []

        try:
            self.clients_for_pair_id[pair_id].remove(session_id, user_id)
        except:
            pass

    async def _send_message_to_session(self, session_id, message_dict):
        try:
            await self.connected_sockets[session_id].send_json(message_dict)
        except:
            pass
    async def send_confirmation(self, session_id):
        await self._send_message_to_session(session_id=session_id, message_dict={"type": "confirmation"})

    async def process_balance_updates(self, pair_id):
        if pair_id not in self.clients_for_pair_id:
            return

        for session_id, user_id in self.clients_for_pair_id[pair_id]:
            user = BSEUser(self.db, user_id)
            user_balance = user.get_balances()

            message_dict =  { "type": "balances", "data": [{
                    "balance": asset.balance,
                    "name": asset.name,
                    "ticker": asset.ticker,
                } for asset in user_balance]}
            await self._send_message_to_session(session_id, message_dict)

    async def process_orderbooks_update(self, pair_id):
        if pair_id not in self.clients_for_pair_id:
            return
        for session_id, user_id in self.clients_for_pair_id[pair_id]:
            trade_pair = TradePair(self.db, pair_id)
            open_orders = trade_pair.get_open_orders(pair_id)
            buy_orders = [{
                'price': order.get_price(),
                'amount': order.get_amount(),
                'fullfilled_amount': order.get_fullfilled_amount()
            } for order in open_orders if order.is_buy()]
            sell_orders = [{
                'price': order.get_price(),
                'amount': order.get_amount(),
                'fullfilled_amount': order.get_fullfilled_amount()
            } for order in open_orders if not order.is_buy()]
            buy_orders.reverse()

            data = {
                "buy": buy_orders,
                "sell": sell_orders
            }
            message_dict = { "type": "orderbook", "data": data}
            await self._send_message_to_session(session_id, message_dict)


websocket_clients_manager = WebsocketManager()

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = websocket_clients_manager.add_client(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            if data["action"] == "register":
                user_id = data["user_id"]
                trade_id = data["pair_id"]
                websocket_clients_manager.register_client_for_pair_id(session_id, user_id, trade_id)
                await websocket_clients_manager.send_confirmation(session_id)

            if data["action"] == "leave":
                user_id = data["user_id"]
                trade_id = data["pair_id"]
                websocket_clients_manager.remove_client_for_pair_id(session_id, user_id, trade_id)
                await websocket_clients_manager.send_confirmation(session_id)

    except Exception as e:
        websocket_clients_manager.remove_client(session_id)
