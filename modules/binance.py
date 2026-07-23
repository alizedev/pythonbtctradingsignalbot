from binance.client import Client
from binance import ThreadedWebsocketManager



class BinanceModule:


    def __init__(self):

        self.client = Client()

        self.ws_manager = None

        self.callback = None




    def get_btc_price(self):

        try:

            ticker = self.client.get_symbol_ticker(

                symbol="BTCUSDT"

            )


            return float(
                ticker["price"]
            )


        except Exception as e:


            print(
                "Price Error:",
                e
            )


            return 0





    def load_candles(self):


        candles = self.client.get_klines(

            symbol="BTCUSDT",

            interval=Client.KLINE_INTERVAL_5MINUTE,

            limit=100

        )



        result = []



        for c in candles:


            result.append(

                {

                    "time": c[0],

                    "open": float(c[1]),

                    "high": float(c[2]),

                    "low": float(c[3]),

                    "close": float(c[4])

                }

            )



        return result





    def start_live_candles(self, callback):


        self.callback = callback



        self.ws_manager = ThreadedWebsocketManager()



        self.ws_manager.start()




        def handle_message(msg):


            try:


                if msg.get("e") != "kline":

                    return



                k = msg["k"]



                candle = {


                    "time":

                    k["t"],


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



            except Exception as e:


                print(

                    "Websocket Error:",

                    e

                )





        self.ws_manager.start_kline_socket(

            callback=handle_message,

            symbol="BTCUSDT",

            interval="5m"

        )





    def stop_websocket(self):


        if self.ws_manager:


            self.ws_manager.stop()



    def get_trades(self):


        try:


            return self.client.get_my_trades(

                symbol="BTCUSDT"

            )


        except:


            return []