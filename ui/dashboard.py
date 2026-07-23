from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFrame
)

from PyQt6.QtCore import Qt


class Dashboard(QWidget):
    """
    Haupt Dashboard GUI
    """


    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "BTC Trading Signal Bot - Dashboard"
        )

        self.setMinimumSize(
            1000,
            650
        )

        self.init_ui()



    def init_ui(self):

        main_layout = QVBoxLayout()


        # ==========================
        # Header
        # ==========================

        title = QLabel(
            "🚀 Bitcoin Trading Dashboard"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size: 26px;
            font-weight: bold;
            """
        )

        main_layout.addWidget(title)



        # ==========================
        # Stats Boxen
        # ==========================

        stats_layout = QHBoxLayout()


        self.price_label = self.create_card(
            "BTC Preis",
            "$0.00"
        )


        self.portfolio_label = self.create_card(
            "Portfolio",
            "0 USDT"
        )


        self.profit_label = self.create_card(
            "Gewinn / Verlust",
            "0 USDT"
        )


        self.roi_label = self.create_card(
            "ROI",
            "0%"
        )


        stats_layout.addWidget(
            self.price_label
        )

        stats_layout.addWidget(
            self.portfolio_label
        )

        stats_layout.addWidget(
            self.profit_label
        )

        stats_layout.addWidget(
            self.roi_label
        )


        main_layout.addLayout(
            stats_layout
        )



        # ==========================
        # Trading Signal
        # ==========================


        self.signal_label = QLabel(
            "Signal: WAIT"
        )

        self.signal_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        self.signal_label.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )


        main_layout.addWidget(
            self.signal_label
        )



        # ==========================
        # Trade Tabelle
        # ==========================


        self.trade_table = QTableWidget()


        self.trade_table.setColumnCount(
            5
        )


        self.trade_table.setHorizontalHeaderLabels(
            [
                "Symbol",
                "Typ",
                "Menge",
                "Preis",
                "Zeit"
            ]
        )


        main_layout.addWidget(
            self.trade_table
        )



        # ==========================
        # Buttons
        # ==========================


        button_layout = QHBoxLayout()


        refresh_button = QPushButton(
            "🔄 Aktualisieren"
        )

        refresh_button.clicked.connect(
            self.refresh
        )


        settings_button = QPushButton(
            "⚙ Einstellungen"
        )


        button_layout.addWidget(
            refresh_button
        )


        button_layout.addWidget(
            settings_button
        )


        main_layout.addLayout(
            button_layout
        )


        self.setLayout(
            main_layout
        )



    def create_card(
        self,
        title,
        value
    ):

        frame = QFrame()

        frame.setFrameShape(
            QFrame.Shape.Box
        )


        layout = QVBoxLayout()


        title_label = QLabel(
            title
        )

        value_label = QLabel(
            value
        )


        title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        value_label.setStyleSheet(
            """
            font-size:18px;
            font-weight:bold;
            """
        )


        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )


        frame.setLayout(
            layout
        )


        return frame



    def update_price(
        self,
        price
    ):

        self.price_label.layout().itemAt(1).widget().setText(
            f"${price:,.2f}"
        )



    def update_portfolio(
        self,
        value
    ):

        self.portfolio_label.layout().itemAt(1).widget().setText(
            f"{value:.2f} USDT"
        )



    def update_profit(
        self,
        profit
    ):

        self.profit_label.layout().itemAt(1).widget().setText(
            f"{profit:.2f} USDT"
        )



    def update_roi(
        self,
        roi
    ):

        self.roi_label.layout().itemAt(1).widget().setText(
            f"{roi:.2f}%"
        )



    def update_signal(
        self,
        signal
    ):

        self.signal_label.setText(
            f"Signal: {signal}"
        )



    def add_trade(
        self,
        trade
    ):

        row = self.trade_table.rowCount()

        self.trade_table.insertRow(
            row
        )


        self.trade_table.setItem(
            row,
            0,
            QTableWidgetItem(
                trade.symbol
            )
        )

        self.trade_table.setItem(
            row,
            1,
            QTableWidgetItem(
                trade.side
            )
        )

        self.trade_table.setItem(
            row,
            2,
            QTableWidgetItem(
                str(trade.quantity)
            )
        )

        self.trade_table.setItem(
            row,
            3,
            QTableWidgetItem(
                str(trade.price)
            )
        )

        self.trade_table.setItem(
            row,
            4,
            QTableWidgetItem(
                str(
                    trade.get_datetime()
                )
            )
        )



    def refresh(self):

        print(
            "Dashboard refresh..."
        )