from modules.logger import TradingLogger




class Trader:


    def __init__(
        self,
        binance,
        paper=True
    ):


        self.binance = binance


        self.paper = paper


        self.logger = TradingLogger()


        self.balance = 500.0


        self.btc_amount = 0.0





    # ==========================
    # BUY
    # ==========================

    def buy(
        self,
        usdt_amount
    ):


        try:



            price = self.binance.get_btc_price()



            btc = (

                usdt_amount

                /

                price

            )




            # PAPER MODE

            if self.paper:



                self.balance -= usdt_amount


                self.btc_amount += btc



                self.logger.info(

                    f"PAPER BUY | "

                    f"{btc:.6f} BTC "

                    f"@ {price:.2f}"

                )


                return {

                    "mode":

                    "paper",


                    "side":

                    "BUY",


                    "price":

                    price,


                    "btc":

                    btc

                }





            # LIVE BINANCE

            order = self.binance.client.order_market_buy(

                symbol="BTCUSDT",

                quoteOrderQty=usdt_amount

            )


            self.logger.info(

                "LIVE BUY ausgeführt"

            )


            return order





        except Exception as e:


            self.logger.error(

                f"BUY ERROR: {e}"

            )


            return None






    # ==========================
    # SELL
    # ==========================

    def sell(
        self,
        btc_amount
    ):


        try:



            price = self.binance.get_btc_price()



            if self.paper:



                usdt = (

                    btc_amount

                    *

                    price

                )



                self.balance += usdt


                self.btc_amount -= btc_amount



                self.logger.info(

                    f"PAPER SELL | "

                    f"{btc_amount:.6f} BTC "

                    f"@ {price:.2f}"

                )



                return {

                    "mode":

                    "paper",


                    "side":

                    "SELL",


                    "price":

                    price

                }





            order = self.binance.client.order_market_sell(

                symbol="BTCUSDT",

                quantity=btc_amount

            )



            self.logger.info(

                "LIVE SELL ausgeführt"

            )



            return order





        except Exception as e:


            self.logger.error(

                f"SELL ERROR: {e}"

            )


            return None





    # ==========================
    # STATUS
    # ==========================

    def get_status(self):


        return {


            "balance":

            self.balance,


            "btc":

            self.btc_amount,


            "paper":

            self.paper

        }