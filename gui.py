import os
import json


from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)


from PyQt6.QtCore import Qt, QTimer


from PyQt6.QtGui import (
    QColor,
    QFont
)



class Dashboard(QWidget):


    def __init__(self):

        super().__init__()


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



    # ==================================================
    # THEME
    # ==================================================

    def apply_dark_theme(self):

        self.setStyleSheet("""

        QWidget {

            background:#0d1117;
            color:white;

        }


        QLabel {

            background:transparent;
            color:white;

        }


        QPushButton {

            background:#21262d;
            color:white;
            border:1px solid #30363d;
            border-radius:10px;
            padding:12px;

        }


        QPushButton:hover {

            background:#238636;

        }


        QLineEdit {

            background:#161b22;
            color:white;
            border-radius:8px;
            padding:10px;

        }


        QTextEdit {

            background:#090b10;
            color:white;

        }


        QGroupBox {

            background:#161b22;
            border-radius:12px;
            padding:15px;

        }


        QTableWidget {

            background:#161b22;
            color:white;

        }

        """)



    # ==================================================
    # MAIN UI
    # ==================================================

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
                28
            )
        )


        title.setStyleSheet(
            "color:#f7931a;"
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
            self.trading_tab(),
            "🤖 Trading"
        )


        tabs.addTab(
            self.history_tab(),
            "📜 Trades"
        )



        layout.addWidget(
            tabs
        )


        self.setLayout(
            layout
        )



    # ==================================================
    # DASHBOARD
    # ==================================================

    def dashboard_tab(self):


        page = QWidget()


        layout = QVBoxLayout()



        self.price_label = QLabel(
            "₿ BTC PRICE\n\nLoading..."
        )


        self.portfolio_label = QLabel(
            "💰 Portfolio\n\nLoading..."
        )


        self.signal_label = QLabel(
            "📈 Signal\n\nWAIT"
        )



        for widget in [

            self.price_label,
            self.portfolio_label,
            self.signal_label

        ]:


            widget.setFont(
                QFont(
                    "Arial",
                    20
                )
            )


            widget.setStyleSheet("""

            background:#161b22;

            border:1px solid #30363d;

            border-radius:15px;

            padding:25px;

            """)


            layout.addWidget(
                widget
            )



        page.setLayout(
            layout
        )


        return page



    # ==================================================
    # BINANCE
    # ==================================================

    def binance_tab(self):


        page = QWidget()


        layout = QVBoxLayout()



        box = QGroupBox(
            "🔑 Binance API"
        )


        form = QVBoxLayout()



        self.api_input = QLineEdit()

        self.api_input.setPlaceholderText(
            "API Key"
        )


        self.secret_input = QLineEdit()

        self.secret_input.setPlaceholderText(
            "Secret Key"
        )


        self.secret_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )



        button = QPushButton(
            "💾 Save API"
        )


        button.clicked.connect(
            self.save_api
        )



        form.addWidget(
            self.api_input
        )


        form.addWidget(
            self.secret_input
        )


        form.addWidget(
            button
        )


        box.setLayout(
            form
        )


        layout.addWidget(
            box
        )


        page.setLayout(
            layout
        )


        return page



    # ==================================================
    # TRADING
    # ==================================================

    def trading_tab(self):


        page = QWidget()


        layout = QVBoxLayout()



        buttons = QHBoxLayout()



        for name in [

            "▶ Start",

            "⏹ Stop",

            "⬆ BUY",

            "⬇ SELL"

        ]:


            btn = QPushButton(
                name
            )


            btn.clicked.connect(
                lambda checked=False,
                x=name:
                self.log_message(x)
            )


            buttons.addWidget(
                btn
            )



        self.console = QTextEdit()



        layout.addLayout(
            buttons
        )


        layout.addWidget(
            self.console
        )


        page.setLayout(
            layout
        )


        return page



    # ==================================================
    # HISTORY
    # ==================================================

    def history_tab(self):


        page = QWidget()


        layout = QVBoxLayout()



        self.table = QTableWidget()



        self.table.setColumnCount(
            8
        )


        self.table.setHorizontalHeaderLabels([

            "ID",
            "Symbol",
            "Side",
            "Price",
            "Amount",
            "Profit",
            "ROI",
            "Time"

        ])



        refresh = QPushButton(
            "Refresh"
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



    # ==================================================
    # SAVE API
    # ==================================================

    def save_api(self):


        os.makedirs(
            "data",
            exist_ok=True
        )



        with open(
            "data/binance.json",
            "w"
        ) as f:


            json.dump({

                "api_key":
                self.api_input.text(),

                "secret_key":
                self.secret_input.text()

            },

            f,

            indent=4

            )


        QMessageBox.information(
            self,
            "Saved",
            "Binance API gespeichert"
        )



    # ==================================================
    # HISTORY LOAD
    # ==================================================

    def load_history(self):


        path="data/trades.json"


        if not os.path.exists(path):

            return



        with open(path) as f:

            data=json.load(f)



        trades=data.get(
            "trades",
            []
        )


        self.table.setRowCount(
            len(trades)
        )



        for row,t in enumerate(trades):


            values=list(t.values())


            for col,v in enumerate(values[:8]):

                self.table.setItem(

                    row,
                    col,

                    QTableWidgetItem(
                        str(v)
                    )

                )



    # ==================================================
    # LOG
    # ==================================================

    def log_message(self,text):


        self.console.append(
            text
        )



    # ==================================================
    # PRICE TIMER
    # ==================================================

    def start_price_timer(self):


        self.timer=QTimer()


        self.timer.timeout.connect(
            self.update_price
        )


        self.timer.start(
            5000
        )



    def update_price(self):


        pass