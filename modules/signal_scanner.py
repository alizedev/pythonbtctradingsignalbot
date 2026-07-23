import statistics



class SignalScanner:


    def __init__(self):

        self.last_signal = "HOLD"



    def calculate_ema(
            self,
            prices,
            period=20
    ):


        if len(prices) < period:

            return None



        multiplier = (
            2 /
            (period + 1)
        )


        ema = prices[0]



        for price in prices[1:]:

            ema = (

                (price - ema)
                *
                multiplier

            ) + ema



        return ema





    def calculate_rsi(
            self,
            prices,
            period=14
    ):


        if len(prices) <= period:

            return 50



        gains = []

        losses = []



        for i in range(
            1,
            len(prices)
        ):


            diff = (

                prices[i]
                -
                prices[i-1]

            )



            if diff >= 0:

                gains.append(
                    diff
                )

                losses.append(
                    0
                )


            else:

                gains.append(
                    0
                )

                losses.append(
                    abs(diff)
                )



        avg_gain = statistics.mean(

            gains[-period:]

        )


        avg_loss = statistics.mean(

            losses[-period:]

        )



        if avg_loss == 0:

            return 100



        rs = (

            avg_gain /
            avg_loss

        )


        rsi = (

            100 -
            (
                100 /
                (1 + rs)
            )

        )


        return rsi





    def scan(
            self,
            candles
    ):


        if not candles or len(candles) < 20:

            return {

                "signal": "WAIT",

                "confidence": 0

            }



        closes = [

            c["close"]

            for c in candles

        ]



        price = closes[-1]



        ema = self.calculate_ema(
            closes,
            20
        )


        rsi = self.calculate_rsi(
            closes
        )



        confidence = 50



        signal = "HOLD"



        # Oversold + Trend

        if (

            rsi < 35

            and

            price > ema

        ):


            signal = "BUY"

            confidence += 20



        # Overbought

        elif (

            rsi > 70

        ):


            signal = "SELL"

            confidence += 20



        else:


            signal = "HOLD"



        result = {


            "signal":

            signal,


            "price":

            price,


            "rsi":

            round(
                rsi,
                2
            ),


            "ema":

            round(
                ema,
                2
            ),


            "confidence":

            min(
                confidence,
                100
            )

        }



        self.last_signal = signal



        print(
            "SIGNAL:",
            result
        )



        return result