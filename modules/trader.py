from modules.risk import RiskManager
from modules.trade_history import TradeHistory


class Trader:

    def __init__(self, binance):

        self.binance = binance

        self.risk = RiskManager()

        self.history = TradeHistory()

        self.position = False

        self.entry_price = 0

        self.quantity = 0

    def execute_signal(self, signal):

        action = signal.get("signal", "HOLD")

        price = signal.get("price", 0)

        confidence = signal.get("confidence", 0)

        print(f"📊 SIGNAL: {action} | Confidence: {confidence}% | Price: {price}")

        # Mindest-Confidence auf 45% gesetzt

        if confidence < 45:

            print("⚠ Signal unter 45% - ignoriert")

            return

        if action == "BUY":

            self.buy(price)

        elif action == "SELL":

            self.sell(price)

        else:

            print("⏸ HOLD")

    def buy(self, price):

        if self.position:

            print("⚠ BTC Position bereits offen")

            return

        quantity = self.risk.calculate_quantity(price)

        print(f"🟢 BUY ORDER: {quantity} BTC @ {price}")

        # Binance Kauf

        self.binance.buy_market(quantity)

        # History speichern

        self.history.add_trade("BUY", price, quantity)

        self.position = True

        self.entry_price = price

        self.quantity = quantity

    def sell(self, price):

        if not self.position:

            print("⚠ Keine BTC Position zum Verkaufen")

            return

        print(f"🔴 SELL ORDER: {self.quantity} BTC @ {price}")

        # Binance Verkauf

        self.binance.sell_market(self.quantity)

        # History speichern

        self.history.add_trade("SELL", price, self.quantity)

        profit = (price - self.entry_price) * self.quantity

        fee = self.risk.calculate_fee(price, self.quantity)

        profit_after_fee = profit - fee

        print(f"💰 Profit: {profit_after_fee:.4f} USDT")

        self.position = False

        self.entry_price = 0

        self.quantity = 0

    def check_risk(self, current_price):

        if not self.position:

            return

        result = self.risk.check_exit(self.entry_price, current_price)

        if result["action"] == "SELL":

            print("🚨", result["reason"])

            self.sell(current_price)
