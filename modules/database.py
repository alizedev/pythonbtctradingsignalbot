import json
import os
from datetime import datetime

import config


class DatabaseModule:
    """
    JSON Database Module

    Speichert:
    - Trades
    - Gewinne
    - Verluste
    - Statistiken
    """

    def __init__(self):

        self.enabled = getattr(config, "DATABASE_ENABLED", True)

        self.file = "data/trades.json"

        if not os.path.exists("data"):

            os.makedirs("data")

        if not os.path.exists(self.file):

            self.create_database()

    # =========================
    # CREATE DATABASE
    # =========================

    def create_database(self):

        data = {
            "trades": [],
            "statistics": {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "total_profit": 0,
                "total_loss": 0,
                "roi": 0,
            },
        }

        self.save(data)

    # =========================
    # LOAD / SAVE
    # =========================

    def load(self):

        if not self.enabled:

            return {}

        with open(self.file, "r") as f:

            return json.load(f)

    def save(self, data):

        if not self.enabled:

            return

        with open(self.file, "w") as f:

            json.dump(data, f, indent=4)

    # =========================
    # TRADES
    # =========================

    def add_trade(self, trade):

        data = self.load()

        trade["id"] = len(data["trades"]) + 1

        trade["timestamp"] = datetime.now().isoformat()

        data["trades"].append(trade)

        data["statistics"] = self.calculate_statistics(data["trades"])

        self.save(data)

    def get_trades(self):

        data = self.load()

        return data.get("trades", [])

    def clear_trades(self):

        self.create_database()

    # =========================
    # STATISTICS
    # =========================

    def calculate_statistics(self, trades):

        total = len(trades)

        profit = 0

        loss = 0

        wins = 0

        losses = 0

        for trade in trades:

            pnl = trade.get("profit_loss", 0)

            if pnl > 0:

                wins += 1

                profit += pnl

            elif pnl < 0:

                losses += 1

                loss += abs(pnl)

        win_rate = 0

        if total > 0:

            win_rate = (wins / total) * 100

        roi = 0

        if getattr(config, "START_BALANCE_USD", 0):

            roi = (profit - loss) / config.START_BALANCE_USD * 100

        return {
            "total_trades": total,
            "winning_trades": wins,
            "losing_trades": losses,
            "win_rate": round(win_rate, 2),
            "total_profit": round(profit, 2),
            "total_loss": round(loss, 2),
            "roi": round(roi, 2),
        }

    def get_statistics(self):

        data = self.load()

        return data.get("statistics", {})
