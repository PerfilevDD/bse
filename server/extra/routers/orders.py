from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from starlette import status

from dependencies import get_database_object
from models.models import User, Token, TokenData

from jwt.exceptions import InvalidTokenError

from BSE import User as BSEUser, Database, TradePair

from routers.users import get_current_user

db = Database()

router = APIRouter(
    tags=["Orders"]
)


# TRADES --------------------------

@router.post("/trade")
async def create_trade(base_asset_id: int, price_asset_id: int,
                       amount: int, price: int, buy: bool,
                       db: Annotated[Database, Depends(get_database_object)],
                       current_user: Annotated[User, Depends(get_current_user)]):
    try:
        new_trade = TradePair(db, base_asset_id, price_asset_id)

        new_trade.create_order(new_trade.get_trade_pair_id(), current_user.get_user_id(), amount, price, buy)
        return {"status": "complete"}
    except Exception as e:

        print(f"{e}")


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
