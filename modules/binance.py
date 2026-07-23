import os
import json
import threading

import websocket

from binance.client import Client
from binance.exceptions import BinanceAPIException

from modules.logger import TradingLogger



class BinanceModule:


    def __init__(self):

        self.client = None

        self.logger = TradingLogger()

        self.connected = False

        self.websocket = None

        self.load_api()



    # ==========================
    # LOAD API
    # ==========================

    def load_api(self):

        file = "data/binance.json"


        if not os.path.exists(file):

            self.logger.warning(
                "⚠ Keine Binance API gefunden"
            )

            return



        try:

            with open(
                file,
                "r"
            ) as f:

                data = json.load(f)



            api_key = data.get(
                "key"
            )

            secret = data.get(
                "secret"
            )



            if not api_key or not secret:

                self.logger.error(
                    "API Key oder Secret fehlt"
                )

                return

            self.client = Client(
                api_key,
                secret
            )

            self.client.API_URL = (
                "https://api.binance.com/api"
            )

            server_time = self.client.get_server_time()

            print(
                "Binance Server Time:",
                server_time
            )

            self.connected = True


            self.logger.info(
                "✅ Binance API loaded"
            )



        except Exception as e:

            self.logger.error(
                f"API Fehler: {e}"
            )



    # ==========================
    # BTC PRICE
    # ==========================

    def get_btc_price(self):

        try:

            if not self.client:

                return 0.0



            ticker = self.client.get_symbol_ticker(

                symbol="BTCUSDT"

            )


            return float(
                ticker["price"]
            )



        except Exception as e:


            self.logger.error(
                f"Preis Fehler: {e}"
            )


            return 0.0





    # ==========================
    # HISTORICAL CANDLES
    # ==========================

    def get_candles(
        self,
        limit=200
    ):


        try:


            candles = self.client.get_klines(

                symbol="BTCUSDT",

                interval=Client.KLINE_INTERVAL_5MINUTE,

                limit=limit

            )



            result = []



            for c in candles:


                result.append({

                    "time": c[0],

                    "open": float(c[1]),

                    "high": float(c[2]),

                    "low": float(c[3]),

                    "close": float(c[4]),

                    "volume": float(c[5])

                })



            return result



        except BinanceAPIException as e:


            self.logger.error(

                f"Binance Fehler: {e}"

            )


            return []



        except Exception as e:


            self.logger.error(

                f"Candle Fehler: {e}"

            )


            return []





    # ==========================
    # CHART LOAD
    # ==========================

    def load_candles(self):

        return self.get_candles(
            100
        )





    # ==========================
    # LIVE 5M CANDLES
    # ==========================

    def start_live_candles(
        self,
        callback
    ):


        def run():


            url = (

                "wss://stream.binance.com:9443/ws/"

                "btcusdt@kline_5m"

            )



            def on_message(
                ws,
                message
            ):


                try:


                    data = json.loads(

                        message

                    )


                    kline = data["k"]



                    candle = {


                        "time":

                        kline["t"],


                        "open":

                        float(
                            kline["o"]
                        ),


                        "high":

                        float(
                            kline["h"]
                        ),


                        "low":

                        float(
                            kline["l"]
                        ),


                        "close":

                        float(
                            kline["c"]
                        ),


                        "volume":

                        float(
                            kline["v"]
                        )

                    }



                    callback(
                        candle
                    )



                except Exception as e:


                    self.logger.error(

                        f"Websocket Daten Fehler: {e}"

                    )





            def on_error(
                ws,
                error
            ):


                self.logger.error(

                    f"Websocket Error: {error}"

                )





            def on_close(
                ws,
                code,
                msg
            ):


                self.logger.warning(

                    "Websocket geschlossen"

                )





            def on_open(
                ws
            ):


                self.logger.info(

                    "🟢 Binance Live Candle verbunden"

                )





            self.websocket = websocket.WebSocketApp(

                url,

                on_message=on_message,

                on_error=on_error,

                on_close=on_close,

                on_open=on_open

            )



            self.websocket.run_forever()






        thread = threading.Thread(

            target=run

        )


        thread.daemon = True


        thread.start()





    # ==========================
    # STOP WEBSOCKET
    # ==========================

    def stop_websocket(self):


        try:


            if self.websocket:


                self.websocket.close()



                self.logger.info(

                    "Websocket beendet"

                )



        except Exception as e:


            self.logger.error(

                str(e)

            )