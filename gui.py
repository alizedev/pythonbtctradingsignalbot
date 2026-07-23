from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
)

import pyqtgraph as pg


from candlestick import CandlestickItem



class Dashboard(QWidget):


    def __init__(
            self,
            binance,
            bot
    ):


        super().__init__()


        self.binance = binance

        self.bot = bot


        self.candles = []



        self.setWindowTitle(
            "BTC Binance Trading Bot"
        )


        self.resize(
            1200,
            800
        )


        self.create_ui()






    def create_ui(
            self
    ):


        layout = QVBoxLayout()



        self.status = QLabel(

            "🟢 Bot gestartet"

        )


        layout.addWidget(

            self.status

        )



        self.price_label = QLabel(

            "BTC Price: --"

        )


        layout.addWidget(

            self.price_label

        )



        # Chart


        self.chart = pg.PlotWidget()


        self.chart.setBackground(

            "black"

        )


        self.chart.showGrid(

            x=True,

            y=True

        )



        layout.addWidget(

            self.chart

        )



        self.candle_item = CandlestickItem()



        self.chart.addItem(

            self.candle_item

        )




        # Trade History



        self.table = QTableWidget()


        self.table.setColumnCount(

            5

        )


        self.table.setHorizontalHeaderLabels(

            [

                "Time",

                "Side",

                "Price",

                "Quantity",

                "Fee"

            ]

        )



        layout.addWidget(

            self.table

        )




        self.refresh_button = QPushButton(

            "Refresh"

        )


        self.refresh_button.clicked.connect(

            self.update_history

        )


        layout.addWidget(

            self.refresh_button

        )



        self.setLayout(

            layout

        )



        # Live candles verbinden


        self.binance.start_live_candles(

            self.update_chart

        )







    def update_chart(
            self,
            candles
    ):


        self.candles = candles



        print(

            "GUI CANDLES:",

            len(candles)

        )



        self.candle_item.setData(

            candles

        )



        if candles:


            price = candles[-1]["close"]


            self.price_label.setText(

                f"BTC Price: {price:.2f}$"

            )





    def update_history(
            self
    ):


        trades = (

            self.bot.trader.history.get_history()

        )



        self.table.setRowCount(

            len(trades)

        )



        for row, trade in enumerate(trades):


            self.table.setItem(

                row,

                0,

                QTableWidgetItem(

                    trade["time"]

                )

            )


            self.table.setItem(

                row,

                1,

                QTableWidgetItem(

                    trade["side"]

                )

            )


            self.table.setItem(

                row,

                2,

                QTableWidgetItem(

                    str(

                        trade["price"]

                    )

                )

            )


            self.table.setItem(

                row,

                3,

                QTableWidgetItem(

                    str(

                        trade["quantity"]

                    )

                )

            )


            self.table.setItem(

                row,

                4,

                QTableWidgetItem(

                    str(

                        trade["fee"]

                    )

                )

            )