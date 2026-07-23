def get_trade_history(self):
    if not self.client:
        return []

    try:

        trades = self.client.get_my_trades(
            symbol="BTCUSDT"
        )

        return trades


    except Exception as e:

        print(
            "Trade history error:",
            e
        )

        return []