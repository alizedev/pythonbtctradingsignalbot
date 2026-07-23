import statistics


class Strategy:


    def __init__(self):

        self.last_signal = "WAIT"



    def analyze(
            self,
            candles
    ):


        if len(candles) < 20:

            return "WAIT"



        closes = [

            c["close"]

            for c in candles

        ]



        price = closes[-1]



        avg = statistics.mean(
            closes[-20:]
        )



        # günstig gekauft

        if price < avg * 0.985:


            self.last_signal = "BUY"

            return "BUY"



        # teuer verkaufen

        elif price > avg * 1.015:


            self.last_signal = "SELL"

            return "SELL"



        return "WAIT"