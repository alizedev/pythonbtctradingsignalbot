import config
from telegram import Bot
import asyncio


async def send_signal(message):

    bot = Bot(
        token=config.TELEGRAM_TOKEN
    )

    await bot.send_message(
        chat_id=config.CHAT_ID,
        text=message
    )



def send_telegram(message):

    asyncio.run(
        send_signal(message)
    )



def format_signal(signal, price):

    emoji = "⚪"


    if signal["signal"] == "BUY":
        emoji = "🟢"

    elif signal["signal"] == "SELL":
        emoji = "🔴"



    message = f"""
{emoji} BTC AI SIGNAL ALERT

━━━━━━━━━━━━━━

Signal:
{signal["signal"]}

Confidence:
{signal["confidence"]}%

BTC Price:
{price}$


━━━━━━━━━━━━━━

Powered by BTC AI Tracker
"""


    return message