import os
import json

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QTabWidget,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from PyQt6.QtCore import Qt, QTimer

from PyQt6.QtGui import QColor, QFont

from modules.binance import BinanceModule



class Dashboard(QWidget):


    def __init__(self):

        super().__init__()


        self.binance = BinanceModule()


        self.setWindowTitle(
            "₿ Bitcoin Trading Bot"
        )


        self.resize(
            1200,
            800
        )


        self.apply_dark_theme()


        self.create_ui()


        self.start_price_timer()



    def apply_dark_theme(self):

        self.setStyleSheet(
            """

            QWidget {

                background:#0d1117;
                color:white;

            }


            QPushButton {

                background:#21262d;
                color:white;
                padding:10px;

            }


            QPushButton:hover {

                background:#238636;

            }


            QLineEdit {

                background:#161b22;
                color:white;

            }


            QTableWidget {

                background:#161b22;
                color:white;

            }

            """
        )



    def create_ui(self):


        layout = QVBoxLayout()


        title = QLabel(
            "₿ Bitcoin Trading Dashboard"
        )


        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        title.setFont(
            QFont(
                "Arial",
                24
            )
        )


        layout.addWidget(
            title
        )


        tabs = QTabWidget()


        tabs.addTab(
            self.dashboard_tab(),
            "📊 Dashboard"
        )


        tabs.addTab(
            self.binance_tab(),
            "🔑 Binance"
        )


        tabs.addTab(
            self.trades_tab(),
            "📜 Trades"
        )


        layout.addWidget(
            tabs
        )


        self.setLayout(
            layout
        )



    def dashboard_tab(self):


        page = QWidget()


        layout = QVBoxLayout()


        self.price_label = QLabel(
            "₿ BTC Price Loading..."
        )


        self.price_label.setFont(
            QFont(
                "Arial",
                20
            )
        )


        self.log_box = QTextEdit()


        self.log_box.setReadOnly(
            True
        )


        layout.addWidget(
            self.price_label
        )


        layout.addWidget(
            self.log_box
        )


        page.setLayout(
            layout
        )


        return page
    # ===============================
    # BINANCE TAB
    # ===============================

    def binance_tab(self):

        page = QWidget()

        layout = QVBoxLayout()


        box = QGroupBox(
            "🔑 Binance API"
        )


        box_layout = QVBoxLayout()


        self.api_input = QLineEdit()

        self.api_input.setPlaceholderText(
            "Binance API Key"
        )


        self.secret_input = QLineEdit()

        self.secret_input.setPlaceholderText(
            "Binance Secret Key"
        )


        self.secret_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )


        save_button = QPushButton(
            "💾 API speichern"
        )


        save_button.clicked.connect(
            self.save_api
        )


        box_layout.addWidget(
            self.api_input
        )

        box_layout.addWidget(
            self.secret_input
        )

        box_layout.addWidget(
            save_button
        )


        box.setLayout(
            box_layout
        )


        layout.addWidget(
            box
        )


        page.setLayout(
            layout
        )


        return page



    # ===============================
    # TRADES TAB
    # ===============================

    def trades_tab(self):

        page = QWidget()

        layout = QVBoxLayout()



        self.table = QTableWidget()



        self.table.setColumnCount(
            8
        )


        self.table.setHorizontalHeaderLabels(
            [
                "Coin",
                "Side",
                "Price",
                "Amount",
                "Fee",
                "Value",
                "P/L",
                "Time"
            ]
        )



        refresh = QPushButton(
            "🔄Load Trades"
        )


        refresh.clicked.connect(
            self.load_history
        )



        layout.addWidget(
            self.table
        )


        layout.addWidget(
            refresh
        )


        page.setLayout(
            layout
        )


        return page



    # ===============================
    # LOAD TRADES JSON
    # ===============================

    def load_history(self):

        try:


            path = os.path.join(

                os.path.dirname(

                    os.path.abspath(__file__)

                ),

                "trades.json"

            )


            if not os.path.exists(path):


                self.log_message(
                    "⚠ trades.json fehlt"
                )


                return



            with open(

                path,

                "r"

            ) as file:


                trades = json.load(file)




            self.table.setRowCount(

                len(trades)

            )



            buy_price = None



            for row, trade in enumerate(trades):


                side = trade.get(

                    "side",

                    "BUY"

                )



                price = float(

                    trade.get(

                        "price",

                        0

                    )

                )



                amount = float(

                    trade.get(

                        "quantity",

                        0

                    )

                )



                value = price * amount



                pnl = 0



                if side == "BUY":


                    buy_price = price



                elif side == "SELL" and buy_price:


                    pnl = (

                        price - buy_price

                    ) * amount




                data = [

                    trade.get(
                        "symbol",
                        "BTCUSDT"
                    ),

                    "🟢 BUY"
                    if side == "BUY"
                    else
                    "🔴 SELL",

                    f"${price:,.2f}",

                    f"{amount:.6f}",

                    str(
                        trade.get(
                            "fee",
                            0
                        )
                    ),

                    f"${value:,.2f}",

                    f"${pnl:,.2f}",

                    trade.get(
                        "time",
                        "-"
                    )

                ]



                for col, text in enumerate(data):


                    self.table.setItem(

                        row,

                        col,

                        QTableWidgetItem(

                            str(text)

                        )

                    )




                if side == "BUY":


                    self.table.item(
                        row,
                        1
                    ).setForeground(

                        QColor(
                            "#00ff88"
                        )

                    )


                else:


                    self.table.item(
                        row,
                        1
                    ).setForeground(

                        QColor(
                            "#ff4444"
                        )

                    )



            self.table.resizeColumnsToContents()



            self.log_message(

                f"✅ {len(trades)} Trades geladen"

            )



        except Exception as e:


            self.log_message(

                f"❌ Trade Fehler: {e}"

            )



    # ===============================
    # SAVE API
    # ===============================

    def save_api(self):


        os.makedirs(

            "data",

            exist_ok=True

        )


        data = {

            "api_key":
            self.api_input.text(),

            "secret_key":
            self.secret_input.text()

        }



        with open(

            "data/binance.json",

            "w"

        ) as file:


            json.dump(

                data,

                file,

                indent=4

            )



        QMessageBox.information(

            self,

            "Binance",

            "✅ API gespeichert"

        )



    # ===============================
    # BTC PRICE TIMER
    # ===============================

    def start_price_timer(self):


        self.timer = QTimer()


        self.timer.timeout.connect(

            self.update_price

        )


        self.timer.start(

            5000

        )



    def update_price(self):


        try:


            price = self.binance.get_btc_price()



            if price:


                self.price_label.setText(

                    f"₿ BTC Preis\n\n💵 ${price:,.2f}"

                )


        except Exception as e:


            self.log_message(e)




    # ===============================
    # LOG
    # ===============================

    def log_message(self, message):


        print(message)


        if hasattr(

            self,

            "log_box"

        ):


            self.log_box.append(

                str(message)

            )