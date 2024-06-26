from tkinter import Tk, Listbox, ttk, StringVar, Button, BOTH, messagebox, END

import requests
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap import Style

from state import WindowState

from interactions.trading_pairs import get_trading_pair, get_orders

from interactions.assets import get_assets

from interactions.user import get_balances


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
    def __init__(self, pair_id: int, state: WindowState, return_to_selector_fn):
        super().__init__()

        self.title = "Trading Window"
        self.state = state
        self.pair_id = pair_id

        self.trading_pair = get_trading_pair(self.state.url, pair_id)
        self.assets = get_assets(self.state.url)
        self.balances = get_balances(self.state.url, self.state.token)
        self.orders = get_orders(self.state.url, pair_id)

        if not self.trading_pair or not self.assets or not self.balances:
            messagebox.showerror(title="Parsing error.",
                                 message="Error while parsing data.")
            self.destroy()
            return_to_selector_fn()
            return

        self.open_trading_ui()

    def open_trading_ui(self):
        # Main window
        self.title = "Bonn Stock Exchange"

        # Style settings
        style = Style('darkly')

        # Window settings
        mainframe = ttk.Frame(self, padding="70 70 70 70")
        mainframe.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Balance
        empty_label = ttk.Label(mainframe, text=f"     ")
        empty_label.config(font=("Courier", 12))
        empty_label.grid(column=4, row=0)

        # balance_label = ttk.Label(mainframe, text=f"Currency / Your Balance")
        # balance_label.config(font=("Courier", 12))
        # balance_label.grid(column=5, row=0)
        # BUY_______________________________

        buy = ttk.Frame(mainframe)
        buy.grid(row=2, column=1)
        buy.grid_columnconfigure((0, 1), weight=1)
        buy.grid_rowconfigure(0, weight=1)

        # Scrollbox
        base_asset_ticker = self.assets[self.trading_pair['base_asset']]['ticker'].upper()
        price_asset_ticker = self.assets[self.trading_pair['price_asset']]['ticker'].upper()
        legend_label = ttk.Label(mainframe,
                                 text=f"Trading Pair: {base_asset_ticker}/{price_asset_ticker}\n" \
                                      f"Balance [{base_asset_ticker}]: {self.balances[base_asset_ticker.lower()]['balance'] / 100}\n" + \
                                      f"Balance [{price_asset_ticker}]: {self.balances[price_asset_ticker.lower()]['balance'] / 100}\n"
                                 )
        legend_label.config(font=("Courier", 24))
        legend_label.grid(column=0, row=0)

        listbox_buy = Listbox(mainframe)
        listbox_buy.config(font=("Courier", 14), width=22)
        listbox_buy.grid(row=2, column=0, padx=20, )

        for amount, price in _parse_orderbook(self.orders['buy']):
            listbox_buy.insert(END, f"{amount} {base_asset_ticker} for {price} {price_asset_ticker}")

        # Labels

        price_label = ttk.Label(buy, text=f"Price")
        price_label.config(font=("Courier", 16))
        price_label.grid(column=1, row=1)

        feet_price = StringVar()
        entry_price = ttk.Entry(buy, textvariable=feet_price)
        entry_price.config(font=("Courier", 14))
        entry_price.grid(row=1, column=2, padx=20, pady=5)

        amount_label = ttk.Label(buy, text=f"Amount")
        amount_label.grid(column=1, row=2)
        amount_label.config(font=("Courier", 16))

        feet_amount = StringVar()
        entry_amount = ttk.Entry(buy, textvariable=feet_amount)
        entry_amount.config(font=("Courier", 14))
        entry_amount.grid(row=2, column=2, padx=20, pady=5)

        Button(buy, text=f"BUY --", command=lambda i=0: self.buy_func(feet_price, feet_amount), width=18, height=2,
               bg="red",
               fg="white").grid(column=2, row=3)

        # SELL__________________________

        sell = ttk.Frame(mainframe)
        sell.grid(row=2, column=3)
        sell.grid_columnconfigure((0, 1), weight=1)
        sell.grid_rowconfigure(0, weight=1)

        # Scrollbox
        listbox_sell = Listbox(mainframe)
        listbox_sell.config(font=("Courier", 14), width=22)
        listbox_sell.grid(row=2, column=4)

        for amount, price in _parse_orderbook(self.orders['sell']):
            listbox_sell.insert(END, f"{amount} {base_asset_ticker} for {price} {price_asset_ticker}")
        # Labels

        price_label = ttk.Label(sell, text=f"Price")
        price_label.config(font=("Courier", 16))
        price_label.grid(column=2, row=1)

        feet_price_sell = StringVar()
        entry_price = ttk.Entry(sell, textvariable=feet_price_sell)
        entry_price.config(font=("Courier", 14))
        entry_price.grid(row=1, column=3, padx=20, pady=5)

        amount_label = ttk.Label(sell, text=f"Amount")
        amount_label.grid(column=2, row=2)
        amount_label.config(font=("Courier", 16))

        feet_amount_sell = StringVar()
        entry_amount = ttk.Entry(sell, textvariable=feet_amount_sell)
        entry_amount.config(font=("Courier", 14))
        entry_amount.grid(row=2, column=3, padx=20, pady=5)

        Button(sell, text=f"SELL --", command=lambda i=0: self.sell_func(feet_price_sell, feet_amount_sell), width=18,
               height=2,
               bg="green", fg="white").grid(column=3, row=3)

        # GRAPHIC

        graphic = ttk.Frame(mainframe)
        graphic.grid(row=1, column=2)
        graphic.grid_columnconfigure((0, 1), weight=1)
        graphic.grid_rowconfigure(0, weight=1)

        frame = ttk.Frame(graphic)
        frame.grid(column=6, row=2)

        frame.pack(fill=BOTH, expand=1)

        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        # start_websocket()
        entry_price.focus()

        self.mainloop()

    def update_graphic(self, graphic, canvas, ax):
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

        graphic.after(10000, self.update_graphic)

    def buy_func(self, feet_price, feet_amount):

        price = feet_price.get()
        amount = feet_amount.get()

        try:
            data = {'trader_id': self.state.user_id, 'item': 'FRC', 'pair_item': 'POEUR', 'price': price,
                    'item_amount': amount}
            r = requests.post(f"{self.state.url}/trade", json=data)
            r.raise_for_status()
            r.json()['status'] == 'trade reg complete'

            messagebox.showinfo("", f"comlete")
            return r.json()

        except requests.exceptions.RequestException as e:
            messagebox.showinfo("", f"No Internet!")
            return None

    def sell_func(self, feet_price, feet_amount):
        price = feet_price.get()
        amount = feet_amount.get()

        try:
            data = {'trader_id': self.state.user_id, 'item': 'POEUR', 'pair_item': 'FRC', 'price': price,
                    'item_amount': amount}
            r = requests.post(f"{self.state.url}/trade", json=data)
            r.raise_for_status()
            r.json()['status'] == 'trade reg complete'

            messagebox.showinfo("", f"comlete")
            return r.json()

        except requests.exceptions.RequestException as e:
            messagebox.showinfo("", f"No Internet!")
            return None
