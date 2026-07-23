from dataclasses import dataclass, field
from typing import List


@dataclass
class Balance:
    """
    Einzelnes Coin-Guthaben
    """

    asset: str
    free: float
    locked: float

    @property
    def total(self) -> float:
        return self.free + self.locked


@dataclass
class Account:
    """
    Binance Account Model
    """

    account_id: str = ""
    balances: List[Balance] = field(default_factory=list)

    total_value_usdt: float = 0.0
    total_profit_loss: float = 0.0
    roi_percentage: float = 0.0

    last_update: str = ""

    def add_balance(self, balance: Balance):
        """
        Fügt ein Coin-Guthaben hinzu
        """
        self.balances.append(balance)

    def get_balance(self, asset: str) -> float:
        """
        Gibt den Bestand eines Coins zurück
        Beispiel:
        BTC -> 0.25
        """

        for balance in self.balances:
            if balance.asset.upper() == asset.upper():
                return balance.total

        return 0.0

    def calculate_roi(self, invested_amount: float):
        """
        Berechnet ROI
        """

        if invested_amount <= 0:
            self.roi_percentage = 0
            return

        self.roi_percentage = (
            (self.total_value_usdt - invested_amount) / invested_amount
        ) * 100

    def update_value(self, value_usdt: float):
        """
        Aktualisiert den aktuellen Portfolio Wert
        """

        self.total_value_usdt = value_usdt

    def update_profit(self, invested_amount: float):
        """
        Berechnet Gewinn/Verlust
        """

        self.total_profit_loss = self.total_value_usdt - invested_amount

        self.calculate_roi(invested_amount)

    def get_summary(self):
        """
        Gibt eine Übersicht zurück
        """

        return {
            "Account": self.account_id,
            "Portfolio Value": f"{self.total_value_usdt:.2f} USDT",
            "Profit/Loss": f"{self.total_profit_loss:.2f} USDT",
            "ROI": f"{self.roi_percentage:.2f}%",
            "Coins": len(self.balances),
        }
