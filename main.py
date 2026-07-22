price = get_price()

wallet = create_demo_wallet(price)

print(f"Wallet: ${wallet.usd:,.2f}")
print(f"BTC Holdings: {wallet.btc:.8f} BTC")