import sys

from PyQt6.QtWidgets import QApplication

from gui import Dashboard


app = QApplication(sys.argv)


window = Dashboard()

window.show()


sys.exit(app.exec())
