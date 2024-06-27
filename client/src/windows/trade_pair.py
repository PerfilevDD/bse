import asyncio
import json
import threading
from tkinter import Tk, Listbox, ttk, StringVar, Button, BOTH, messagebox, END
from matplotlib.figure import Figure 
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.style import use as mpl_style

from ttkbootstrap import Style
import requests
import websockets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from state import WindowState

from interactions.trading_pairs import get_trading_pair, get_orders

from interactions.assets import get_assets

from interactions.user import get_balances

from interactions.graph import get_graph_data

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 


def _parse_orderbook(orders):
    old_price = -1
    amount = 0
    for order in orders:
        if order['price'] != old_price and old_price != -1:
            yield (amount, old_price)
            amount = 0
        old_price = order['price']
        amount += order['amount'] - order['fullfilled_amount']
    if old_price != -1:
        yield (amount, old_price)


class TradePair(Tk):
    listbox_sell: Listbox
    listbox_buy: Listbox
    label_text: StringVar
    websocket: websockets
    base_asset_ticker: str
    price_asset_ticker: str

    def __init__(self, pair_id: int, state: WindowState, return_to_selector_fn):
        super().__init__()
        self.open = True
        self.title = "Trading Window"
        self.state = state
        self.pair_id = pair_id
        self.return_to_selector_fn = return_to_selector_fn
        self.trading_pair = get_trading_pair(self.state.url, pair_id)
        self.assets = get_assets(self.state.url)
        self.balances = get_balances(self.state.url, self.state.token)
        self.orders = get_orders(self.state.url, pair_id)
        self.time_data, self.price_data = get_graph_data(self.state.url)

        if not self.trading_pair or not self.assets or not self.balances:
            messagebox.showerror(title="Parsing error.",
                                 message="Error while parsing data.")
            self.after(500, self.destroy())
            return_to_selector_fn()
            return

        self.base_asset_ticker = self.assets[self.trading_pair['base_asset']]['ticker'].upper()
        self.price_asset_ticker = self.assets[self.trading_pair['price_asset']]['ticker'].upper()

        self.open_trading_ui()
        self.update_orderbook()
        self.update_graphic()



        style = Style('darkly')

        self.ws_thread = threading.Thread(target=asyncio.run, args=(self.listen_updates(),), daemon=True)
        self.ws_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    async def listen_updates(self):
        ws_url = self.state.url.replace('http', 'ws').replace('htpps', 'wss') + '/ws'
        self.websocket = await websockets.connect(ws_url)
        self.time_data = []
        self.price_data = []

        await self.websocket.send(json.dumps(
            {"type": "register", "user_id": self.state.user_id, "pair_id": self.pair_id}
        ))

        while self.open:
            try:
                message = await self.websocket.recv()

                if not self.open:
                    break

                data = json.loads(message)
                if "type" in data and data["type"] == "orderbook":
                    self.orders = data["data"]
                    self.update_orderbook()

                if "type" in data and data["type"] == "balances":
                    print(self.balances)
                    self.balances = {
                        balance['ticker']: balance
                        for balance in data["data"]
                    }
                    self.update_balances()
                
                if "type" in data and data["type"] == "order_history":
                    for order in data["data"]:
                        time = datetime.utcfromtimestamp(int(order["time"])//1000)
                        self.time_data.append(time)
                        self.price_data.append(order["price"])
                    self.update_graphic()

                if "type" in data and data["type"] == "ping":
                    await self.websocket.send(json.dumps({"type": "pong"}))

            except:
                pass

        await self.websocket.send(json.dumps(
            {"type": "leave", "user_id": self.state.user_id, "pair_id": self.pair_id}
        ))

        await self.websocket.close()

    def on_close(self):
        self.open = False
        self.after(500, self.destroy)
        self.return_to_selector_fn()

    def open_trading_ui(self):
        
        # Main window

        # Window settings
        mainframe = ttk.Frame(self, padding="70 70 70 70")
        mainframe.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Balance

        
        # BUY_______________________________


        # Scrollbox
        text = f"Trading Pair: {self.base_asset_ticker}/{self.price_asset_ticker}\n" \
               f"Balance [{self.base_asset_ticker}]: {self.balances[self.base_asset_ticker.lower()]['balance']}\n" + \
               f"Balance [{self.price_asset_ticker}]: {self.balances[self.price_asset_ticker.lower()]['balance']}\n"

        self.label_text = StringVar()
        self.label_text.set(text)


        self.listbox_buy = Listbox(mainframe)
        self.listbox_buy.config(font=("Courier", 14), width=22, height=20)
        self.listbox_buy.grid(row=1, column=0, padx=20)

        # Labels


        legend_label = ttk.Label(mainframe, textvariable=self.label_text)
        legend_label.config(font=("Courier", 24))
        legend_label.grid(column=1, row=0)



        center = ttk.Frame(mainframe)
        center.grid(row=2, column=1)
        center.grid_columnconfigure((0, 1), weight=1)
        center.grid_rowconfigure(0, weight=1)

        price_label = ttk.Label(center, text=f"Price")
        price_label.config(font=("Courier", 16))
        price_label.grid(column=0, row=0)

        feet_price = StringVar()
        entry_price = ttk.Entry(center, textvariable=feet_price)
        entry_price.config(font=("Courier", 14))
        entry_price.grid(row=0, column=1, padx=20, pady=5)

        amount_label = ttk.Label(center, text=f"Amount")
        amount_label.grid(column=0, row=1)
        amount_label.config(font=("Courier", 16))

        feet_amount = StringVar()
        entry_amount = ttk.Entry(center, textvariable=feet_amount)
        entry_amount.config(font=("Courier", 14))
        entry_amount.grid(row=1, column=1, padx=20, pady=5)

        Button(center, text=f"BUY", command=lambda i=0: self.create_order(feet_price.get(), feet_amount.get(), True),
               width=18, height=2,
               bg="red",
               fg="white").grid(column=1, row=2)


        # Scrollbox
        self.listbox_sell = Listbox(mainframe)
        self.listbox_sell.config(font=("Courier", 14), width=22, height=20)
        self.listbox_sell.grid(row=1, column=2, padx=20)

        # Labels

        price_label = ttk.Label(center, text=f"Price")
        price_label.config(font=("Courier", 16))
        price_label.grid(column=2, row=0)

        feet_price_sell = StringVar()
        entry_price = ttk.Entry(center, textvariable=feet_price_sell)
        entry_price.config(font=("Courier", 14))
        entry_price.grid(row=0, column=3, padx=20, pady=5)

        amount_label = ttk.Label(center, text=f"Amount")
        amount_label.grid(column=2, row=1)
        amount_label.config(font=("Courier", 16))

        feet_amount_sell = StringVar()
        entry_amount = ttk.Entry(center, textvariable=feet_amount_sell)
        entry_amount.config(font=("Courier", 14))
        entry_amount.grid(row=1, column=3, padx=20, pady=5)

        Button(center, text=f"SELL",
               command=lambda i=0: self.create_order(feet_price_sell.get(), feet_amount_sell.get(), False), width=18,
               height=2,
               bg="green", fg="white").grid(column=3, row=2)

        # GRAPHIC
        
        graphic = ttk.Frame(mainframe)
        graphic.grid(row=1, column=1)
        graphic.grid_columnconfigure((0, 1), weight=1)
        graphic.grid_rowconfigure(0, weight=1)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graphic)
        self.canvas.get_tk_widget().grid(column=0, row=0)




    def update_graphic(self):
        self.ax.clear()

        sorted_data = sorted(zip(self.time_data, self.price_data), key=lambda x: x[0])
        sorted_time_data, sorted_price_data = zip(*sorted_data) if sorted_data else ([], [])

        self.ax.plot(sorted_time_data, sorted_price_data, label="Price")
        self.ax.scatter(sorted_time_data, sorted_price_data, color='red') 
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")
        self.ax.legend()
        
        self.canvas.draw()

        
        

    def create_order(self, price, amount, buy):
        headers = {"Authorization": "Bearer " + self.state.token}
        try:
            parsed_price = int(amount)
            parsed_amount = int(amount)
            data = {'trade_pair_id': self.pair_id,
                    'amount': parsed_amount,
                    'price': parsed_price,
                    'buy': buy
                    }
            r = requests.post(f"{self.state.url}/trade/create", json=data, headers=headers)
            response_data = r.json()

            # Check if a error response code has been returned
            if not r.ok:
                if "detail" in response_data:
                    messagebox.showerror("Error", response_data["detail"])
                else:
                    messagebox.showinfo("", f"Error!")
            else:
                messagebox.showinfo("", f"Order created")
            return response_data

        # Check if the request itself failed
        except requests.exceptions.RequestException as e:
            messagebox.showinfo("", f"Error!")
        except ValueError:
            messagebox.showerror("Invalid Data", "Please enter two valid numbers.")

    def update_orderbook(self):
        self.listbox_buy.delete(0, END)
        for amount, price in _parse_orderbook(self.orders['buy']):
            self.listbox_buy.insert(END, f"{amount} {self.base_asset_ticker} for {price} {self.price_asset_ticker}")

        self.listbox_sell.delete(0, END)
        for amount, price in _parse_orderbook(self.orders['sell']):
            self.listbox_sell.insert(END, f"{amount} {self.base_asset_ticker} for {price} {self.price_asset_ticker}")

    def update_balances(self):
        text = f"Trading Pair: {self.base_asset_ticker}/{self.price_asset_ticker}\n" \
               f"Balance [{self.base_asset_ticker}]: {self.balances[self.base_asset_ticker.lower()]['balance']}\n" + \
               f"Balance [{self.price_asset_ticker}]: {self.balances[self.price_asset_ticker.lower()]['balance']}\n"

        self.label_text.set(text)
        self.update()
