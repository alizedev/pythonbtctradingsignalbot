from dataclasses import dataclass

# Demo Wallet
START_BALANCE_USD = 1000.00


@dataclass
class Wallet:
    usd: float
    btc: float


def create_demo_wallet(btc_price_usd: float) -> Wallet:
    btc_amount = START_BALANCE_USD / btc_price_usd

    return Wallet(
        usd=START_BALANCE_USD,
        btc=btc_amount
    )