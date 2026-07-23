from modules.risk import RiskManager
from modules.trade_history import TradeHistory



class Trader:


    def __init__(
            self,
            binance
    ):


        self.binance = binance

        self.risk = RiskManager()

        self.history = TradeHistory()


        self.position = None

        self.entry_price = 0

        self.quantity = 0





    def execute_signal(
            self,
            signal
    ):


        action = signal.get(
            "signal"
        )


        price = signal.get(
            "price"
        )



        confidence = signal.get(
            "confidence",
            0
        )



        print(

            "TRADER:",

            action,

            "Confidence:",

            confidence

        )



        # Nur starke Signale handeln

        if confidence < 70:

            print(

                "Signal zu schwach"

            )

            return





        if action == "BUY":


            self.buy(
                price
            )





        elif action == "SELL":


            self.sell(
                price
            )







    def buy(
            self,
            price
    ):


        if self.position:

            print(

                "Bereits BTC Position"

            )

            return



        quantity = self.risk.calculate_quantity(

            price

        )



        order = self.binance.buy_market(

            quantity

        )



        self.position = "BTC"

        self.entry_price = price

        self.quantity = quantity



        self.history.add_trade(

            "BUY",

            price,

            quantity

        )



        print(

            "🟢 BUY",

            quantity,

            "BTC @",

            price

        )







    def sell(
            self,
            price
    ):


        if not self.position:


            print(

                "Keine Position"

            )

            return





        order = self.binance.sell_market(

            self.quantity

        )



        self.history.add_trade(

            "SELL",

            price,

            self.quantity

        )



        profit = (

            price -
            self.entry_price

        ) * self.quantity



        print(

            "🔴 SELL",

            self.quantity,

            "BTC @",

            price,

            "PROFIT:",

            round(
                profit,
                2
            )

        )



        self.position = None

        self.entry_price = 0

        self.quantity = 0