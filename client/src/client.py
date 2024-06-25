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
from state import WindowState

from PIL import Image, ImageTk

state = WindowState()


# Balance
def get_user_balance(email: str):
    global balanceFRC, balancePOEUR
    try:
        r = requests.get(f"{url}/balance{email}")
        r.raise_for_status()
        balanceFRC = r.json()['frc']
        balancePOEUR = r.json()['poeur']
    except requests.exceptions.RequestException as e:
        messagebox.showerror("", f"No Internet")

    # Registrarion

    # MAINWINDOW ------------------------------


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

def accept_order(item):
    string = item.get(item.curselection()[0])[25:]
    dataset = list(string.split(","))

    order_id = dataset[0]
    trader_id = dataset[1]
    type_dataset = dataset[2]
    price = dataset[3]
    amount = dataset[4]

    try:
        data = {'email': user_email, 'order_id': order_id, 'trader_id': trader_id, 'item': type_dataset, 'price': price,
                'item_amount': amount}
        r = requests.post(f"{url}/accept_order", json=data)
        r.raise_for_status()
        return r.json()
    except:
        messagebox.showinfo("", f"No Internet!")

    print(f"{order_id} {trader_id} {type_dataset} {price} {amount}")


def start_websocket():
    def run_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(listen_for_updates())

    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_loop, args=(loop,))
    t.start()


def buy_func(feet_price, feet_amount):
    global url

    price = feet_price.get()
    amount = feet_amount.get()

    try:
        data = {'trader_id': user_id, 'item': 'FRC', 'pair_item': 'POEUR', 'price': price, 'item_amount': amount}
        r = requests.post(f"{url}/trade", json=data)
        r.raise_for_status()
        r.json()['status'] == 'trade reg complete'

        messagebox.showinfo("", f"comlete")
        return r.json()

    except requests.exceptions.RequestException as e:
        messagebox.showinfo("", f"No Internet!")
        return None


def sell_func(feet_price, feet_amount):
    global url

    price = feet_price.get()
    amount = feet_amount.get()

    try:
        data = {'trader_id': user_id, 'item': 'POEUR', 'pair_item': 'FRC', 'price': price, 'item_amount': amount}
        r = requests.post(f"{url}/trade", json=data)
        r.raise_for_status()
        r.json()['status'] == 'trade reg complete'

        messagebox.showinfo("", f"comlete")
        return r.json()

    except requests.exceptions.RequestException as e:
        messagebox.showinfo("", f"No Internet!")
        return None

    # CURRENCY


def update_currency():
    pass


def open_game_window():
    global root, entry_price, entry_amount, listbox_buy, listbox_sell, listbox_balance

    # Main window
    root = Tk()
    root.title("Bonn Stock Exchange")

    # Style settings
    style = Style('darkly')

    # Window settings
    mainframe = ttk.Frame(root, padding="70 70 70 70")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Balance

    empty_label = ttk.Label(mainframe, text=f"     ")
    empty_label.config(font=("Courier", 12))
    empty_label.grid(column=4, row=0)

    balance_label = ttk.Label(mainframe, text=f"Currency / Your Balance")
    balance_label.config(font=("Courier", 12))
    balance_label.grid(column=5, row=0)

    listbox_balance = Listbox(mainframe)
    listbox_balance.config(font=("Courier", 14), width=22)
    listbox_balance.grid(row=1, column=5)

    # BUY_______________________________

    Buy = ttk.Frame(mainframe)
    Buy.grid(row=1, column=1)
    Buy.grid_columnconfigure((0, 1), weight=1)
    Buy.grid_rowconfigure(0, weight=1)

    # Scrollbox

    legend_label = ttk.Label(mainframe, text=f"Price(POEUR)    Amount(--)")
    legend_label.config(font=("Courier", 12))
    legend_label.grid(column=0, row=0)

    listbox_buy = Listbox(mainframe)
    listbox_buy.config(font=("Courier", 14), width=22)
    listbox_buy.grid(row=1, column=0)

    # Labels 

    price_label = ttk.Label(Buy, text=f"Price")
    price_label.config(font=("Courier", 16))
    price_label.grid(column=0, row=0)

    feet_price = StringVar()
    entry_price = ttk.Entry(Buy, textvariable=feet_price)
    entry_price.config(font=("Courier", 14))
    entry_price.grid(row=0, column=1, padx=20, pady=5)

    amount_label = ttk.Label(Buy, text=f"Amount")
    amount_label.grid(column=0, row=1)
    amount_label.config(font=("Courier", 16))

    feet_amount = StringVar()
    entry_amount = ttk.Entry(Buy, textvariable=feet_amount)
    entry_amount.config(font=("Courier", 14))
    entry_amount.grid(row=1, column=1, padx=20, pady=5)

    Button(Buy, text=f"BUY --", command=lambda i=0: buy_func(feet_price, feet_amount), width=18, height=2, bg="red",
           fg="white").grid(column=1, row=2)

    # SELL__________________________

    Sell = ttk.Frame(mainframe)
    Sell.grid(row=1, column=2)
    Sell.grid_columnconfigure((0, 1), weight=1)
    Sell.grid_rowconfigure(0, weight=1)

    # Scrollbox
    legend_label = ttk.Label(mainframe, text=f"Price(POEUR)    Amount(--)")
    legend_label.config(font=("Courier", 12))
    legend_label.grid(column=3, row=0)

    listbox_sell = Listbox(mainframe)
    listbox_sell.config(font=("Courier", 14), width=22)
    listbox_sell.grid(row=1, column=3)

    # Labels 

    price_label = ttk.Label(Sell, text=f"Price")
    price_label.config(font=("Courier", 16))
    price_label.grid(column=1, row=0)

    feet_price_sell = StringVar()
    entry_price = ttk.Entry(Sell, textvariable=feet_price_sell)
    entry_price.config(font=("Courier", 14))
    entry_price.grid(row=0, column=2, padx=20, pady=5)

    amount_label = ttk.Label(Sell, text=f"Amount")
    amount_label.grid(column=1, row=1)
    amount_label.config(font=("Courier", 16))

    feet_amount_sell = StringVar()
    entry_amount = ttk.Entry(Sell, textvariable=feet_amount_sell)
    entry_amount.config(font=("Courier", 14))
    entry_amount.grid(row=1, column=2, padx=20, pady=5)

    Button(Sell, text=f"SELL --", command=lambda i=0: sell_func(feet_price_sell, feet_amount_sell), width=18, height=2,
           bg="green", fg="white").grid(column=2, row=2)

    # GRAPHIC

    graphic = ttk.Frame(mainframe)
    graphic.grid(row=1, column=6)
    graphic.grid_columnconfigure((0, 1), weight=1)
    graphic.grid_rowconfigure(0, weight=1)

    frame = ttk.Frame(graphic)
    frame.grid(column=6, row=1)

    frame.pack(fill=BOTH, expand=1)

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)

    start_websocket()
    entry_price.focus()

    root.mainloop()


def update_graphic(graphic, canvas, ax):
    database = []
    price_data = [data['price'] for data in database]
    time_data = [data['time'] for data in database]

    ax.clear()

    ax.plot(price_data, label='Price')
    ax.plot(time_data, label='Time')

    ax.set_xlabel('Trade Index')
    ax.set_ylabel('Price')
    ax.set_title('Currency Price Chart')
    ax.legend()

    canvas.draw()

    graphic.after(10000, update_graphic)


def open_trade_window(pair_id):
    print("Opening")


# open_game_window()
pair_selector = PairSelector(state=state, callback_fn=open_trade_window)
pair_selector.mainloop()

authentication_window = AuthenticationWindow(state=state)
authentication_window.mainloop()
