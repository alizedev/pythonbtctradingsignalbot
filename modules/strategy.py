class Strategy:


    def __init__(self):

        self.last_signal = "WAIT"





    # ==========================
    # SIMPLE EMA
    # ==========================

    def ema(
        self,
        prices,
        period
    ):


        if len(prices) < period:

            return None



        multiplier = 2 / (period + 1)



        ema = prices[0]



        for price in prices[1:]:


            ema = (

                (price - ema)

                *

                multiplier

            ) + ema



        return ema





    # ==========================
    # RSI
    # ==========================

    def rsi(
        self,
        prices,
        period=14
    ):


        if len(prices) <= period:

            return 50



        gains = 0

        losses = 0



        for i in range(

            len(prices)-period,

            len(prices)

        ):


            change = (

                prices[i]

                -

                prices[i-1]

            )



            if change > 0:

                gains += change


            else:

                losses += abs(change)





        if losses == 0:

            return 100



        rs = gains / losses



        return (

            100

            -

            (

                100 /

                (1 + rs)

            )

        )







    # ==========================
    # SIGNAL
    # ==========================

    def analyze(
        self,
        candles
    ):


        if len(candles) < 50:

            return "WAIT"




        prices = [

            c["close"]

            for c in candles

        ]



        price = prices[-1]



        ema20 = self.ema(

            prices[-50:],

            20

        )



        ema50 = self.ema(

            prices,

            50

        )



        rsi = self.rsi(

            prices

        )





        # ==================
        # BUY CONDITIONS
        # ==================

        if (

            price > ema20

            and

            ema20 > ema50

            and

            rsi < 70

        ):


            self.last_signal = "BUY"


            return "BUY"






        # ==================
        # SELL CONDITIONS
        # ==================

        if (

            price < ema20

            and

            ema20 < ema50

            and

            rsi > 30

        ):


            self.last_signal = "SELL"


            return "SELL"






        self.last_signal = "WAIT"


        return "WAIT"