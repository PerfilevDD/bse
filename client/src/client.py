from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests
import asyncio
import websockets
import threading
import json
import jwt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ttkbootstrap import Style

from windows.authentication import AuthenticationWindow
from windows.pair_selector import PairSelector
from windows.trade_pair import TradePair
from state import WindowState

from PIL import Image, ImageTk

state = WindowState()


async def listen_for_updates():
    ws_url = url.replace('http', 'ws').replace('htpps', 'wss') + '/ws'
    print("Connecting")
    async with websockets.connect(ws_url) as websocket:
        print("Connected")
        await websocket.send(json.dumps({"action": "register", "user_id": user_id}))
        while True:

            try:
                message = await websocket.recv()
                data = json.loads(message)

                action = data["action"]
                ws_order_id = data["order_id"]
                ws_trader_id = data["trader_id"]
                ws_item = data["item"]
                ws_pair_item = data["pair_item"]
                ws_price = data["price"]
                ws_item_amount = data["item_amount"]

                # update balance
                if data["action"] == "update_balance":
                    new_balance = data["balance"]
                    print(f"New balance for user {user_id}: {new_balance}")

                # update orders

                # calculate space between two parms
                # 21 is length of listbox
                len_ws_price = len(str(ws_price))
                len_ws_item_amount = len(str(ws_item_amount))
                len_spaces = 22 - len_ws_price - len_ws_item_amount

                listbox_entry = f"{ws_price}" + " " * len_spaces + f"{ws_item_amount}"
                order_str = f"Item: {ws_item}, Pair Item: {ws_pair_item}, Price: {ws_price}, Item Amount: {ws_item_amount}"

                # this works, but remake with order_id
                if action == "add":
                    # 1. in current orders save the id's
                    # and check, if exact this id was printed, if not, than pritn
                    # so can we add more same orders in listbox
                    if order_str not in current_orders:
                        if ws_item == 'FRC':
                            listbox_buy.insert(0,
                                               f"{ws_price}" + " " * len_spaces + f"{ws_item_amount}" + "   " + f"{ws_order_id},{ws_trader_id},{ws_item},{ws_price},{ws_item_amount}")
                        elif ws_item == "POEUR":
                            listbox_sell.insert(0,
                                                f"{ws_price}" + " " * len_spaces + f"{ws_item_amount}" + "   " + f"{ws_order_id},{ws_trader_id},{ws_item},{ws_price},{ws_item_amount}")

                        current_orders.add(order_str)

                elif action == "remove":
                    if ws_item == 'FRC':
                        items = listbox_buy.get(0, END)
                        for i, item in enumerate(items):
                            if item == listbox_entry:
                                listbox_buy.delete(i)
                                current_orders.remove(order_str)
                                break
                    elif ws_item == "POEUR":
                        items = listbox_sell.get(0, END)
                        for i, item in enumerate(items):
                            if item == listbox_entry:
                                listbox_sell.delete(i)
                                current_orders.remove(order_str)
                                break

            except websockets.ConnectionClosed:
                break


# ACCEPT ORDER


def start_websocket():
    def run_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(listen_for_updates())

    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_loop, args=(loop,))
    t.start()

    # CURRENCY


def update_currency():
    pass


def open_trade_window(pair_id):
    trade_pair = TradePair(pair_id, state=state, return_to_selector_fn=open_selector)
    trade_pair.mainloop()


def open_selector():
    pair_selector = PairSelector(state=state, callback_fn=open_trade_window)
    pair_selector.mainloop()


authentication_window = AuthenticationWindow(state=state)
authentication_window.mainloop()

open_selector()
