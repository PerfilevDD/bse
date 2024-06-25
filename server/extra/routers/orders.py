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
        






oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")