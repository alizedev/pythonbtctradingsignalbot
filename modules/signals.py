import config



class SignalModule:
    """
    Trading Signal Engine

    Erzeugt:

    BUY
    SELL
    HOLD

    Strategien:

    - EMA Trend
    - RSI
    - MACD Vorbereitung

    """



    def __init__(self):

        self.enabled = getattr(
            config,
            "SIGNAL_ENGINE_ENABLED",
            True
        )


        self.rsi_buy = getattr(
            config,
            "RSI_BUY_LEVEL",
            30
        )


        self.rsi_sell = getattr(
            config,
            "RSI_SELL_LEVEL",
            70
        )



    # =========================
    # MAIN SIGNAL
    # =========================


    def generate_signal(
        self,
        candles
    ):


        if not self.enabled:

            return {

                "signal":
                "DISABLED"

            }



        if len(candles) < 20:

            return {

                "signal":
                "HOLD",

                "reason":
                "Not enough data"

            }



        prices = [

            candle["close"]

            for candle in candles

        ]



        ema = self.calculate_ema(
            prices,
            20
        )


        rsi = self.calculate_rsi(
            prices
        )


        current = prices[-1]



        # BUY

        if (

            current > ema

            and

            rsi < self.rsi_sell

        ):

            return {

                "signal":
                "BUY",

                "price":
                current,

                "ema":
                ema,

                "rsi":
                rsi,

                "reason":
                "Uptrend"

            }



        # SELL

        if (

            current < ema

            or

            rsi > self.rsi_sell

        ):

            return {

                "signal":
                "SELL",

                "price":
                current,

                "ema":
                ema,

                "rsi":
                rsi,

                "reason":
                "Weakness"

            }



        return {

            "signal":
            "HOLD",

            "price":
            current,

            "ema":
            ema,

            "rsi":
            rsi,

            "reason":
            "No setup"

        }



    # =========================
    # EMA
    # =========================


    def calculate_ema(
        self,
        prices,
        period
    ):


        if len(prices) < period:

            return prices[-1]


        multiplier = (
            2 /
            (
                period + 1
            )
        )


        ema = prices[0]


        for price in prices[1:]:

            ema = (

                (price - ema)
                *
                multiplier

            ) + ema



        return round(
            ema,
            2
        )



    # =========================
    # RSI
    # =========================


    def calculate_rsi(
        self,
        prices,
        period=14
    ):


        if len(prices) <= period:

            return 50



        gains = 0

        losses = 0



        for i in range(
            1,
            period + 1
        ):

            change = (

                prices[-i]
                -
                prices[-i-1]

            )


            if change > 0:

                gains += change


            else:

                losses += abs(
                    change
                )



        if losses == 0:

            return 100



        rs = (

            gains
            /
            losses

        )


        rsi = (

            100
            -
            (
                100 /
                (
                    1 + rs
                )
            )

        )


        return round(
            rsi,
            2
        )



    # =========================
    # SIMPLE STATUS
    # =========================


    def status(self):

        return {

            "enabled":
            self.enabled,

            "strategy":
            "EMA + RSI"

        }