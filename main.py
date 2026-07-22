from wallet import create_demo_wallet

price = get_price()  # BTC price in USD

wallet = create_demo_wallet(price)

print(f"Wallet: ${wallet.usd:,.2f}")
print(f"BTC Holdings: {wallet.btc:.8f} BTC")