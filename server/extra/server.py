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



from BSE import Asset, Marketplace, User as BSEUser, Database, Order as BSEOrder # type: ignore

db = Database()

clients = []


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

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
    


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(get_orders())
    yield
    
    
app = FastAPI(
    title="Bonn Stock Exchange",
    lifespan=lifespan

)


# Websocket to send a data on client 
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        clients.remove(websocket)



# LOGIN --------------------

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user_id, error = authenticate_user(form_data.username, form_data.password)
    
    if not user_id and error != 'not reg':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user_id and error == 'not reg':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user in nor register",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "user_id": user_id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def authenticate_user(email: str, password: str):
    is_userDB = db.find_user_by_email(email)
    error = ''
    if not is_userDB:
        error = 'not reg'
        return False, error
    if not verify_password(email, password):
        error = 'false pass'
        return False, error
    return is_userDB, error

def verify_password(email, password):
    user = BSEUser(db, email)
    return user.check_password(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# BALANCE ---------------------

@app.get("/balance{email}")
async def get_balance(email):
    user_balanceFRC = db.get_user_balance_frc(email)
    user_balancePOEUR = db.get_user_balance_poeur(email)
    return {"frc": user_balanceFRC, "poeur": user_balancePOEUR}




# REGISTER --------------------

@app.post("/register")
async def register_user(user: User):
    if not db.find_user_by_email(user.email):
        create_user(user.email, user.password)
        return {"status": "reg complete"}
    else:
        return {"status": "user is already reg"}

def create_user(email: str, password: str):
    try:
        BSEUser(db, email, password)
    except Exception as e:
        print(f"{e}")



# TRADES --------------------------
@app.post("/trade")
async def new_trade(order: Order):
    create_order(order.trader_id, order.item, order.pair_item, order.price, order.item_amount)
    return {"status": "trade reg complete"}

def create_order(trader_id: int, item: str, pair_item: str, price: int, item_amount: int):
    try:
        BSEOrder(db, trader_id, item, pair_item, price, item_amount)
    except Exception as e:
        print(f"{e}")

async def get_orders():
    while True:
        await asyncio.sleep(3)
        orders = db.get_all_orders()
        action = "add"
        for order in orders:
            # Websocket
            for client in clients:
                data = {"action": action, "order_id": order.id, "trader_id": order.trader_id, "item": order.item, "pair_item": order.pair_item, 'price': order.price, 'item_amount': order.item_amount}
                try:
                    await client.send_text(json.dumps(data))
                except Exception as e:
                    clients.remove(client)            

# ACCEPT ORDER -------------------

@app.post("/accept_order")
async def accept_order(order: OrderToAccept):
    if ("POEUR" == order.item):
        if(db.get_user_balance_poeur(order.email) >= order.price):
            db.update_user_balance_poeur(order.email, -order.price)
            db.update_user_balance_frc(order.email, order.item_amount)
            # TODO: remove this order from database, we have here order.order_id
        else:
            # TODO: error poeur balance is low
            return # Delete
    elif ("FRC" == order.item):
        print(db.get_user_balance_frc(order.email))
        if(db.get_user_balance_frc(order.email) >= order.price):
            db.update_user_balance_frc(order.email, -order.price)
            db.update_user_balance_poeur(order.email, order.item_amount)
            # TODO: remove from database
        else:
            # TODO: error frc balance is low
            return # Delete
    else:
        # TODO: this type didnt exist
        return # Delete
        



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
