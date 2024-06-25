from tkinter import Tk, Listbox, Text, END, Label, messagebox, Button
from state import WindowState

from interactions.assets import get_assets

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
        self.geometry("200x250")

        self.trading_pairs = get_trading_pairs(url=self.state.url)
        self.create_pair_selector_window()

    def create_pair_selector_window(self):
        text = Label(self, text="Please select your trading pair")
        text.grid(column=0, row=0)
        self.listbox_pairs = Listbox(self)
        self.listbox_pairs.config(font=("Courier", 14), width=22)
        self.listbox_pairs.grid(row=1, column=0)
        for trading_pair in self.trading_pairs:
            base_asset_id = trading_pair["base_asset"]
            price_asset_id = trading_pair["price_asset"]
            pair_detail = self.assets[base_asset_id]["ticker"] + "/" + self.assets[price_asset_id]["ticker"]
            self.listbox_pairs.insert(trading_pair["pair_id"] + 1, pair_detail)

        selector = Button(text="Select", command=self.select_pair)
        selector.grid(row=2, column=0)

    def select_pair(self):
        selected_pair_id = self.listbox_pairs.curselection()[0]
        self.destroy()
        self.callback_fn(selected_pair_id)
