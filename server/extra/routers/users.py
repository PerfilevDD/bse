from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from server.extra.dependencies import get_database_object
from server.extra.models.models import User, Token

from BSE import User as BSEUser, Database

router = APIRouter()

# LOGIN --------------------
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
async def register_user(user: User, db: Annotated[dict, Depends(get_database_object)]):
    if not db.find_user_by_email(user.email):
        create_user(db, user.email, user.password)
        return {"status": "reg complete"}
    else:
        return {"status": "user is already reg"}

def create_user(db, email: str, password: str):
    try:
        BSEUser(db, email, password)
    except Exception as e:
        print(f"{e}")

def authenticate_user(db, email: str, password: str):
    is_userDB = db.find_user_by_email(email)
    error = ''
    if not is_userDB:
        error = 'not reg'
        return False, error
    if not verify_password(email, password):
        error = 'false pass'
        return False, error
    return is_userDB, error

def verify_password(db, email, password):
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

