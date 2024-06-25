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
    # lifespan=lifespan

)

app.include_router(router=user_router)
app.include_router(router=orders_router)
app.include_router(router=assets_router)
app.include_router(router=trade_pairs_router)


# Websocket to send a data on client
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)

            if data["action"] == "register":
                user_id = data["user_id"]
                clients[user_id] = websocket
    except Exception as e:
        clients.remove(websocket)




    


# ACCEPT ORDER -------------------

@app.post("/accept_order")
async def accept_order(order: OrderToAccept):
    if ("POEUR" == order.item):
        if (db.get_user_balance_poeur(order.email) >= order.price):
            db.update_user_balance_poeur(order.email, -order.price)
            db.update_user_balance_frc(order.email, order.item_amount)
            # TODO: remove this order from database, we have here order.order_id
        else:
            # TODO: error poeur balance is low
            return  # Delete
    elif ("FRC" == order.item):
        print(db.get_user_balance_frc(order.email))
        if (db.get_user_balance_frc(order.email) >= order.price):
            db.update_user_balance_frc(order.email, -order.price)
            db.update_user_balance_poeur(order.email, order.item_amount)
            # TODO: remove from database
        else:
            # TODO: error frc balance is low
            return  # Delete
    else:
        # TODO: this type didnt exist
        return  # Delete


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
