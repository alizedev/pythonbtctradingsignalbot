from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    """
    Binance Trade Model

    Speichert:
    - Kauf / Verkauf
    - Coin Menge
    - Preis
    - Gebühren
    - Gewinn / Verlust
    """

    trade_id: str

    symbol: str
    side: str        # BUY oder SELL

    quantity: float
    price: float

    fee: float = 0.0
    fee_asset: str = "USDT"

    timestamp: int = 0

    order_id: str = ""

    def total_value(self) -> float:
        """
        Gesamtwert des Trades
        """

        return self.quantity * self.price


    def net_value(self) -> float:
        """
        Wert nach Gebühren
        """

        return self.total_value() - self.fee


    def is_buy(self) -> bool:
        """
        Prüft ob Kauf
        """

        return self.side.upper() == "BUY"


    def is_sell(self) -> bool:
        """
        Prüft ob Verkauf
        """

        return self.side.upper() == "SELL"


    def get_datetime(self):
        """
        Zeitstempel als Datum
        """

        if self.timestamp == 0:
            return None

        return datetime.fromtimestamp(
            self.timestamp / 1000
        )


    def profit_loss(
        self,
        buy_price: float
    ) -> float:
        """
        Berechnet Gewinn/Verlust
        Beispiel:
        Kauf BTC bei 100000
        Verkauf bei 110000
        """

        if not self.is_sell():
            return 0.0

        return (
            (self.price - buy_price)
            * self.quantity
        ) - self.fee


    def roi(
        self,
        buy_price: float
    ) -> float:
        """
        ROI Prozent
        """

        if buy_price <= 0:
            return 0.0

        return (
            (
                self.price - buy_price
            )
            / buy_price
        ) * 100


    def to_dict(self):
        """
        Für JSON Speicherung
        """

        return {
            "trade_id": self.trade_id,
            "symbol": self.symbol,
            "side": self.side,
            "quantity": self.quantity,
            "price": self.price,
            "fee": self.fee,
            "fee_asset": self.fee_asset,
            "timestamp": self.timestamp,
            "order_id": self.order_id
        }


    def __str__(self):
        return (
            f"{self.side} "
            f"{self.quantity} {self.symbol} "
            f"@ {self.price}"
        )