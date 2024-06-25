from tkinter import Tk, Listbox, ttk, StringVar, Button, BOTH, messagebox

import requests
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap import Style

from client.src.state import WindowState


class TradePair(Tk):
    def __init__(self, pair_id: int, state: WindowState):
        super().__init__()

        self.title = "Trading Window"
        self.state = state
        self.pair_id = pair_id

    def open_game_window(self):
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

        buy = ttk.Frame(mainframe)
        buy.grid(row=1, column=1)
        buy.grid_columnconfigure((0, 1), weight=1)
        buy.grid_rowconfigure(0, weight=1)

        # Scrollbox

        legend_label = ttk.Label(mainframe, text=f"Price(POEUR)    Amount(--)")
        legend_label.config(font=("Courier", 12))
        legend_label.grid(column=0, row=0)

        listbox_buy = Listbox(mainframe)
        listbox_buy.config(font=("Courier", 14), width=22)
        listbox_buy.grid(row=1, column=0)

        # Labels

        price_label = ttk.Label(buy, text=f"Price")
        price_label.config(font=("Courier", 16))
        price_label.grid(column=0, row=0)

        feet_price = StringVar()
        entry_price = ttk.Entry(buy, textvariable=feet_price)
        entry_price.config(font=("Courier", 14))
        entry_price.grid(row=0, column=1, padx=20, pady=5)

        amount_label = ttk.Label(buy, text=f"Amount")
        amount_label.grid(column=0, row=1)
        amount_label.config(font=("Courier", 16))

        feet_amount = StringVar()
        entry_amount = ttk.Entry(buy, textvariable=feet_amount)
        entry_amount.config(font=("Courier", 14))
        entry_amount.grid(row=1, column=1, padx=20, pady=5)

        Button(buy, text=f"BUY --", command=lambda i=0: self.buy_func(feet_price, feet_amount), width=18, height=2,
               bg="red",
               fg="white").grid(column=1, row=2)

        # SELL__________________________

        sell = ttk.Frame(mainframe)
        sell.grid(row=1, column=2)
        sell.grid_columnconfigure((0, 1), weight=1)
        sell.grid_rowconfigure(0, weight=1)

        # Scrollbox
        legend_label = ttk.Label(mainframe, text=f"Price(POEUR)    Amount(--)")
        legend_label.config(font=("Courier", 12))
        legend_label.grid(column=3, row=0)

        listbox_sell = Listbox(mainframe)
        listbox_sell.config(font=("Courier", 14), width=22)
        listbox_sell.grid(row=1, column=3)

        # Labels

        price_label = ttk.Label(sell, text=f"Price")
        price_label.config(font=("Courier", 16))
        price_label.grid(column=1, row=0)

        feet_price_sell = StringVar()
        entry_price = ttk.Entry(sell, textvariable=feet_price_sell)
        entry_price.config(font=("Courier", 14))
        entry_price.grid(row=0, column=2, padx=20, pady=5)

        amount_label = ttk.Label(sell, text=f"Amount")
        amount_label.grid(column=1, row=1)
        amount_label.config(font=("Courier", 16))

        feet_amount_sell = StringVar()
        entry_amount = ttk.Entry(sell, textvariable=feet_amount_sell)
        entry_amount.config(font=("Courier", 14))
        entry_amount.grid(row=1, column=2, padx=20, pady=5)

        Button(sell, text=f"SELL --", command=lambda i=0: self.sell_func(feet_price_sell, feet_amount_sell), width=18,
               height=2,
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

        # start_websocket()
        entry_price.focus()

        root.mainloop()

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
        global url

        price = feet_price.get()
        amount = feet_amount.get()

        try:
            data = {'trader_id': self.state.user_id, 'item': 'FRC', 'pair_item': 'POEUR', 'price': price,
                    'item_amount': amount}
            r = requests.post(f"{url}/trade", json=data)
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
            r = requests.post(f"{url}/trade", json=data)
            r.raise_for_status()
            r.json()['status'] == 'trade reg complete'

            messagebox.showinfo("", f"comlete")
            return r.json()

        except requests.exceptions.RequestException as e:
            messagebox.showinfo("", f"No Internet!")
            return None
