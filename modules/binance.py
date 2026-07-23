from binance.client import Client



class BinanceModule:


    def __init__(self):

        self.client = Client()



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





    def get_candles(self):


        try:


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



        except Exception as e:


            print(

                "Candle Error:",

                e

            )


            return []




    def get_trades(self):


        try:

            return self.client.get_my_trades(

                symbol="BTCUSDT"

            )


        except:


            return []