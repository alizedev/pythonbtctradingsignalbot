import json
import threading

import websocket

from binance.client import Client

from modules.config import load_config


class BinanceModule:

    def __init__(self):

        self.config = load_config()

        self.client = None

        self.callback = None

        self.connect()

    def connect(self):

        try:

            api_key = self.config.get("api_key", "")

            api_secret = self.config.get("api_secret", "")

            if api_key and api_secret:

                self.client = Client(api_key, api_secret)

                print("✅ Binance API geladen")

            else:

                self.client = Client()

                print("⚠ Binance Public API geladen")

        except Exception as e:

            print("Binance Verbindung Fehler:", e)

            self.client = Client()

    def get_price(self):

        try:

            data = self.client.get_symbol_ticker(symbol="BTCUSDT")

            return float(data["price"])

        except Exception as e:

            print("Preis Fehler:", e)

            return 0

    def get_candles(self, limit=50):

        try:

            data = self.client.get_klines(
                symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_5MINUTE, limit=limit
            )

            candles = []

            for c in data:

                candles.append(
                    {
                        "time": c[0],
                        "open": float(c[1]),
                        "high": float(c[2]),
                        "low": float(c[3]),
                        "close": float(c[4]),
                        "volume": float(c[5]),
                    }
                )

            print("BINANCE CANDLES:", len(candles))

            return candles

        except Exception as e:

            print("Candle Fehler:", e)

            return []

    def start_live_candles(self, callback):

        self.callback = callback

        candles = self.get_candles(50)

        if candles:

            callback(candles)

        def on_message(ws, message):

            try:

                data = json.loads(message)

                k = data["k"]

                live = {
                    "time": k["t"],
                    "open": float(k["o"]),
                    "high": float(k["h"]),
                    "low": float(k["l"]),
                    "close": float(k["c"]),
                    "volume": float(k["v"]),
                }

                candles[-1] = live

                if self.callback:

                    self.callback(candles)

                print("LIVE BTC:", live["close"])

            except Exception as e:

                print("Websocket Fehler:", e)

        socket = "wss://stream.binance.com:9443/ws/" "btcusdt@kline_5m"

        ws = websocket.WebSocketApp(socket, on_message=on_message)

        thread = threading.Thread(target=ws.run_forever, daemon=True)

        thread.start()

        print("🟢 Binance BTCUSDT 5m Live gestartet")

    def buy_market(self, quantity):

        if not self.config.get("live_trading", False):

            print("PAPER BUY:", quantity)

            return None

        order = self.client.create_order(
            symbol="BTCUSDT", side="BUY", type="MARKET", quantity=quantity
        )

        return order

    def sell_market(self, quantity):

        if not self.config.get("live_trading", False):

            print("PAPER SELL:", quantity)

            return None

        order = self.client.create_order(
            symbol="BTCUSDT", side="SELL", type="MARKET", quantity=quantity
        )

        return order
