import sys

from PyQt6.QtWidgets import QApplication

from gui import TradingDashboard


app = QApplication(sys.argv)


window = TradingDashboard()

window.show()


sys.exit(
    app.exec()
)