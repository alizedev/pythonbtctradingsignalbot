import json
import os

from datetime import datetime



class Trader:


    def __init__(self, binance):


        self.binance = binance


        # ==========================
        # SICHERHEIT
        # ==========================

        self.PAPER_MODE = False


        # maximale Trade Größe

        self.max_trade_usdt = 10




        # Paper Guthaben

        self.usdt_balance = 500.0

        self.btc_amount = 0.0



        self.trades_file = "trades.json"






    # ==========================
    # BUY
    # ==========================

    def buy(self, amount):


        if amount > self.max_trade_usdt:


            amount = self.max_trade_usdt




        price = self.binance.get_btc_price()



        if price <= 0:

            return None




        btc_quantity = amount / price






        # ======================
        # LIVE BINANCE
        # ======================

        if not self.PAPER_MODE:


            try:


                order = self.binance.client.create_order(


                    symbol="BTCUSDT",


                    side="BUY",


                    type="MARKET",


                    quoteOrderQty=amount


                )



                trade = {


                    "mode":"LIVE",


                    "order":order


                }



            except Exception as e:


                print(

                    "BUY Fehler:",

                    e

                )


                return None




        # ======================
        # PAPER
        # ======================

        else:


            if amount > self.usdt_balance:


                return None



            self.usdt_balance -= amount


            self.btc_amount += btc_quantity



            trade = {


                "mode":"PAPER",


                "coin":"BTC",


                "side":"BUY",


                "price":price,


                "amount":btc_quantity,


                "value":amount,


                "time":datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                )

            }




        self.save_trade(trade)



        return trade







    # ==========================
    # SELL
    # ==========================

    def sell(self, amount_btc):


        price = self.binance.get_btc_price()



        if price <= 0:

            return None






        if not self.PAPER_MODE:


            try:


                order = self.binance.client.create_order(


                    symbol="BTCUSDT",


                    side="SELL",


                    type="MARKET",


                    quantity=amount_btc


                )



                trade = {


                    "mode":"LIVE",


                    "order":order


                }



            except Exception as e:


                print(

                    "SELL Fehler:",

                    e

                )


                return None





        else:


            value = amount_btc * price



            self.btc_amount -= amount_btc


            self.usdt_balance += value




            trade = {


                "mode":"PAPER",


                "coin":"BTC",


                "side":"SELL",


                "price":price,


                "amount":amount_btc,


                "value":value,


                "time":datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                )

            }





        self.save_trade(trade)



        return trade






    # ==========================
    # SAVE HISTORY
    # ==========================

    def save_trade(self, trade):


        trades=[]



        if os.path.exists(self.trades_file):


            try:


                with open(

                    self.trades_file,

                    "r"

                ) as f:


                    trades=json.load(f)



            except:


                trades=[]






        trades.append(trade)






        with open(

            self.trades_file,

            "w"

        ) as f:


            json.dump(

                trades,

                f,

                indent=4

            )







    # ==========================
    # STATUS
    # ==========================

    def status(self):


        return {


            "paper":

            self.PAPER_MODE,


            "USDT":

            self.usdt_balance,


            "BTC":

            self.btc_amount


        }