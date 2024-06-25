from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from starlette import status

from dependencies import get_database_object

from jwt.exceptions import InvalidTokenError

from BSE import User as BSEUser, Database, TradePair


db = Database()

router = APIRouter(
    tags=["Orders"]
)


# TRADES --------------------------

        


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")