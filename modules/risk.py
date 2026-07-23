class RiskManager:


    def __init__(self):

        self.max_trade_usdt = 10

        self.stop_loss = 0.02

        self.take_profit = 0.04



    def calculate_amount(self, balance):

        if balance < self.max_trade_usdt:

            return balance


        return self.max_trade_usdt



    def check_exit(
        self,
        entry,
        current
    ):


        change = (
            current-entry
        ) / entry



        if change <= -self.stop_loss:

            return "STOP_LOSS"



        if change >= self.take_profit:

            return "TAKE_PROFIT"



        return "HOLD"