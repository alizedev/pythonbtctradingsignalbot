# gui.py

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QApplication
)

from PyQt6.QtCore import Qt


from binance_api import get_price
from wallet import create_wallet



class Dashboard(QWidget):


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

        QWidget {

            background-color:#111827;
            color:white;
            font-size:20px;

        }


        QPushButton {

            background:#2563eb;
            padding:15px;
            border-radius:10px;

        }


        """)


        layout = QVBoxLayout()


        self.title = QLabel(
            "₿ BTC AI SIGNAL TRACKER"
        )


        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        self.price = QLabel()


        self.wallet = QLabel()


        self.btc = QLabel()


        self.signal = QLabel(
            "Signal: WAIT ⚪"
        )


        self.refresh = QPushButton(
            "Refresh"
        )


        self.refresh.clicked.connect(
            self.update_data
        )



        layout.addWidget(
            self.title
        )


        layout.addWidget(
            self.price
        )


        layout.addWidget(
            self.wallet
        )


        layout.addWidget(
            self.btc
        )


        layout.addWidget(
            self.signal
        )


        layout.addWidget(
            self.refresh
        )


        self.setLayout(
            layout
        )


        self.update_data()



    def update_data(self):


        price = get_price()


        wallet = create_wallet(
            price
        )


        self.price.setText(
            f"BTC Price: ${price:,.2f}"
        )


        self.wallet.setText(
            f"Wallet: ${wallet.usd:,.2f}"
        )


        self.btc.setText(
            f"BTC Holdings: {wallet.btc:.8f} BTC"
        )


