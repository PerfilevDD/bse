from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    email: str
    password: str

class Order(BaseModel):
    trader_id: int
    item: str
    pair_item: str
    price: int
    item_amount: int


class OrderToAccept(BaseModel):
    email: str
    order_id: int
    trader_id: int
    item: str
    price: int
    item_amount: int
