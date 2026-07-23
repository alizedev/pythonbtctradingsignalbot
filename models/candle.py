from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:
    """
    Binance Candlestick Model

    Beispiel:
    BTCUSDT 1m Candle
    """

    symbol: str
    interval: str

    open_time: int
    close_time: int

    open_price: float
    high_price: float
    low_price: float
    close_price: float

    volume: float

    quote_volume: float = 0.0
    trades: int = 0

    def is_green(self) -> bool:
        """
        Prüft ob die Kerze positiv geschlossen hat
        """

        return self.close_price > self.open_price


    def is_red(self) -> bool:
        """
        Prüft ob die Kerze negativ geschlossen hat
        """

        return self.close_price < self.open_price


    @property
    def body_size(self) -> float:
        """
        Größe des Kerzenkörpers
        """

        return abs(
            self.close_price - self.open_price
        )


    @property
    def percentage_change(self) -> float:
        """
        Prozentuale Veränderung der Kerze
        """

        if self.open_price == 0:
            return 0

        return (
            (self.close_price - self.open_price)
            / self.open_price
        ) * 100


    def open_datetime(self):
        """
        Startzeit als Datum
        """

        return datetime.fromtimestamp(
            self.open_time / 1000
        )


    def close_datetime(self):
        """
        Endzeit als Datum
        """

        return datetime.fromtimestamp(
            self.close_time / 1000
        )


    def to_dict(self):
        """
        Für JSON / Speicherung
        """

        return {
            "symbol": self.symbol,
            "interval": self.interval,
            "open_time": self.open_time,
            "close_time": self.close_time,
            "open": self.open_price,
            "high": self.high_price,
            "low": self.low_price,
            "close": self.close_price,
            "volume": self.volume,
            "quote_volume": self.quote_volume,
            "trades": self.trades
        }


    def __str__(self):
        return (
            f"{self.symbol} "
            f"{self.interval} | "
            f"O:{self.open_price} "
            f"H:{self.high_price} "
            f"L:{self.low_price} "
            f"C:{self.close_price}"
        )