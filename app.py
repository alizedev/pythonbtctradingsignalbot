import sys

from PyQt6.QtWidgets import QApplication

from gui import Dashboard

from modules.binance import BinanceModule

from modules.bot import TradingBot




class TradingBotApp:



    def __init__(self):


        self.binance = BinanceModule()


        self.bot = TradingBot(

            self.binance

        )


        self.window = Dashboard(

            self.binance,

            self.bot

        )



        self.window.show()



        self.bot.start()





if __name__ == "__main__":



    app = QApplication(

        sys.argv

    )



    program = TradingBotApp()



    sys.exit(

        app.exec()

    )