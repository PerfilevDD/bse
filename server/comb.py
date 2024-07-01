# server.py

from datetime import datetime, timedelta, timezone
from typing import Annotated

from contextlib import asynccontextmanager

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

import argparse, uvicorn
from starlette.responses import RedirectResponse
import json
import asyncio

from dependencies import get_database_object
from models.models import OrderToAccept, Order
from routers.users import router as user_router
from routers.orders import router as orders_router
from routers.trade_pairs import router as trade_pairs_router
from routers.assets import router as assets_router
from routers.websocket import router as websocket_router

from BSE import Asset, TradePair, User as BSEUser, Database, Order as BSEOrder, OrderDB  # type: ignore

db = Database()

clients = []

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
'''
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(get_orders())
    yield
    '''

app = FastAPI(
    title="Bonn Stock Exchange",

)

app.include_router(router=user_router)
app.include_router(router=orders_router)
app.include_router(router=assets_router)
app.include_router(router=trade_pairs_router)
app.include_router(router=websocket_router)


# CONFIG -------------------------
@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8000, help="The port on which the api will be accessible.")
    parser.add_argument('-ho', '--host', default="localhost", help="The host on which the api will be accessible.")
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)


# models.py

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    user_id: int

class User(BaseModel):
    email: str 
    password: str

class Order(BaseModel):
    trader_id: int
    item: str
    pair_item: str
    price: int
    item_amount: int

class OrderToAccept(BaseModel):
    email: str
    order_id: int
    trader_id: int
    item: str
    price: int
    item_amount: int

class Trade(BaseModel):
    trade_pair_id: int 
    amount: int
    price: int
    buy: bool


# websocket.py

import asyncio
import json
import threading

from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
import uuid

from BSE import User as BSEUser, Database, TradePair, Order


class WebsocketManager:
    def __init__(self):
        self.open = True

        self.connected_sockets = {}
        self.clients_for_pair_id = {}
        self.db = Database()
        self.pinged_sessions = []

        self.ping_thread = threading.Thread(target=asyncio.run, args=(self.ping_loop(), ), daemon=True)
        self.ping_thread.start()

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
        if (pair_id not in self.clients_for_pair_id):
            return

        for session_id, user_id in self.clients_for_pair_id[pair_id]:
            user = BSEUser(self.db, user_id)
            user_balance = user.get_balances()

            message_dict = {"type": "balances", "data": [{
                "balance": asset.balance,
                "name": asset.name,
                "ticker": asset.ticker,
            } for asset in user_balance]}
            await self._send_message_to_session(session_id, message_dict)
            
    
    async def process_graphic_updates(self, pair_id):
        if (pair_id not in self.clients_for_pair_id):
            return

        for session_id, _ in self.clients_for_pair_id[pair_id]:
            
            all_orders = Order.get_all_completed_orders(self.db)

            message_dict = {"type": "order_history", "data": [{
                "price": order.get_price(),
                "time": order.get_completed_timestamp(),
            } for order in all_orders]}
            await self._send_message_to_session(session_id, message_dict)

    async def process_orderbooks_update(self, pair_id):
        if (pair_id not in self.clients_for_pair_id):
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
            message_dict = {"type": "orderbook", "data": data}
            await self._send_message_to_session(session_id, message_dict)

    async def ping_loop(self):
        while (True):
            for session_id in self.connected_sockets.keys():
                await self._send_message_to_session(session_id, {"type": "ping"})
                self.pinged_sessions.append(session_id)

            await asyncio.sleep(2)

            for session_id in self.pinged_sessions:
                self.remove_client(session_id)

            self.pinged_sessions = []


websocket_clients_manager = WebsocketManager()

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = websocket_clients_manager.add_client(websocket)
    try:
        while (True):
            message = await websocket.receive_text()
            data = json.loads(message)
            if data["type"] == "register":
                user_id = data["user_id"]
                trade_id = data["pair_id"]
                websocket_clients_manager.register_client_for_pair_id(session_id, user_id, trade_id)
                await websocket_clients_manager.send_confirmation(session_id)

            if data["type"] == "leave":
                user_id = data["user_id"]
                trade_id = data["pair_id"]
                websocket_clients_manager.remove_client_for_pair_id(session_id, user_id, trade_id)
                await websocket_clients_manager.send_confirmation(session_id)

            if data["type"] == "pong":
                if session_id in websocket_clients_manager.pinged_sessions:
                    websocket_clients_manager.pinged_sessions.remove(session_id)

    except Exception as e:
        websocket_clients_manager.remove_client(session_id)
