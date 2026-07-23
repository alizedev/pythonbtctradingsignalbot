class SignalService:


    def calculate_signal(
        self,
        price,
        ema
    ):

        if price > ema:
            return "BUY"

        elif price < ema:
            return "SELL"

        else:
            return "HOLD"