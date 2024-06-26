from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from starlette import status

from dependencies import get_database_object

from jwt.exceptions import InvalidTokenError

from BSE import User as BSEUser, Database, TradePair, Order


db = Database()

router = APIRouter(
    tags=["Orders"]
)


# TRADES --------------------------

        
@router.get("/orders/all")
def get_all_completed_orders(db: Annotated[Database, Depends(get_database_object)]):
    all_orders = Order.get_all_completed_orders(db)
    return {
        "order": [{
            "order_id": t.get_order_id(),
            "trader_id": t.get_trader_id(),
            "price": t.get_price(),
            "amount": t.get_amount(),
            "fullfilled_amount": t.get_fullfilled_amount(),
            "completed_timestamp": t.get_completed_timestamp(),
            "completed": t.is_completed(),
            "buy": t.is_buy()
        } for t in all_orders]
    }


@router.get("/orders/{pair_id}")
def get_open_orders(pair_id: int, db: Annotated[Database, Depends(get_database_object)]):
    trade_pair = TradePair(db, pair_id)
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
    return {
        "buy": buy_orders,
        "sell": sell_orders
    }
    
@router.post("/orders/complete")
def set_order_complete(order_id: int, db: Annotated[Database, Depends(get_database_object)]):
    order = Order(db, order_id)
    order.set_completed(1)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")