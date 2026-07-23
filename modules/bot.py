import threading
import time

from modules.logger import TradingLogger



class TradingBot:


    def __init__(
        self,
        strategy,
        trader,
        risk
    ):


        self.strategy = strategy

        self.trader = trader

        self.risk = risk


        self.logger = TradingLogger()


        self.running = False

        self.thread = None


        self.last_signal = "WAIT"





    # ==========================
    # START BOT
    # ==========================

    def start(
        self,
        get_candles,
        status_callback=None
    ):


        if self.running:

            self.logger.info(
                "Bot läuft bereits"
            )

            return



        self.running = True



        self.logger.info(
            "🟢 Trading gestartet"
        )



        self.thread = threading.Thread(

            target=self.loop,

            args=(

                get_candles,

                status_callback

            )

        )


        self.thread.daemon = True


        self.thread.start()





    # ==========================
    # MAIN LOOP
    # ==========================

    def loop(
        self,
        get_candles,
        status_callback
    ):


        while self.running:


            try:


                candles = get_candles()



                if len(candles) < 50:


                    self.logger.info(

                        "Warte auf genügend Candles"

                    )

                    time.sleep(60)

                    continue




                signal = self.strategy.analyze(

                    candles

                )


                self.last_signal = signal



                price = candles[-1]["close"]



                message = (

                    f"BTC: {price:.2f} | "

                    f"Signal: {signal}"

                )



                self.logger.info(

                    message

                )



                if status_callback:


                    status_callback(

                        signal

                    )





                # BUY

                if signal == "BUY":


                    self.logger.info(

                        "BUY Signal erkannt"

                    )


                    amount = self.risk.max_trade_usdt



                    self.trader.buy(

                        amount

                    )





                # SELL

                elif signal == "SELL":


                    self.logger.info(

                        "SELL Signal erkannt"

                    )





                else:


                    self.logger.info(

                        "Keine Aktion"

                    )





            except Exception as e:


                self.logger.error(

                    str(e)

                )



            # 5 Minuten Candle

            time.sleep(

                300

            )







    # ==========================
    # STOP BOT
    # ==========================

    def stop(self):


        self.running = False


        self.logger.info(

            "🔴 Trading gestoppt"

        )