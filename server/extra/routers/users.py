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

router = APIRouter(
    tags=["Authentication"]
)

# LOGIN --------------------
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
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


@router.post("/register")
async def register_user(user: User, db: Annotated[Database, Depends(get_database_object)]):
    try:
        user = BSEUser(db, user.email)
        return {"status": "user is already reg"}
    except Exception as e:
        if e == "User not found":
            create_user(db, user.email, user.password)
            return {"status": "reg complete"}


def create_user(db, email: str, password: str):
    try:
        BSEUser(db, email, password)
    except Exception as e:
        print(f"{e}")


def authenticate_user(email: str, password: str):
    user_id = db.find_user_by_email(email)
    error = ''
    if not user_id:
        error = 'not reg'
        return False, error
    if not verify_password(user_id, password):
        error = 'false pass'
        return False, error
    return user_id, error


def verify_password(user_id, password):
    user = BSEUser(db, user_id)
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


def get_user(user_id: int):
    if db.find_user_by_id(user_id):
        return BSEUser(user_id)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


@router.post('/test_balance')
def test_balance(user_id: int, db: Annotated[Database, Depends(get_database_object)]):
    user = BSEUser(db, user_id)
    return user.get_balances()
