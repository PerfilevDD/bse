from tkinter import Tk, Listbox, Text, END, Label, messagebox, Button, ttk
from state import WindowState

from interactions.assets import get_assets

from ttkbootstrap import Style
from interactions.trading_pairs import get_trading_pairs


class PairSelector(Tk):
    listbox_pairs: Listbox

    def __init__(self, state: WindowState, callback_fn):
        super().__init__()
        self.state = state
        self.assets = get_assets(self.state.url)
        self.callback_fn = callback_fn

        if not self.assets:
            messagebox.showerror(title="Parsing error", message="Error while parsing Assets.")

        self.title = "Select your trading pair"

        self.mainframe = ttk.Frame(self, padding="30 30 30 30")
        self.mainframe.grid(column=0, row=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        style = Style('darkly')

        self.trading_pairs = get_trading_pairs(url=self.state.url)
        self.create_pair_selector_window()

    def create_pair_selector_window(self):
        text = ttk.Label(self.mainframe, text="Please select your trading pair")
        text.grid(column=0, row=0)
        text.config(font=("Courier", 14))

        self.listbox_pairs = Listbox(self.mainframe)
        self.listbox_pairs.config(font=("Courier", 14), width=22)
        self.listbox_pairs.grid(row=1, column=0)

        for trading_pair in self.trading_pairs:
            base_asset_id = trading_pair["base_asset"]
            price_asset_id = trading_pair["price_asset"]
            pair_detail = self.assets[base_asset_id]["ticker"] + "/" + self.assets[price_asset_id]["ticker"]
            string = f"{pair_detail}"
            string = " " * 7 + string
            self.listbox_pairs.insert(trading_pair["pair_id"], string)

        selector = Button(self.mainframe, text="Select", command=self.select_pair, width=32, height=2, bg="green",
                          fg="white")
        selector.grid(row=2, column=0)

    def select_pair(self):
        selected_pair_id = self.listbox_pairs.curselection()[0]
        trading_pair = self.trading_pairs[selected_pair_id]
        self.destroy()
        self.callback_fn(trading_pair["pair_id"])
