import json
import os

from binance.client import Client



class BinanceModule:


    def __init__(self):

        self.client = None

        self.load_api()



    def load_api(self):

        try:

            path = "data/binance.json"


            if not os.path.exists(path):

                print(
                    "⚠ No Binance API"
                )

                return



            with open(path, "r") as f:

                data = json.load(f)



            self.client = Client(

                data["api_key"],

                data["secret_key"]

            )


            print(
                "✅ Binance connected"
            )


        except Exception as e:

            print(
                "Binance error:",
                e
            )



    def get_btc_price(self):

        if not self.client:

            return 0


        try:

            ticker = self.client.get_symbol_ticker(

                symbol="BTCUSDT"

            )


            return float(
                ticker["price"]
            )


        except:

            return 0