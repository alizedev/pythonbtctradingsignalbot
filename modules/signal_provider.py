import time
import random


class SignalProvider:

    def __init__(self):

        self.last_signal = "HOLD"

        self.last_time = 0

    def get_signal(self):
        """
        Externer Signal Provider

        Rückgabe:

        BUY
        SELL
        HOLD

        mit Confidence Score

        """

        # Abstand zwischen Signalen

        if time.time() - self.last_time < 60:

            return {"signal": "HOLD", "confidence": 0, "source": "COPY_TRADING"}

        self.last_time = time.time()

        # TEST SIGNAL
        #
        # Später ersetzen durch:
        #
        # TradingView Webhook
        # Telegram Bot
        # Binance Copy Trading API
        #

        signals = ["BUY", "SELL", "HOLD"]

        signal = random.choice(signals)

        confidence = random.randint(45, 95)

        self.last_signal = signal

        return {
            "signal": signal,
            "confidence": confidence,
            "source": "TOP_TRADER_SIMULATION",
        }
