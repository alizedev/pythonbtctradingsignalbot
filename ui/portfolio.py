from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
)

from PyQt6.QtCore import Qt


class PortfolioWidget(QWidget):
    """
    Portfolio Ansicht

    Zeigt:
    - Coin Bestand
    - Wert
    - Gewinn/Verlust
    - ROI
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Portfolio")

        self.setMinimumSize(900, 500)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        # Titel

        title = QLabel("💰 Binance Portfolio")

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet(
            """
            font-size:24px;
            font-weight:bold;
            """
        )

        layout.addWidget(title)

        # Gesamtwerte

        info_layout = QHBoxLayout()

        self.total_value = QLabel("Portfolio Wert: 0 USDT")

        self.total_profit = QLabel("Gewinn/Verlust: 0 USDT")

        self.total_roi = QLabel("ROI: 0%")

        info_layout.addWidget(self.total_value)

        info_layout.addWidget(self.total_profit)

        info_layout.addWidget(self.total_roi)

        layout.addLayout(info_layout)

        # Tabelle

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            ["Asset", "Menge", "Preis", "Wert", "Profit", "ROI"]
        )

        layout.addWidget(self.table)

        # Buttons

        button_layout = QHBoxLayout()

        refresh = QPushButton("🔄 Aktualisieren")

        refresh.clicked.connect(self.refresh)

        export = QPushButton("📁 Export")

        button_layout.addWidget(refresh)

        button_layout.addWidget(export)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_summary(self, value, profit, roi):

        self.total_value.setText(f"Portfolio Wert: {value:.2f} USDT")

        self.total_profit.setText(f"Gewinn/Verlust: {profit:.2f} USDT")

        self.total_roi.setText(f"ROI: {roi:.2f}%")

    def add_asset(self, asset, amount, price, value, profit, roi):

        row = self.table.rowCount()

        self.table.insertRow(row)

        data = [asset, amount, price, value, profit, roi]

        for column, item in enumerate(data):

            self.table.setItem(row, column, QTableWidgetItem(str(item)))

    def clear_table(self):

        self.table.setRowCount(0)

    def refresh(self):

        print("Portfolio aktualisiert")
