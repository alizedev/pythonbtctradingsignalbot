class RiskManager:


    def __init__(self):


        # Startkapital Paper Trading

        self.balance = 500.0


        # maximaler Einsatz pro Trade

        self.trade_percent = 2.0


        # Verlustgrenze

        self.stop_loss_percent = 2.5


        # Gewinnziel

        self.take_profit_percent = 5.0







    # ==========================
    # TRADE AMOUNT
    # ==========================

    def get_trade_amount(self):


        amount = (

            self.balance

            *

            (

                self.trade_percent

                /

                100

            )

        )



        return round(

            amount,

            2

        )







    # ==========================
    # STOP LOSS
    # ==========================

    def calculate_stop_loss(

        self,

        entry_price

    ):


        return round(

            entry_price

            *

            (

                1

                -

                self.stop_loss_percent / 100

            ),

            2

        )







    # ==========================
    # TAKE PROFIT
    # ==========================

    def calculate_take_profit(

        self,

        entry_price

    ):


        return round(

            entry_price

            *

            (

                1

                +

                self.take_profit_percent / 100

            ),

            2

        )







    # ==========================
    # CHECK POSITION
    # ==========================

    def allowed_trade(

        self,

        amount

    ):


        if amount <= 0:


            return False



        if amount > self.balance:


            return False




        return True







    # ==========================
    # UPDATE BALANCE
    # ==========================

    def update_balance(

        self,

        value

    ):


        self.balance += value






    # ==========================
    # STATUS
    # ==========================

    def get_status(self):


        return {


            "balance":

            self.balance,


            "trade_size":

            self.get_trade_amount(),


            "stop_loss":

            self.stop_loss_percent,


            "take_profit":

            self.take_profit_percent


        }