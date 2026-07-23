import config


class TradingModule:
    """
    Trading Engine

    Unterstützt:

    PAPER Trading
    LIVE Trading

    """

    def __init__(self, binance=None, database=None, telegram=None):

        self.enabled = getattr(config, "TRADING_ENABLED", False)

        self.mode = getattr(config, "TRADING_MODE", "PAPER")

        self.binance = binance

        self.database = database

        self.telegram = telegram

        self.position = None

        print("Trading Mode:", self.mode)

    # =========================
    # START / STOP
    # =========================

    def start(self):

        if not self.enabled:

            print("Trading deaktiviert")

            return False

        print("Trading Bot gestartet")

        return True

    def stop(self):

        print("Trading Bot gestoppt")

        return True

    # =========================
    # SIGNAL HANDLER
    # =========================

    def process_signal(self, signal):

        if not self.enabled:

            return

        action = signal.get("signal")

        price = signal.get("price")

        if action == "BUY":

            return self.buy(price)

        elif action == "SELL":

            return self.sell(price)

        return None

    # =========================
    # BUY
    # =========================

    def buy(self, price, quantity=0.001):

        trade = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "price": price,
            "quantity": quantity,
            "mode": self.mode,
            "status": "FILLED",
        }

        # PAPER MODE

        if self.mode == "PAPER":

            print("PAPER BUY", trade)

        # LIVE MODE

        elif self.mode == "LIVE":

            if self.binance:

                trade = self.binance.client.order_market_buy(
                    symbol="BTCUSDT", quantity=quantity
                )

        self.position = trade

        if self.database:

            self.database.add_trade(trade)

        if self.telegram:

            self.telegram.send_buy_alert(price, quantity)

        return trade

    # =========================
    # SELL
    # =========================

    def sell(self, price, quantity=0.001):

        trade = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "price": price,
            "quantity": quantity,
            "mode": self.mode,
            "status": "FILLED",
        }

        if self.mode == "PAPER":

            print("PAPER SELL", trade)

        elif self.mode == "LIVE":

            if self.binance:

                trade = self.binance.client.order_market_sell(
                    symbol="BTCUSDT", quantity=quantity
                )

        self.position = None

        if self.database:

            self.database.add_trade(trade)

        if self.telegram:

            self.telegram.send_sell_alert(price, quantity)

        return trade

    # =========================
    # RISK MANAGEMENT
    # =========================

    def check_stop_loss(self, buy_price, current_price):

        stop_loss = getattr(config, "STOP_LOSS_PERCENT", 5)

        loss = ((buy_price - current_price) / buy_price) * 100

        if loss >= stop_loss:

            return True

        return False

    def check_take_profit(self, buy_price, current_price):

        take_profit = getattr(config, "TAKE_PROFIT_PERCENT", 10)

        profit = ((current_price - buy_price) / buy_price) * 100

        if profit >= take_profit:

            return True

        return False

    # =========================
    # STATUS
    # =========================

    def status(self):

        return {"enabled": self.enabled, "mode": self.mode, "position": self.position}
