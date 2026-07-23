import threading
import time



class LivePrice:


    def __init__(

        self,

        binance

    ):


        self.binance = binance


        self.price = 0.0


        self.running = False


        self.thread = None




    # ==========================
    # START
    # ==========================

    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )


        self.thread.start()



        print(

            "🟢 Live BTC Preis gestartet"

        )






    # ==========================
    # LOOP
    # ==========================

    def loop(self):


        while self.running:


            try:


                self.price = (

                    self.binance.get_btc_price()

                )


                print(

                    f"BTC Live: ${self.price:,.2f}"

                )



            except Exception as e:


                print(

                    "Live Preis Fehler:",

                    e

                )



            time.sleep(2)








    # ==========================
    # GET PRICE
    # ==========================

    def get_price(self):


        return self.price






    # ==========================
    # STOP
    # ==========================

    def stop(self):


        self.running = False