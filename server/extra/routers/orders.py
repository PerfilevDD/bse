from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from starlette import status

from dependencies import get_database_object
from models.models import User, Token, TokenData

from jwt.exceptions import InvalidTokenError

from BSE import User as BSEUser, Database


db = Database()


router = APIRouter(
    tags=["Orders"]
)




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")