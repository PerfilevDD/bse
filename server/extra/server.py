import argparse, uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, WebSocket
from fairoulette import Randomizer, Bet, Table  # type: ignore

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from typing import Optional

import database.models as models
import database.database as database
import database.crud as crud
import database.schemas as schemas

import asyncio
import time
import threading
import json

tables: list[Table] = []
results: list[int] = []
round_duration: int = 5

clients = []

async def run_roulette_game(db: Session):
    while True:
        await asyncio.sleep(round_duration)
        for table in tables:
            result_random = table.calculate_result()
            results[table.get_table_id() - 1] = result_random
            print(f"Table: {table.get_table_id()} - Result: {result_random}")
            balance_to_client = 0
            win_client = 2
            
            # Bets
            for bet in table.get_and_clear_bets():
                received = bet.calculate_result(result_random)
                placed_sum = bet.get_bet_worth()
                print("Bet", bet.get_bet_id(), "for user ID ", bet.get_user_id() ,"placed", placed_sum, "and received", received)
                if received > 0:
                    print("Updating balance")
                    crud.process_bet(db, bet.get_bet_id(), bet.get_user_id(), table.get_table_id(), received)
                    balance_to_client = received
                    win_client = 1
                else:
                    win_client = 0
                    # Websocket

                for client in clients:
                    data = {"result": result_random, "balance": balance_to_client, "win": win_client, 'user_id': bet.get_user_id()}
                    try:
                        await client.send_text(json.dumps(data))
                    except Exception as e:
                        clients.remove(client)


            crud.close_all_open_bets(db=db)




@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    crud.close_all_open_bets(db)
    for table in crud.get_tables(db):
        tables.append(Table(table.id))
        results.append(-1)
    asyncio.create_task(run_roulette_game(db))
    yield
    crud.close_all_open_bets(db)


app = FastAPI(
    title="Fairroulette",
    lifespan=lifespan
)

# Database

models.Base.metadata.create_all(bind=database.db)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Websocket to send a data on client 
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        clients.remove(websocket)

# create new user
@app.post("/users", response_model=schemas.User, tags=["User"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, name=user.name)


# get bet from user
@app.post("/bet", response_model=schemas.Bet, tags=["Bet"])
def create_bet(bet: schemas.BetBase, db: Session = Depends(get_db)):

    db_bet = crud.check_if_user_has_open_bet(db=db, user_id=bet.user_id, table_id=bet.table_id)

    if db_bet:
        print("User is editing bet", db_bet.id)
        bet_obj = tables[bet.table_id].get_bet_by_bet_id(db_bet.id)
        db_bet.type = "multibet"
        db_bet.value = "*"
        db_bet.amount += bet.amount
        db.commit()


    else:
        print("User created a new bet.")
        db_bet = crud.create_bet(db=db, user_id=bet.user_id, table_id=bet.table_id, type=bet.type, value=bet.value, amount=bet.amount)
        bet_obj = Bet(bet.user_id, db_bet.id)

    user = crud.get_user_id(db, bet.user_id)

    if user.balance < bet.amount:
        raise HTTPException(
            status=500,
            details="Not enough balance to do this."
        )

    user.balance -= bet.amount



# bet's types
    if 'number' == bet.type:
        bet_obj.add_number_bet(int(bet.value), bet.amount)
    elif 'col' == bet.type:
        bet_obj.add_dozen_bet(int(bet.value), bet.amount)
    elif 'doz' == bet.type:
        bet_obj.add_dozen_bet(int(bet.value), bet.amount)
    elif 'parity' == bet.type:
        if '0' == bet.value:
            bet_obj.add_even_bet(bet.amount)
        else:
            bet_obj.add_odd_bet(bet.amount)
    elif 'color' == bet.type:
        if 'red' == bet.value:
            bet_obj.add_red_bet(bet.amount)
        else:
            bet_obj.add_black_bet(bet.amount)
        
    tables[bet.table_id].add_or_update_bet_by_bet_id(db_bet.id, bet_obj)

    return db_bet




@app.get("/users/{name}", response_model=schemas.User, tags=["User"])
def read_user(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_name(db, name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# give a result to user
@app.get("/get_result/{user_id}/", response_model=schemas.Bet, tags=["Bet"])
def get_result(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_id(db, user_id)
    return user


#
@app.get("/get_result/{table_id}")
async def post_random(table_id: int):
    return {'result': results[table_id - 1]}

@app.get("/tables", tags=["Table"])
async def get_tables(db: Session = Depends(get_db)):

    return {
        "tables": [table.id for table in crud.get_tables(db)]
    }

@app.post("/table", tags=["Table"])
async def create_table(db: Session = Depends(get_db)):
    table = crud.create_table(db)
    return {
        "table": table.id
    }
@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url="/docs")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-rd', '--round_duration', type=int,  default=30)
    parser.add_argument('-p', '--port', type=int, default=8000, help="The port on which the api will be accessible.")
    parser.add_argument('-ho', '--host', default="localhost", help="The host on which the api will be accessible.")
    args = parser.parse_args()

    round_duration = args.round_duration
    print(f"Round duration is set at {round_duration}")

    uvicorn.run(app, host=args.host, port=args.port)
