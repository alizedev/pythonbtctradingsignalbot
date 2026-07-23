import os
import json

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
    QTextEdit,
    QGroupBox,
    QHeaderView
)

from PyQt6.QtCore import QTimer, pyqtSlot
from PyQt6.QtGui import QFont

from modules.binance import BinanceModule
from candlestick import CandlestickItem




class Dashboard(QMainWindow):


    def __init__(self):

        super().__init__()



        self.setWindowTitle(
            "₿ Binance BTC Trading Terminal"
        )


        self.resize(
            1400,
            900
        )



        self.binance = BinanceModule()


        self.candles = []



        self.create_ui()



        self.load_chart_data()



    # =================================
    # UI
    # =================================

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





    # =================================
    # DASHBOARD
    # =================================

    def dashboard_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.price_label = QLabel(

            "₿ BTCUSDT\nLoading..."

        )


        self.price_label.setFont(

            QFont(

                "Arial",

                22

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

            "BTCUSDT 5m Live Candles"

        )



        self.candle_item = CandlestickItem()



        self.chart.addItem(

            self.candle_item

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


        return widget





    # =================================
    # BINANCE
    # =================================

    def binance_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        group = QGroupBox(

            "🔑 Binance API"

        )



        box = QVBoxLayout()



        self.api_key_input = QLineEdit()


        self.api_key_input.setPlaceholderText(

            "API Key"

        )



        self.secret_input = QLineEdit()


        self.secret_input.setPlaceholderText(

            "Secret Key"

        )



        self.secret_input.setEchoMode(

            QLineEdit.EchoMode.Password

        )



        save = QPushButton(

            "💾 Save"

        )



        save.clicked.connect(

            self.save_api

        )



        box.addWidget(

            self.api_key_input

        )


        box.addWidget(

            self.secret_input

        )


        box.addWidget(

            save

        )



        group.setLayout(

            box

        )


        layout.addWidget(

            group

        )


        widget.setLayout(

            layout

        )


        return widget





    # =================================
    # TRADES
    # =================================

    def trades_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.trade_table = QTableWidget()



        self.trade_table.setColumnCount(

            5

        )


        self.trade_table.setHorizontalHeaderLabels(

            [

            "Symbol",

            "Side",

            "Price",

            "Amount",

            "Fee"

            ]

        )



        self.trade_table.horizontalHeader().setSectionResizeMode(

            QHeaderView.ResizeMode.Stretch

        )



        button = QPushButton(

            "🔄 Load Trades"

        )


        button.clicked.connect(

            self.load_trades

        )



        layout.addWidget(

            self.trade_table

        )


        layout.addWidget(

            button

        )



        widget.setLayout(

            layout

        )


        return widget






    # =================================
    # LOAD CANDLES
    # =================================

    def load_chart_data(self):


        self.candles = self.binance.load_candles()



        self.candle_item.setData(

            self.candles

        )



        self.binance.start_live_candles(

            self.update_live_candle

        )





    # =================================
    # LIVE UPDATE
    # =================================

    @pyqtSlot(object)
    def update_live_candle(

        self,

        candle

    ):



        if self.candles:


            self.candles[-1] = candle


        else:


            self.candles.append(

                candle

            )



        self.candle_item.setData(

            self.candles

        )



        self.price_label.setText(

            f"""
₿ BTCUSDT LIVE

💵 ${candle['close']:,.2f}

🕯 Binance 5 Minute Candle
"""

        )





    # =================================
    # TRADES
    # =================================

    def load_trades(self):


        trades = self.binance.get_trades()



        self.trade_table.setRowCount(

            len(trades)

        )



        for row, trade in enumerate(trades):


            data = [

                "BTCUSDT",

                "BUY" if trade["isBuyer"] else "SELL",

                trade["price"],

                trade["qty"],

                trade["commission"]

            ]



            for col,value in enumerate(data):


                self.trade_table.setItem(

                    row,

                    col,

                    QTableWidgetItem(

                        str(value)

                    )

                )



        self.log_message(

            f"✅ {len(trades)} Trades geladen"

        )






    # =================================
    # SAVE API
    # =================================

    def save_api(self):


        os.makedirs(

            "data",

            exist_ok=True

        )


        with open(

            "data/binance.json",

            "w"

        ) as file:


            json.dump(

                {

                "api_key":

                self.api_key_input.text(),


                "secret":

                self.secret_input.text()

                },

                file,

                indent=4

            )



        self.log_message(

            "✅ API gespeichert"

        )






    def log_message(self,text):


        print(text)


        self.log_box.append(

            text

        )





    # =================================
    # CLEAN SHUTDOWN
    # =================================

    def closeEvent(self,event):


        try:

            self.binance.stop_websocket()


        except:

            pass



        event.accept()





    # =================================
    # STYLE
    # =================================

    def apply_style(self):


        self.setStyleSheet(

        """

        QWidget {

            background:#0b0f14;

            color:white;

        }


        QPushButton {

            background:#f7931a;

            color:black;

            padding:10px;

            border-radius:8px;

        }


        QLineEdit {

            background:#161b22;

            color:white;

            padding:8px;

        }


        QTableWidget {

            background:#010409;

        }

        """

        )