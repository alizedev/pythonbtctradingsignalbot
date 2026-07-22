import ccxt
import config


exchange = ccxt.binance({
    "apiKey": config.BINANCE_API_KEY,
    "secret": config.BINANCE_SECRET
})


def get_price():

    ticker = exchange.fetch_ticker(
        config.SYMBOL
    )

    return ticker["last"]



def get_candles():

    data = exchange.fetch_ohlcv(
        config.SYMBOL,
        timeframe=config.TIMEFRAME,
        limit=200
    )

    return data