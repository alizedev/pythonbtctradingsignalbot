import pandas as pd

from binance_api import get_candles,get_price
from indicators import calculate
from signal_engine import generate_signal


while True:


    candles=get_candles()


    df=pd.DataFrame(
        candles,
        columns=[
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume"
        ]
    )


    df=calculate(df)


    signal=generate_signal(df)


    print(
        "BTC:",
        get_price()
    )

    print(signal)