import threading
import time


from modules.signal_scanner import SignalScanner
from modules.trader import Trader


try:
    from modules.signal_provider import SignalProvider

    HAS_PROVIDER = True

except ImportError:

    HAS_PROVIDER = False


class TradingBot:

    def __init__(self, binance):

        self.binance = binance

        self.scanner = SignalScanner()

        self.trader = Trader(binance)

        self.candles = []

        self.running = False

        # externe Signale / Copy Trading

        if HAS_PROVIDER:

            self.provider = SignalProvider()

        else:

            self.provider = None

    def update_candles(self, candles):

        self.candles = candles

        print("📈 BOT CANDLES:", len(candles))

        if len(candles) < 25:

            return

        # eigene Analyse

        local_signal = self.scanner.scan(candles)

        print("🤖 LOCAL SIGNAL:", local_signal)

        # externes Copy Signal

        external_signal = None

        if self.provider:

            try:

                external_signal = self.provider.get_signal()

                print("👑 COPY SIGNAL:", external_signal)

            except Exception as e:

                print("Signal Provider Fehler:", e)

        final_signal = self.combine_signals(local_signal, external_signal)

        self.trader.execute_signal(final_signal)

    def combine_signals(self, local, external):

        # kein externes Signal

        if not external:

            return local

        score = 0

        signal = "HOLD"

        # gleiche Richtung = stärker

        if local["signal"] == external["signal"]:

            signal = local["signal"]

            score = (local["confidence"] + external.get("confidence", 0)) / 2

            score += 15

        else:

            signal = external["signal"]

            score = external.get("confidence", 50)

        return {
            "signal": signal,
            "price": local["price"],
            "confidence": min(int(score), 100),
            "source": "COPY+AI",
        }

    def start(self):

        if self.running:

            return

        self.running = True

        self.binance.start_live_candles(self.update_candles)

        thread = threading.Thread(target=self.monitor, daemon=True)

        thread.start()

        print("🟢 Trading Bot gestartet")

    def monitor(self):

        while self.running:

            try:

                price = self.binance.get_price()

                print("💰 BTC LIVE:", price)

                # Stop Loss / Take Profit prüfen

                self.trader.check_risk(price)

            except Exception as e:

                print("Monitor Fehler:", e)

            time.sleep(10)

    def stop(self):

        self.running = False

        print("🔴 Bot gestoppt")
