import traceback
from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from starlette import status

from dependencies import get_database_object

from jwt.exceptions import InvalidTokenError

from BSE import User as BSEUser, Database, TradePair
from routers.users import get_current_user
from routers.websocket import websocket_clients_manager
from models.models import Trade, User

db = Database()

router = APIRouter(
    tags=["Trade Pairs"]
)


@router.post("/trade-pairs")
def new_trade_pairs(base_asset_id: int, price_asset_id: int, db: Annotated[Database, Depends(get_database_object)]):
    new_item = TradePair(db, base_asset_id, price_asset_id)
    return {"status": "complete"}


@router.get("/trade-pairs")
def get_trade_pairs(db: Annotated[Database, Depends(get_database_object)]):
    trade_pairs = TradePair.get_all_trade_pairs(db)
    return {
        "trade_pairs": [{
            "pair_id": t.get_trade_pair_id(),
            "base_asset": t.get_base_asset(),
            "price_asset": t.get_price_asset(),
        } for t in trade_pairs]
    }


@router.get("/trade-pairs/{pair_id}")
def get_trade_pair(pair_id: int, db: Annotated[Database, Depends(get_database_object)]):
    try:
        trade_pair = TradePair(db, pair_id)
    except:
        raise HTTPException(status_code=404, detail="Trading Pair not found")

    return {
        "pair_id": trade_pair.get_trade_pair_id(),
        "base_asset": trade_pair.get_base_asset(),
        "price_asset": trade_pair.get_price_asset(),
    }


@router.post("/trade/create")
async def create_trade(trade: Trade, db: Annotated[Database, Depends(get_database_object)],
                       current_user: Annotated[User, Depends(get_current_user)]):
    try:
        new_trade = TradePair(db, trade.trade_pair_id)
        new_trade.create_order(new_trade.get_trade_pair_id(), current_user.get_user_id(), trade.amount, trade.price,
                               trade.buy)
        await websocket_clients_manager.process_orderbooks_update(trade.trade_pair_id)
        await websocket_clients_manager.process_balance_updates(trade.trade_pair_id)
        return {"status": "complete"}

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Trade couldn't be completed")


@router.get("/trade/all")
async def get_orders(trade_pair_id: int):
    trade_pairs = TradePair.get_orders_as_python_list(trade_pair_id)
    print(trade_pairs)
