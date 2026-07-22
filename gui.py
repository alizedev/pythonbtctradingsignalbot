import sys

from PyQt6.QtWidgets import QApplication


class TradingDashboard:
    pass


from gui import TradingDashboard

app = QApplication(sys.argv)

window = TradingDashboard()
window.show()

sys.exit(app.exec())