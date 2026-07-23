import pandas as pd


class Strategy:


    def __init__(self):

        self.last_score = 0




    # ==========================
    # ANALYSE
    # ==========================

    def analyze(self, candles):


        if len(candles) < 50:

            return "WAIT"



        df = pd.DataFrame(candles)



        score = 0




        # EMA

        df["ema20"] = (

            df["close"]

            .ewm(span=20)

            .mean()

        )


        df["ema50"] = (

            df["close"]

            .ewm(span=50)

            .mean()

        )



        if df.iloc[-1]["ema20"] > df.iloc[-1]["ema50"]:

            score += 30




        # RSI

        delta = df["close"].diff()


        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)



        avg_gain = gain.rolling(14).mean()

        avg_loss = loss.rolling(14).mean()



        rs = avg_gain / avg_loss


        df["rsi"] = 100 - (

            100 / (1 + rs)

        )



        rsi = df.iloc[-1]["rsi"]



        if rsi < 40:

            score += 20


        elif rsi > 70:

            score -= 20






        # MACD

        ema12 = (

            df["close"]

            .ewm(span=12)

            .mean()

        )


        ema26 = (

            df["close"]

            .ewm(span=26)

            .mean()

        )



        macd = ema12 - ema26



        if macd.iloc[-1] > 0:

            score += 20






        # Volume

        avg_volume = (

            df["volume"]

            .rolling(20)

            .mean()

        )


        if df.iloc[-1]["volume"] > avg_volume.iloc[-1]:

            score += 15






        # Candle Richtung

        if (

            df.iloc[-1]["close"]

            >

            df.iloc[-1]["open"]

        ):

            score += 15





        self.last_score = score





        if score >= 80:

            return "BUY"



        elif score <= 20:

            return "SELL"



        else:

            return "WAIT"





    # ==========================
    # SCORE
    # ==========================

    def get_score(self):

        return self.last_score