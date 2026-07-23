import sys

from PyQt6.QtWidgets import QApplication

from gui import Dashboard


class TradingBotApp:
    """
    Hauptanwendung für den BTC Trading Signal Bot
    """

    def __init__(self):

        self.app = QApplication(
            sys.argv
        )

        self.window = Dashboard()


    def start(self):

        self.window.show()

        sys.exit(
            self.app.exec()
        )



if __name__ == "__main__":

    application = TradingBotApp()

    application.start()