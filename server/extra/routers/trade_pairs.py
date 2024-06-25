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

db = Database()

router = APIRouter(
    tags=["Trade Pairs"]
)


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
