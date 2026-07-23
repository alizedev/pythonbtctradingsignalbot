class RiskManager:


    def __init__(self):


        # Kontostand

        self.account_balance = 50.0


        # maximaler Einsatz pro Trade in %

        self.max_trade_percent = 10



        # Stop Loss / Take Profit

        self.stop_loss_percent = 2.0

        self.take_profit_percent = 5.0



        self.open_trade = None






    # ==========================
    # TRADE GRÖSSE
    # ==========================

    def get_trade_amount(self):


        amount = (

            self.account_balance

            *

            self.max_trade_percent

            /

            100

        )


        return round(amount, 2)






    # ==========================
    # DARF TRADE AUSFÜHREN?
    # ==========================

    def allowed_trade(self, amount):


        if amount <= 0:

            return False



        if amount > self.account_balance:

            return False



        return True






    # ==========================
    # STOP LOSS
    # ==========================

    def check_stop_loss(

        self,

        buy_price,

        current_price

    ):


        change = (

            (current_price - buy_price)

            /

            buy_price

        ) * 100



        if change <= -self.stop_loss_percent:

            return True



        return False






    # ==========================
    # TAKE PROFIT
    # ==========================

    def check_take_profit(

        self,

        buy_price,

        current_price

    ):


        change = (

            (current_price - buy_price)

            /

            buy_price

        ) * 100



        if change >= self.take_profit_percent:

            return True



        return False






    # ==========================
    # POSITION ÖFFNEN
    # ==========================

    def open_position(

        self,

        price,

        amount

    ):


        self.open_trade = {


            "buy_price": price,

            "amount": amount

        }







    # ==========================
    # POSITION SCHLIESSEN
    # ==========================

    def close_position(self):


        self.open_trade = None






    # ==========================
    # POSITION AKTUELL?
    # ==========================

    def has_position(self):


        return self.open_trade is not None