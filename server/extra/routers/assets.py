from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from starlette import status

from dependencies import get_database_object
from models.models import User, Token, TokenData

from jwt.exceptions import InvalidTokenError

from BSE import User as BSEUser, Database, Asset

db = Database()

router = APIRouter(
    tags=["Assets"]
)


@router.get("/assets")
def get_assets(db: Annotated[Database, Depends(get_database_object)]):
    trade_pairs = Asset.get_all_assets(db)
    return {
        "assets": [{
            "asset_id": t.get_asset_id(),
            "name": t.get_asset_name(),
            "ticker": t.get_asset_ticker(),
        } for t in trade_pairs]
    }
