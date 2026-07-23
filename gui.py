import os
import json

import pyqtgraph as pg

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
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

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QFont, QColor


from modules.binance import BinanceModule
from modules.strategy import Strategy
from modules.trader import Trader
from modules.bot import TradingBot
from modules.risk import RiskManager

from candlestick import CandlestickItem




class Dashboard(QMainWindow):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "₿ Bitcoin Trading Terminal"
        )


        self.resize(
            1100,
            700
        )



        self.binance = BinanceModule()



        self.strategy = Strategy()


        self.trader = Trader(

            self.binance,

            paper=True

        )


        self.risk = RiskManager()



        self.bot = TradingBot(

            self.strategy,

            self.trader,

            self.risk

        )



        self.candles = []



        self.create_ui()



        self.load_chart()





    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):


        tabs = QTabWidget()



        tabs.addTab(

            self.dashboard_tab(),

            "📈 Dashboard"

        )



        tabs.addTab(

            self.trades_tab(),

            "📜 Trades"

        )



        tabs.addTab(

            self.binance_tab(),

            "🔑 Binance"

        )



        self.setCentralWidget(

            tabs

        )


        self.apply_style()





    # ==========================
    # DASHBOARD TAB
    # ==========================

    def dashboard_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()


        layout.setSpacing(
            8
        )



        self.price_label = QLabel(

            "₿ BTCUSDT Loading..."

        )


        self.price_label.setFont(

            QFont(

                "Arial",

                18

            )

        )



        layout.addWidget(

            self.price_label

        )



        buttons = QHBoxLayout()



        self.start_button = QPushButton(

            "🟢 Trading starten"

        )


        self.stop_button = QPushButton(

            "🔴 Trading stoppen"

        )



        self.start_button.clicked.connect(

            self.start_trading

        )


        self.stop_button.clicked.connect(

            self.stop_trading

        )



        buttons.addWidget(

            self.start_button

        )


        buttons.addWidget(

            self.stop_button

        )



        layout.addLayout(

            buttons

        )



        self.signal_label = QLabel(

            "Signal: WAIT"

        )


        layout.addWidget(

            self.signal_label

        )



        self.chart = pg.PlotWidget()



        self.chart.setBackground(

            "#080808"

        )



        self.chart.showGrid(

            x=True,

            y=True

        )



        self.chart.setTitle(

            "BTCUSDT Binance 5m"

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


        self.log_box.setMaximumHeight(

            120

        )



        layout.addWidget(

            self.log_box

        )



        widget.setLayout(

            layout

        )


        return widget
    # ==========================
    # BINANCE TAB
    # ==========================

    def binance_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        box = QGroupBox(

            "Binance API"

        )


        box_layout = QVBoxLayout()



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



        save_button = QPushButton(

            "💾 API speichern"

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
    # LOAD CHART
    # ==========================

    def load_chart(self):


        try:


            self.candles = self.binance.load_candles()



            self.candle_item.setData(

                self.candles

            )



            self.binance.start_live_candles(

                self.update_candle

            )


            self.update_price()



        except Exception as e:


            self.log_message(

                f"Chart Fehler: {e}"

            )







    # ==========================
    # UPDATE CANDLE
    # ==========================

    @pyqtSlot(object)
    def update_candle(

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


        self.update_price()







    # ==========================
    # CURRENT BTC PRICE
    # ==========================

    def update_price(self):


        try:


            price = self.binance.get_btc_price()



            self.price_label.setText(

                f"₿ BTCUSDT   ${price:,.2f}"

            )



        except Exception as e:


            self.log_message(

                f"Preis Fehler: {e}"

            )







    # ==========================
    # SAVE API
    # ==========================

    def save_api(self):


        os.makedirs(

            "data",

            exist_ok=True

        )



        data = {


            "key":

            self.api_key_input.text(),


            "secret":

            self.secret_input.text()


        }




        with open(

            "data/binance.json",

            "w"

        ) as f:


            json.dump(

                data,

                f,

                indent=4

            )



        self.binance.load_api()



        self.log_message(

            "✅ Binance API gespeichert"

        )
    # ==========================
    # TRADES TAB
    # ==========================

    def trades_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.trade_table = QTableWidget()



        self.trade_table.setColumnCount(

            5

        )



        self.trade_table.setHorizontalHeaderLabels(

            [

                "Coin",

                "Side",

                "Price",

                "Amount",

                "Fee"

            ]

        )



        self.trade_table.horizontalHeader().setSectionResizeMode(

            QHeaderView.ResizeMode.Stretch

        )



        self.trade_table.verticalHeader().setVisible(

            False

        )



        self.trade_table.setAlternatingRowColors(

            True

        )



        self.trade_table.setSelectionBehavior(

            QTableWidget.SelectionBehavior.SelectRows

        )



        layout.addWidget(

            self.trade_table

        )



        load_button = QPushButton(

            "🔄 Trades laden"

        )


        load_button.clicked.connect(

            self.load_trades

        )


        layout.addWidget(

            load_button

        )



        widget.setLayout(

            layout

        )



        return widget







    # ==========================
    # LOAD LOCAL TRADES
    # ==========================

    def load_trades(self):


        file = "trades.json"



        if not os.path.exists(file):


            self.log_message(

                "⚠ trades.json nicht gefunden"

            )


            return




        try:



            with open(

                file,

                "r"

            ) as f:



                trades = json.load(f)





            self.trade_table.setRowCount(

                len(trades)

            )





            for row, trade in enumerate(trades):



                coin = trade.get(

                    "coin",

                    "₿ BTC"

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

                        "amount",

                        0

                    )

                )



                fee = float(

                    trade.get(

                        "fee",

                        0

                    )

                )




                values = [

                    coin,


                    side,


                    f"${price:,.2f}",


                    f"{amount:.6f} BTC",


                    f"{fee:.4f} USDT"


                ]





                for col,value in enumerate(values):


                    item = QTableWidgetItem(

                        value

                    )



                    self.trade_table.setItem(

                        row,

                        col,

                        item

                    )







                # BUY / SELL Farbe



                side_item = self.trade_table.item(

                    row,

                    1

                )



                if side.upper() == "BUY":



                    side_item.setForeground(

                        QColor(

                            "#00ff88"

                        )

                    )



                elif side.upper() == "SELL":



                    side_item.setForeground(

                        QColor(

                            "#ff5555"

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
    # START TRADING
    # ==========================

    def start_trading(self):


        self.bot.start(

            lambda:

            self.candles,

            self.update_signal

        )


        self.log_message(

            "🟢 Trading Bot gestartet"

        )




    # ==========================
    # STOP TRADING
    # ==========================

    def stop_trading(self):


        self.bot.stop()


        self.log_message(

            "🔴 Trading Bot gestoppt"

        )





    # ==========================
    # SIGNAL UPDATE
    # ==========================

    def update_signal(

        self,

        signal

    ):


        self.signal_label.setText(

            f"Signal: {signal}"

        )



        if signal == "BUY":


            self.signal_label.setStyleSheet(

                "color:#00ff88;font-weight:bold"

            )



        elif signal == "SELL":


            self.signal_label.setStyleSheet(

                "color:#ff5555;font-weight:bold"

            )



        else:


            self.signal_label.setStyleSheet(

                "color:white"

            )







    # ==========================
    # DEBUG LOG
    # ==========================

    def log_message(

        self,

        message

    ):


        self.log_box.append(

            str(message)

        )


        print(

            message

        )







    # ==========================
    # DARK BITCOIN STYLE
    # ==========================

    def apply_style(self):


        self.setStyleSheet(

        """

        QMainWindow {

            background:#0b0e11;

        }


        QWidget {

            color:#ffffff;

            font-size:13px;

        }


        QLabel {

            color:#f7931a;

        }


        QPushButton {


            background:#f7931a;

            color:#000000;

            border-radius:8px;

            padding:8px;

            font-weight:bold;


        }


        QPushButton:hover {


            background:#ffb347;

        }




        QTabWidget::pane {


            border:1px solid #333;


        }



        QTabBar::tab {


            background:#161b22;

            padding:10px;

        }



        QTabBar::tab:selected {


            background:#f7931a;

            color:black;

        }



        QTextEdit {


            background:#050505;

            border:1px solid #333;

        }




        QTableWidget {


            background:#111820;

            alternate-background-color:#161b22;

            gridline-color:#333;

        }



        QHeaderView::section {


            background:#161b22;

            color:#f7931a;

            padding:8px;

            border:none;

        }


        QLineEdit {


            background:#111820;

            border:1px solid #444;

            padding:6px;

            color:white;

        }


        """

        )







    # ==========================
    # CLOSE
    # ==========================

    def closeEvent(

        self,

        event

    ):


        try:


            self.bot.stop()


            self.binance.stop_websocket()



        except Exception:


            pass



        event.accept()