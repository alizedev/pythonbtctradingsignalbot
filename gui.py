import os
import json

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QTabWidget,
    QGroupBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from PyQt6.QtCore import pyqtSlot

from PyQt6.QtGui import QColor


from modules.binance import BinanceModule
from modules.bot import TradingBot
from modules.strategy import Strategy
from modules.trader import Trader
from modules.risk import RiskManager



from candlestick import CandlestickItem





class Dashboard(QMainWindow):


    def __init__(self):

        super().__init__()



        self.setWindowTitle(

            "₿ Bitcoin Trading Bot"

        )



        self.resize(

            1400,

            900

        )



        # ======================
        # MODULE
        # ======================


        self.binance = BinanceModule()


        self.strategy = Strategy()

        self.trader = Trader(
            self.binance
        )


        self.risk = RiskManager()



        self.bot = TradingBot(

            self.binance,

            self.strategy,

            self.trader,

            self.risk

        )





        self.candles = []



        self.create_ui()



        self.apply_style()

    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):


        self.tabs = QTabWidget()



        self.chart_tab = self.create_chart_tab()

        self.trading_tab = self.create_trading_tab()

        self.api_tab = self.create_api_tab()

        self.trades_tab = self.create_trades_tab()

        self.log_tab = self.create_log_tab()



        self.tabs.addTab(

            self.chart_tab,

            "📈 BTC Chart"

        )


        self.tabs.addTab(

            self.trading_tab,

            "🤖 Trading"

        )


        self.tabs.addTab(

            self.api_tab,

            "🔑 Binance API"

        )


        self.tabs.addTab(

            self.trades_tab,

            "📜 Trades"

        )


        self.tabs.addTab(

            self.log_tab,

            "📝 Debug"

        )



        self.setCentralWidget(

            self.tabs

        )



        # Binance Live Stream starten

        self.binance.start_live_candles(

            self.update_candle

        )






    # ==========================
    # CHART TAB
    # ==========================


    def create_chart_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.price_label = QLabel(

            "BTC Preis: --"

        )



        self.price_label.setStyleSheet(

            "font-size:22px;font-weight:bold;"

        )



        layout.addWidget(

            self.price_label

        )





        from pyqtgraph import PlotWidget



        self.chart = PlotWidget()



        self.chart.showGrid(

            x=True,

            y=True

        )



        self.chart.setBackground(

            "#080808"

        )



        self.chart_item = CandlestickItem()
        # Alte Binance Candles laden

        self.candles = self.binance.get_candles(
            100
        )

        self.chart_item.setData(
            self.candles
        )



        self.chart.addItem(

            self.chart_item

        )



        layout.addWidget(

            self.chart

        )



        widget.setLayout(

            layout

        )



        return widget






    # ==========================
    # LIVE CANDLE UPDATE
    # ==========================


    @pyqtSlot(dict)

    def update_candle(

        self,

        candle

    ):


        try:


            self.candles.append(

                candle

            )



            if len(self.candles) > 200:


                self.candles.pop(

                    0

                )



            self.chart_item.setData(

                self.candles

            )



            price = candle["close"]



            self.price_label.setText(

                f"₿ BTC/USDT   ${price:,.2f}"

            )



        except Exception as e:


            self.log_message(

                f"Chart Fehler: {e}"

            )
    # ==========================
    # TRADING TAB
    # ==========================

    def create_trading_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.signal_label = QLabel(

            "Signal: WAIT"

        )


        self.signal_label.setStyleSheet(

            "font-size:24px;font-weight:bold;"

        )



        layout.addWidget(

            self.signal_label

        )





        button_layout = QHBoxLayout()



        self.start_button = QPushButton(

            "🟢 Start Trading"

        )


        self.start_button.clicked.connect(

            self.start_trading

        )



        button_layout.addWidget(

            self.start_button

        )





        self.stop_button = QPushButton(

            "🔴 Stop Trading"

        )


        self.stop_button.clicked.connect(

            self.stop_trading

        )



        button_layout.addWidget(

            self.stop_button

        )






        self.auto_button = QPushButton(

            "⚡ Auto Trading OFF"

        )


        self.auto_button.clicked.connect(

            self.toggle_auto_trade

        )


        button_layout.addWidget(

            self.auto_button

        )





        layout.addLayout(

            button_layout

        )




        widget.setLayout(

            layout

        )


        return widget






    # ==========================
    # API TAB
    # ==========================


    def create_api_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.api_key_input = QLineEdit()


        self.api_key_input.setPlaceholderText(

            "Binance API Key"

        )



        layout.addWidget(

            self.api_key_input

        )





        self.api_secret_input = QLineEdit()


        self.api_secret_input.setPlaceholderText(

            "Binance Secret"

        )


        self.api_secret_input.setEchoMode(

            QLineEdit.EchoMode.Password

        )



        layout.addWidget(

            self.api_secret_input

        )





        save_button = QPushButton(

            "💾 API speichern"

        )


        save_button.clicked.connect(

            self.save_api

        )



        layout.addWidget(

            save_button

        )



        widget.setLayout(

            layout

        )


        return widget






    # ==========================
    # TRADES TAB
    # ==========================


    def create_trades_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



        self.trade_table = QTableWidget()



        self.trade_table.setColumnCount(

            7

        )



        self.trade_table.setHorizontalHeaderLabels(

            [

                "ID",

                "Coin",

                "Side",

                "Price",

                "Amount",

                "Fee",

                "Zeit"

            ]

        )



        self.trade_table.horizontalHeader().setSectionResizeMode(

            QHeaderView.ResizeMode.Stretch

        )



        layout.addWidget(

            self.trade_table

        )



        widget.setLayout(

            layout

        )


        self.load_trades()



        return widget
    # ==========================
    # START TRADING
    # ==========================

    def start_trading(self):

        try:

            self.bot.start(

                self.update_signal

            )


            self.log_message(

                "🟢 Trading Bot gestartet"

            )


        except Exception as e:


            self.log_message(

                f"❌ Start Fehler: {e}"

            )





    # ==========================
    # STOP TRADING
    # ==========================

    def stop_trading(self):

        try:


            self.bot.stop()



            self.log_message(

                "🔴 Trading Bot gestoppt"

            )


        except Exception as e:


            self.log_message(

                f"❌ Stop Fehler: {e}"

            )







    # ==========================
    # AUTO TRADE
    # ==========================

    def toggle_auto_trade(self):


        if self.bot.auto_trade:


            self.bot.disable_auto_trade()



            self.auto_button.setText(

                "⚡ Auto Trading OFF"

            )



            self.log_message(

                "⛔ Auto Trading deaktiviert"

            )



        else:


            self.bot.enable_auto_trade()



            self.auto_button.setText(

                "⚡ Auto Trading ON"

            )


            self.log_message(

                "⚠ Auto Trading aktiviert"

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



        self.log_message(

            f"Signal Update: {signal}"

        )








    # ==========================
    # SAVE API
    # ==========================

    def save_api(self):


        try:


            os.makedirs(

                "data",

                exist_ok=True

            )



            data = {


                "key":

                self.api_key_input.text(),



                "secret":

                self.api_secret_input.text()

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





            self.log_message(

                "✅ Binance API gespeichert"

            )



            self.binance.load_api()



        except Exception as e:



            self.log_message(

                f"❌ API Fehler: {e}"

            )








    # ==========================
    # LOAD TRADES
    # ==========================

    def load_trades(self):


        try:


            if not os.path.exists(

                "trades.json"

            ):


                return




            with open(

                "trades.json",

                "r",

                encoding="utf-8"

            ) as f:


                trades = json.load(f)





            self.trade_table.setRowCount(

                len(trades)

            )





            for row, trade in enumerate(trades):


                self.trade_table.setItem(

                    row,

                    0,

                    QTableWidgetItem(

                        str(trade.get("id",""))

                    )

                )



                self.trade_table.setItem(

                    row,

                    1,

                    QTableWidgetItem(

                        trade.get("coin","")

                    )

                )



                self.trade_table.setItem(

                    row,

                    2,

                    QTableWidgetItem(

                        trade.get("side","")

                    )

                )



                self.trade_table.setItem(

                    row,

                    3,

                    QTableWidgetItem(

                        str(trade.get("price",""))

                    )

                )



                self.trade_table.setItem(

                    row,

                    4,

                    QTableWidgetItem(

                        str(trade.get("amount",""))

                    )

                )



                self.trade_table.setItem(

                    row,

                    5,

                    QTableWidgetItem(

                        str(trade.get("fee",""))

                    )

                )



                self.trade_table.setItem(

                    row,

                    6,

                    QTableWidgetItem(

                        trade.get("timestamp","")

                    )

                )



        except Exception as e:


            self.log_message(

                f"Trades Fehler: {e}"

            )








    # ==========================
    # LOG TAB
    # ==========================

    def create_log_tab(self):


        widget = QWidget()


        layout = QVBoxLayout()



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





    # ==========================
    # LOG MESSAGE
    # ==========================

    def log_message(

        self,

        message

    ):


        print(message)



        if hasattr(

            self,

            "log_box"

        ):


            self.log_box.append(

                message

            )
    # ==========================
    # STYLE
    # ==========================

    def apply_style(self):


        self.setStyleSheet(

            """

            QMainWindow {

                background-color:#111111;

                color:white;

            }


            QWidget {

                background-color:#111111;

                color:white;

            }


            QPushButton {

                background-color:#222222;

                border:1px solid #444444;

                padding:8px;

                border-radius:5px;

            }


            QPushButton:hover {

                background-color:#333333;

            }


            QLabel {

                color:white;

            }


            QLineEdit {

                background-color:#222222;

                color:white;

                padding:6px;

            }


            QTextEdit {

                background-color:#050505;

                color:#00ff88;

                font-family:monospace;

            }


            QTableWidget {

                background-color:#151515;

                color:white;

                gridline-color:#333333;

            }


            """

        )






    # ==========================
    # WINDOW CLOSE
    # ==========================

    def closeEvent(

        self,

        event

    ):


        try:


            self.bot.stop()



            self.binance.stop_websocket()



        except Exception as e:


            print(

                e

            )



        event.accept()