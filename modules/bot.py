import threading
import time



class TradingBot:


    def __init__(

        self,

        binance,

        strategy,

        trader,

        risk

    ):


        self.binance = binance

        self.strategy = strategy

        self.trader = trader

        self.risk = risk



        self.running = False

        self.auto_trade = False



        self.thread = None



        self.callback = None



        self.last_signal = "WAIT"





    # ==========================
    # START
    # ==========================

    def start(

        self,

        callback=None

    ):


        if self.running:


            return



        self.running = True


        self.callback = callback




        self.thread = threading.Thread(

            target=self.loop

        )


        self.thread.daemon = True


        self.thread.start()



        print(

            "🟢 Trading Bot gestartet"

        )







    # ==========================
    # MAIN LOOP
    # ==========================

    def loop(self):


        while self.running:


            try:



                candles = self.binance.get_candles(

                    200

                )




                if len(candles) < 50:


                    print(

                        "Keine Daten"

                    )


                    time.sleep(60)

                    continue






                signal = self.strategy.analyze(

                    candles

                )



                score = self.strategy.get_score()



                price = candles[-1]["close"]



                self.last_signal = signal




                message = (

                    f"BTC ${price:,.2f} "

                    f"| Signal {signal} "

                    f"| Score {score}/100"

                )



                print(message)





                if self.callback:


                    self.callback(

                        signal

                    )






                # =====================
                # AUTO TRADING
                # =====================


                if self.auto_trade:



                    if signal == "BUY" and score >= 80:


                        self.buy_trade()





                    elif signal == "SELL" and score <= 20:


                        self.sell_trade()






            except Exception as e:



                print(

                    f"Bot Fehler: {e}"

                )







            # 5 Minuten

            time.sleep(

                300

            )








    # ==========================
    # BUY
    # ==========================

    def buy_trade(self):


        amount = self.risk.get_trade_amount()



        if not self.risk.allowed_trade(

            amount

        ):


            return




        trade = self.trader.buy(

            amount

        )



        if trade:


            print(

                "🟢 BUY ausgeführt"

            )







    # ==========================
    # SELL
    # ==========================

    def sell_trade(self):


        if self.trader.btc_amount <= 0:


            return




        trade = self.trader.sell(

            self.trader.btc_amount

        )



        if trade:


            print(

                "🔴 SELL ausgeführt"

            )







    # ==========================
    # AUTO TRADE ON
    # ==========================

    def enable_auto_trade(self):


        self.auto_trade = True



        print(

            "⚡ Auto Trading aktiviert"

        )






    # ==========================
    # AUTO TRADE OFF
    # ==========================

    def disable_auto_trade(self):


        self.auto_trade = False



        print(

            "⛔ Auto Trading deaktiviert"

        )







    # ==========================
    # STOP
    # ==========================

    def stop(self):


        self.running = False



        print(

            "🔴 Trading Bot gestoppt"

        )