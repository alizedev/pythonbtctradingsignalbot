import json
import os
from datetime import datetime


FILE = "trade_history.json"


class TradeHistory:

    def __init__(self):

        self.trades = []

        self.load()

    def load(self):

        if os.path.exists(FILE):

            with open(FILE, "r") as f:

                self.trades = json.load(f)

    def save(self):

        with open(FILE, "w") as f:

            json.dump(self.trades, f, indent=4)

    def add_trade(self, side, price, quantity):

        fee = price * quantity * 0.001

        trade = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "side": side,
            "symbol": "BTCUSDT",
            "price": price,
            "quantity": quantity,
            "fee": fee,
        }

        self.trades.append(trade)

        self.save()

        print("TRADE SAVED:", trade)

    def get_history(self):

        return self.trades
