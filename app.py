import sys

from PyQt6.QtWidgets import QApplication

from gui import Dashboard



class TradingBotApp:


    def __init__(self):

        self.app = QApplication(sys.argv)

        self.window = Dashboard()

        self.window.show()



    def run(self):

        sys.exit(
            self.app.exec()
        )



if __name__ == "__main__":

    app = TradingBotApp()

    app.run()