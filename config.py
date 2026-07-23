import os
from dotenv import load_dotenv

load_dotenv()


# Binance API

BINANCE_API_KEY = os.getenv(
    "BINANCE_API_KEY"
)

BINANCE_SECRET_KEY = os.getenv(
    "BINANCE_SECRET_KEY"
)


# Trading Simulator

START_BALANCE_USD = 1000.0


# Test BTC Preis
BTC_PRICE_USD = 118000.0