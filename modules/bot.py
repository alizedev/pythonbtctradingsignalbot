import threading
import time


from modules.signal_scanner import SignalScanner
from modules.trader import Trader



class TradingBot:



    def __init__(
            self,
            binance
    ):


        self.binance = binance


        self.scanner = SignalScanner()


        self.trader = Trader(

            binance

        )


        self.candles = []


        self.running = False





    def update_candles(
            self,
            candles
    ):


        self.candles = candles


        print(

            "BOT CANDLES:",

            len(candles)

        )



        if len(candles) >= 20:


            signal = self.scanner.scan(

                candles

            )


            self.trader.execute_signal(

                signal

            )







    def start(
            self
    ):


        if self.running:

            return



        self.running = True



        self.binance.start_live_candles(

            self.update_candles

        )



        thread = threading.Thread(

            target=self.monitor,

            daemon=True

        )


        thread.start()



        print(

            "🟢 Trading Bot gestartet"

        )







    def monitor(
            self
    ):


        while self.running:


            try:


                price = self.binance.get_price()



                print(

                    "BTC PRICE:",

                    price

                )



            except Exception as e:


                print(

                    "Monitor Fehler:",

                    e

                )



            time.sleep(10)







    def stop(
            self
    ):


        self.running = False


        print(

            "🔴 Trading Bot gestoppt"

        )