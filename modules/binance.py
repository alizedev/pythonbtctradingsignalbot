import json
import os

from binance.client import Client
from binance import ThreadedWebsocketManager



class BinanceModule:


    def __init__(self):

        self.client = None

        self.ws_manager = None

        self.callback = None

        self.load_api()



    # ==========================
    # API LOAD
    # ==========================

    def load_api(self):

        try:

            if os.path.exists(
                "data/binance.json"
            ):


                with open(
                    "data/binance.json",
                    "r"
                ) as file:


                    data = json.load(file)



                self.client = Client(

                    data["key"],

                    data["secret"]

                )


                print(
                    "✅ Binance API loaded"
                )


            else:


                self.client = Client()


                print(
                    "⚠ Public Binance Mode"
                )


        except Exception as e:


            print(
                "API Error:",
                e
            )


            self.client = Client()




    # ==========================
    # PRICE
    # ==========================

    def get_btc_price(self):

        ticker = self.client.get_symbol_ticker(

            symbol="BTCUSDT"

        )

        return float(
            ticker["price"]
        )




    # ==========================
    # CANDLES
    # ==========================

    def load_candles(self):


        candles = self.client.get_klines(

            symbol="BTCUSDT",

            interval="5m",

            limit=100

        )


        result=[]


        for c in candles:


            result.append(

                {

                "open":
                float(c[1]),

                "high":
                float(c[2]),

                "low":
                float(c[3]),

                "close":
                float(c[4])

                }

            )


        return result





    # ==========================
    # LIVE STREAM
    # ==========================

    def start_live_candles(
        self,
        callback
    ):


        self.callback = callback


        self.ws_manager = ThreadedWebsocketManager()


        self.ws_manager.start()



        def handler(msg):


            if msg.get("e") != "kline":

                return



            k = msg["k"]


            candle = {


            "open":
            float(k["o"]),


            "high":
            float(k["h"]),


            "low":
            float(k["l"]),


            "close":
            float(k["c"])

            }



            if self.callback:

                self.callback(
                    candle
                )



        self.ws_manager.start_kline_socket(

            callback=handler,

            symbol="BTCUSDT",

            interval="5m"

        )





    def stop_websocket(self):

        if self.ws_manager:

            self.ws_manager.stop()

    # ==========================
    # LOAD BINANCE TRADES
    # ==========================

    def get_trades(self):


        try:

            if self.client is None:

                return []


            trades = self.client.get_my_trades(

                symbol="BTCUSDT"

            )


            return trades



        except Exception as e:


            print(

                "Trade Load Error:",

                e

            )


            return []
    def stop_websocket(self):

        if self.ws_manager:

            self.ws_manager.stop()



    def get_trades(self):

        try:

            return self.client.get_my_trades(
                symbol="BTCUSDT"
            )

        except Exception as e:

            print(e)

            return []