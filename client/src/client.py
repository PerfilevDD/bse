from windows.authentication import AuthenticationWindow
from windows.pair_selector import PairSelector
from windows.trade_pair import TradePair
from state import WindowState

state = WindowState()

def open_trade_window(pair_id):
    trade_pair = TradePair(pair_id, state=state, return_to_selector_fn=open_selector)
    trade_pair.mainloop()


def open_selector():
    pair_selector = PairSelector(state=state, callback_fn=open_trade_window)
    pair_selector.mainloop()


authentication_window = AuthenticationWindow(state=state)
authentication_window.mainloop()

if state.token:
    open_selector()
