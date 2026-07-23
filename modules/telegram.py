import os
import asyncio

from dotenv import load_dotenv

from telegram import Bot

import config


load_dotenv()


class TelegramModule:
    """
    Telegram Notification Module

    Funktionen:
    - Trading Alerts
    - Bot Status
    - Fehler Meldungen
    """

    def __init__(self):

        self.enabled = getattr(config, "TELEGRAM_ENABLED", False)

        self.token = os.getenv("TELEGRAM_BOT_TOKEN")

        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if self.enabled:

            if not self.token:

                raise Exception("Telegram Token fehlt")

            self.bot = Bot(token=self.token)

            print("Telegram Modul gestartet")

        else:

            self.bot = None

            print("Telegram deaktiviert")

    # =========================
    # SEND MESSAGE
    # =========================

    def send_message(self, message):

        if not self.enabled:

            return False

        async def send():

            await self.bot.send_message(chat_id=self.chat_id, text=message)

        try:

            asyncio.run(send())

            return True

        except Exception as e:

            print("Telegram Fehler:", e)

            return False

    # =========================
    # TRADING ALERTS
    # =========================

    def send_buy_alert(self, price, quantity):

        message = f"""

🟢 BUY SIGNAL

Coin:
BTCUSDT

Preis:
${price}

Menge:
{quantity} BTC

Mode:
Trading Bot

"""

        return self.send_message(message)

    def send_sell_alert(self, price, quantity):

        message = f"""

🔴 SELL SIGNAL

Coin:
BTCUSDT

Preis:
${price}

Menge:
{quantity} BTC

Mode:
Trading Bot

"""

        return self.send_message(message)

    # =========================
    # SYSTEM ALERTS
    # =========================

    def send_status(self, status):

        message = f"""

🤖 BTC Trading Bot

Status:

{status}

"""

        return self.send_message(message)

    def send_error(self, error):

        message = f"""

⚠️ BOT ERROR

{error}

"""

        return self.send_message(message)
