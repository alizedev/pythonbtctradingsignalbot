from dataclasses import dataclass
import config


@dataclass
class Wallet:

    usd: float
    btc: float



def create_demo_wallet(btc_price):

    btc_amount = (
        config.START_BALANCE_USD
        / btc_price
    )


    return Wallet(
        usd=config.START_BALANCE_USD,
        btc=btc_amount
    )