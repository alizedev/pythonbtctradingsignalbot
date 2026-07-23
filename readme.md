# ₿ Python BTC Trading Signal Bot

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![Binance](https://img.shields.io/badge/API-Binance-yellow)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)

---

# 📌 Overview

The **Python BTC Trading Signal Bot** is a modular Bitcoin trading dashboard.

The application combines:

- ₿ Bitcoin price tracking
- 📊 Trading dashboard
- 🔑 Binance API integration
- 📜 Live Binance trades
- 💰 Portfolio tracking
- 🤖 Trading controls
- 🐳 Docker deployment

---

# ✨ Features

## 📊 Dashboard

Displays:

```
₿ BTC PRICE

$67,420.50


💰 Portfolio

$1,250.00


📈 Signal

WAIT
```

---

## 🔑 Binance Integration

Supported:

- API Key authentication
- Secret Key authentication
- BTCUSDT ticker
- Account balance
- Trade history
- Market data


Binance permissions:

```
✅ Read Permission

✅ Spot Trading (optional)

❌ Withdraw disabled
```

---

# 📜 Trade History

Live Binance trades:

```
🆔 ID

💎 Coin

📈 Side

💰 Price

📦 Amount

💸 Fee

⏰ Time
```

Example:

```
🆔 12345

💎 BTCUSDT

🟢 BUY

💰 $67420.50

📦 0.010000 BTC

💸 0.00001 BTC

⏰ 2026-07-23
```

---

# 🖥 GUI

Built with:

- Python 3
- PyQt6
- Dark Mode


Tabs:

```
📊 Dashboard

🔑 Binance

🤖 Trading

📜 Trades
```

---

# 📂 Project Structure

```
pythonbtctradingsignalbot

│
├── app.py
├── gui.py
├── config.py
│
├── modules
│   └── binance.py
│
├── data
│   ├── binance.json
│   └── trades.json
│
├── Dockerfile
├── requirements.txt
│
├── README.md
├── release.md
├── changes.md
└── dbchangelog.md
```

---

# ⚙ Installation

## Clone

```bash
git clone https://github.com/alizedev/pythonbtctradingsignalbot.git

cd pythonbtctradingsignalbot
```

---

## Virtual Environment

```bash
python3 -m venv .venv
```

Activate:

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

# 📦 Install Requirements

```bash
pip install -r requirements.txt
```

---

# 🔑 Binance Setup

Create:

```
data/binance.json
```

Content:

```json
{
    "api_key":"YOUR_API_KEY",
    "secret_key":"YOUR_SECRET_KEY"
}
```

Never upload this file.

Add to:

```
.gitignore
```

---

# ▶ Start

```bash
python app.py
```

---

# 🐳 Docker

Build:

```bash
docker build -t btc-trading-bot .
```

Run:

```bash
docker run -d \
--name btc-bot \
--restart always \
btc-trading-bot
```

Supported:

- Linux VPS
- Raspberry Pi
- Server
- Cloud VM

---

# 🛣 Roadmap


## v1.0

✅ Dashboard

✅ Binance API

✅ BTC Price

✅ Trade History


## v1.1

⬜ RSI Signals

⬜ MACD

⬜ Moving Average

⬜ Telegram Alerts


## v1.2

⬜ Database

⬜ Backtesting

⬜ Automated Trading


---

# ⚠ Disclaimer

Educational project only.

Crypto trading contains financial risks.

Never trade money you cannot afford to lose.