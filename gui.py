from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton
)

from PyQt6.QtCore import Qt


class TradingDashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "BTC AI Signal Tracker"
        )

        self.setGeometry(
            300,
            200,
            600,
            500
        )


        self.setStyleSheet("""
        QWidget{
            background:#111827;
            color:white;
            font-size:18px;
        }

        QPushButton{
            background:#2563eb;
            padding:12px;
            border-radius:10px;
        }

        QLabel{
            padding:10px;
        }
        """)


        layout = QVBoxLayout()


        self.price = QLabel(
            "BTC Price: Loading..."
        )

        self.signal = QLabel(
            "Signal: WAIT"
        )

        self.confidence = QLabel(
            "Confidence: 0%"
        )


        self.button = QPushButton(
            "Refresh Signal"
        )


        layout.addWidget(
            self.price
        )

        layout.addWidget(
            self.signal
        )

        layout.addWidget(
            self.confidence
        )

        layout.addWidget(
            self.button
        )


        self.setLayout(
            layout
        )

