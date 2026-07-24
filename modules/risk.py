class RiskManager:

    def __init__(self):

        self.max_trade_usdt = 50

        self.stop_loss_percent = 2

        self.take_profit_percent = 3

        self.fee = 0.001

    def calculate_quantity(self, price, balance=None):

        if balance is None:

            balance = self.max_trade_usdt

        amount = min(balance, self.max_trade_usdt)

        quantity = amount / price

        return round(quantity, 6)

    def calculate_fee(self, price, quantity):

        return round(price * quantity * self.fee, 6)

    def stop_loss_price(self, entry_price):

        return round(entry_price * (1 - self.stop_loss_percent / 100), 2)

    def take_profit_price(self, entry_price):

        return round(entry_price * (1 + self.take_profit_percent / 100), 2)

    def check_exit(self, entry_price, current_price):

        stop = self.stop_loss_price(entry_price)

        target = self.take_profit_price(entry_price)

        if current_price <= stop:

            return {"action": "SELL", "reason": "STOP LOSS"}

        if current_price >= target:

            return {"action": "SELL", "reason": "TAKE PROFIT"}

        return {"action": "HOLD", "reason": "WAIT"}
