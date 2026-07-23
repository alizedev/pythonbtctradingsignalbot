import pandas as pd
import ta


def calculate(df):

    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()

    macd = ta.trend.MACD(df["close"])

    df["macd"] = macd.macd()
    df["signal"] = macd.macd_signal()

    df["ema50"] = ta.trend.EMAIndicator(df["close"], 50).ema_indicator()

    df["ema200"] = ta.trend.EMAIndicator(df["close"], 200).ema_indicator()

    return df
