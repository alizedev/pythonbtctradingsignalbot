from binance.client import Client
from binance.exceptions import BinanceAPIException

from config import (
    BINANCE_API_KEY,
    BINANCE_SECRET_KEY
)


class BinanceService:
    """
    Binance API Verbindung
    """

    def __init__(self):

        self.client = Client(
            BINANCE_API_KEY,
            BINANCE_SECRET_KEY
        )


    # =========================
    # MARKET DATA
    # =========================


    def get_btc_price(self):
        """
        Aktueller BTC Preis
        """

        ticker = self.client.get_symbol_ticker(
            symbol="BTCUSDT"
        )

        return float(
            ticker["price"]
        )



    def get_candles(
        self,
        symbol="BTCUSDT",
        interval=Client.KLINE_INTERVAL_1HOUR,
        limit=100
    ):
        """
        Historische Kerzen
        """

        candles = self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )

        return candles



    # =========================
    # ACCOUNT
    # =========================


    def get_account(self):
        """
        Binance Account Daten
        """

        return self.client.get_account()



    def get_balance(
        self,
        asset
    ):
        """
        Coin Bestand abrufen
        """

        balance = self.client.get_asset_balance(
            asset=asset
        )


        if balance is None:
            return 0


        return float(
            balance["free"]
        )



    def get_btc_balance(self):

        return self.get_balance(
            "BTC"
        )



    def get_usdt_balance(self):

        return self.get_balance(
            "USDT"
        )



    # =========================
    # PORTFOLIO
    # =========================


    def get_portfolio_value(self):

        btc = self.get_btc_balance()

        usdt = self.get_usdt_balance()

        btc_price = self.get_btc_price()


        return (
            btc * btc_price
            + usdt
        )



    def get_all_balances(self):
        """
        Alle Coins mit Bestand
        """

        account = self.get_account()


        result = []


        for item in account["balances"]:

            amount = float(
                item["free"]
            )


            if amount > 0:

                result.append(
                    {
                        "asset": item["asset"],
                        "amount": amount
                    }
                )


        return result



    # =========================
    # TRADING HISTORY
    # =========================


    def get_trades(
        self,
        symbol="BTCUSDT"
    ):
        """
        Eigene Trades
        """

        return self.client.get_my_trades(
            symbol=symbol
        )



    # =========================
    # ORDERS
    # =========================


    def get_open_orders(
        self,
        symbol="BTCUSDT"
    ):

        return self.client.get_open_orders(
            symbol=symbol
        )



    # =========================
    # TEST
    # =========================


    def test_connection(self):

        try:

            account = self.client.get_account()

            return True


        except BinanceAPIException:

            return False