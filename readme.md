# 🚀 BTC AI Signal Tracker

A modern Python Bitcoin trading analysis dashboard.

The application monitors BTC/USDT market data and generates technical trading signals using multiple indicators.

> ⚠️ This project is educational software. It does not guarantee profits or a 99% win rate.

---

# ✨ Features

## 📊 Trading Dashboard

Modern desktop interface:

* Live BTC price
* BUY / SELL / WAIT signal
* Confidence percentage
* Technical indicator overview
* Dark trading interface

## 📈 Indicators

The system analyzes:

* RSI
* MACD
* EMA 50
* EMA 200
* Volume data

## 🤖 Telegram Alerts

Receive notifications:

Example:

```
🟢 BTC SIGNAL

BUY

Confidence:
92%

Price:
118500$

Indicators:

✓ RSI Bullish
✓ MACD Positive
✓ EMA Trend
```

---

# 🏗️ Installation

Clone:

```bash
git clone https://github.com/YOURNAME/pythonbtctradingsignalbot.git
```

Enter folder:

```bash
cd pythonbtctradingsignalbot
```

Create environment:

```bash
python -m venv .venv
```

Activate:

macOS:

```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

---

# ▶️ Start Application

Run:

```bash
python main.py
```

The BTC dashboard opens automatically.

---

# ⚙️ Configuration

Edit:

```
config.py
```

Example:

```python
SYMBOL="BTC/USDT"

TIMEFRAME="15m"

SIGNAL_THRESHOLD=85
```

Telegram:

```python
TELEGRAM_TOKEN="TOKEN"

CHAT_ID="ID"
```

---

# 🧠 Signal System

The bot uses a scoring model:

| Indicator | Points |
| --------- | ------ |
| RSI       | 25     |
| MACD      | 25     |
| EMA Trend | 25     |
| EMA Cross | 25     |

Example:

```
Score:

90%

Result:

STRONG BUY
```

---

# 🔮 Future Updates

Planned:

* Live candlestick charts
* AI prediction model
* Machine learning training
* Backtesting engine
* Portfolio tracker
* Automatic strategy optimization

---

# ⚠️ Risk Warning

Crypto trading is highly risky.

This software is only for:

* Learning
* Research
* Strategy testing

Never invest money you cannot afford to lose.

---

# 📜 License

MIT License
