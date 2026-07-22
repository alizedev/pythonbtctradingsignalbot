from dataclasses import dataclass
import config


@dataclass
class Wallet:

    usd: float
    btc: float

# wallet.py

from dataclasses import dataclass
import config


@dataclass
class Wallet:

    usd: float
    btc: float



def create_wallet(price):

    btc_amount = (
        config.START_BALANCE_USD / price
    )


    return Wallet(
        usd=config.START_BALANCE_USD,
        btc=btc_amount
    )

def create_demo_wallet(btc_price):

    btc_amount = (
        config.START_BALANCE_USD
        / btc_price
    )


    return Wallet(
        usd=config.START_BALANCE_USD,
        btc=btc_amount
    )