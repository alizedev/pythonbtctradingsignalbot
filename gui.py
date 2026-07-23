import os
import json
import time

import pyqtgraph as pg

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QGroupBox,
    QTextEdit,
    QHeaderView
)

from PyQt6.QtCore import QTimer

from PyQt6.QtGui import QFont

from modules.binance import BinanceModule



class Dashboard(QMainWindow):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "₿ BTC Trading Terminal"
        )


        self.resize(
            1400,
            900
        )


        self.binance = BinanceModule()


        self.price_history = []


        self.create_ui()


        self.start_price_timer()



    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):


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



        self.setCentralWidget(
            tabs
        )


        self.apply_style()



    # ==========================
    # DASHBOARD
    # ==========================

    def dashboard_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.price_label = QLabel(
            "₿ BTCUSDT\n\nLoading..."
        )


        self.price_label.setFont(
            QFont(
                "Arial",
                24
            )
        )


        layout.addWidget(
            self.price_label
        )



        self.chart = pg.PlotWidget()



        self.chart.setBackground(
            "#050505"
        )


        self.chart.showGrid(
            x=True,
            y=True
        )


        self.chart.setTitle(
            "BTCUSDT Binance Live Price"
        )



        self.line = self.chart.plot(
            pen=pg.mkPen(
                "#00ff88",
                width=3
            )
        )


        layout.addWidget(
            self.chart
        )



        self.log_box = QTextEdit()


        self.log_box.setReadOnly(
            True
        )


        layout.addWidget(
            self.log_box
        )



        widget.setLayout(
            layout
        )


        return widget    # ==========================
    # BINANCE TAB
    # ==========================

    def binance_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        box = QGroupBox(
            "🔑 Binance API"
        )


        box_layout = QVBoxLayout()



        self.api_key_input = QLineEdit()

        self.api_key_input.setPlaceholderText(
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
            "💾 Save API"
        )


        save_button.clicked.connect(
            self.save_api
        )



        box_layout.addWidget(
            self.api_key_input
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


        layout.addStretch()



        widget.setLayout(
            layout
        )


        return widget





    # ==========================
    # TRADES TAB
    # ==========================

    def trades_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.trade_table = QTableWidget()



        self.trade_table.setColumnCount(
            8
        )



        self.trade_table.setHorizontalHeaderLabels(

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



        self.trade_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )



        load_button = QPushButton(
            "🔄 Load Trades"
        )


        load_button.clicked.connect(
            self.load_trades
        )



        layout.addWidget(
            self.trade_table
        )


        layout.addWidget(
            load_button
        )



        widget.setLayout(
            layout
        )


        return widget





    # ==========================
    # SAVE BINANCE API
    # ==========================

    def save_api(self):


        os.makedirs(
            "data",
            exist_ok=True
        )



        api_data = {


            "api_key":

                self.api_key_input.text(),



            "secret_key":

                self.secret_input.text()


        }




        with open(

            "data/binance.json",

            "w"

        ) as file:


            json.dump(

                api_data,

                file,

                indent=4

            )



        self.log_message(

            "✅ Binance API gespeichert"

        )
    # ==========================
    # LOAD TRADES JSON
    # ==========================

    def load_trades(self):

        try:

            file = "trades.json"


            if not os.path.exists(file):

                self.log_message(
                    "⚠ trades.json nicht gefunden"
                )

                return



            with open(
                file,
                "r"
            ) as f:

                trades = json.load(f)



            self.trade_table.setRowCount(
                len(trades)
            )



            for row, trade in enumerate(trades):


                symbol = trade.get(
                    "symbol",
                    "BTCUSDT"
                )


                side = trade.get(
                    "side",
                    "-"
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


                fee = float(
                    trade.get(
                        "fee",
                        0
                    )
                )


                value = price * amount




                values = [

                    symbol,


                    "🟢 BUY"
                    if side.upper() == "BUY"
                    else
                    "🔴 SELL",



                    f"${price:,.2f}",


                    f"{amount:.6f} BTC",


                    f"{fee:.8f} BTC",


                    f"${value:,.2f}",


                    "⚪ $0.00",


                    trade.get(
                        "time",
                        "-"
                    )

                ]



                for col, item in enumerate(values):

                    self.trade_table.setItem(

                        row,

                        col,

                        QTableWidgetItem(
                            str(item)
                        )

                    )



            self.log_message(

                f"✅ {len(trades)} Trades geladen"

            )



        except Exception as e:


            self.log_message(

                f"❌ Trade Fehler: {e}"

            )





    # ==========================
    # PRICE TIMER
    # ==========================

    def start_price_timer(self):


        self.timer = QTimer()


        self.timer.timeout.connect(

            self.update_price

        )


        self.timer.start(

            5000

        )





    # ==========================
    # UPDATE BTC PRICE
    # ==========================

    def update_price(self):


        price = self.binance.get_btc_price()



        if price <= 0:

            return




        self.price_label.setText(

            f"""
₿ BTCUSDT LIVE

💵 ${price:,.2f}

🟢 BINANCE
"""

        )



        self.price_history.append(

            price

        )



        if len(self.price_history) > 100:


            self.price_history.pop(0)



        self.line.setData(

            self.price_history

        )



        self.chart.enableAutoRange()





    # ==========================
    # LOG
    # ==========================

    def log_message(
        self,
        text
    ):


        print(text)



        if hasattr(
            self,
            "log_box"
        ):


            self.log_box.append(

                str(text)

            )





    # ==========================
    # DARK STYLE
    # ==========================

    def apply_style(self):


        self.setStyleSheet(

        """

        QWidget {

            background:#0b0f14;

            color:white;

            font-size:14px;

        }



        QTabWidget::pane {

            border:1px solid #30363d;

        }



        QTabBar::tab {


            background:#161b22;

            padding:12px;

            border-radius:6px;

        }



        QTabBar::tab:selected {


            background:#f7931a;

            color:black;

        }




        QPushButton {


            background:#f7931a;

            color:black;

            padding:10px;

            border-radius:8px;

            font-weight:bold;

        }



        QPushButton:hover {


            background:#ffb347;

        }




        QLineEdit {


            background:#161b22;

            border:1px solid #30363d;

            padding:10px;

            color:white;

        }




        QTableWidget {


            background:#010409;

            alternate-background-color:#161b22;

            gridline-color:#30363d;

        }




        QHeaderView::section {


            background:#161b22;

            color:#f7931a;

            padding:8px;

        }




        QTextEdit {


            background:#010409;

            border-radius:8px;

        }

        """

        )