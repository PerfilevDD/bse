from typing import Union

from pydantic import BaseModel

# Bet
class BetBase(BaseModel):
    table_id: int
    user_id: int
    type: str
    value: str
    amount: int


class BetCreate(BetBase):
    pass

    
class Bet(BetBase):
    id: int

    class Config:
        orm_mode = True
       


# User
class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    balance: float

    class Config:
        orm_mode = True