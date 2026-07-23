# ₿ Python BTC Trading Signal Bot

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![Binance](https://img.shields.io/badge/API-Binance-yellow)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)
![ARM64](https://img.shields.io/badge/Raspberry%20Pi%205-ARM64-red)
![License](https://img.shields.io/badge/License-MIT-green)


---

# 📌 Overview

The **Python BTC Trading Signal Bot** is a modular Bitcoin trading dashboard with Binance integration.

The project provides a complete monitoring environment for Bitcoin prices, trades and portfolio information.

Designed for:

- 🖥 Desktop usage
- 🐳 Docker deployment
- 🍓 Raspberry Pi 5 24/7 operation
- 🐧 Linux servers


---

# ✨ Features


## 📊 Trading Dashboard

Modern PyQt6 dark interface.


Displays:

```
₿ BTC PRICE

$67,420.50


💰 Portfolio

$1,250.00


📈 Signal

WAIT
```


Features:

- Dark Mode
- Live price display
- Portfolio overview
- Trading controls
- Market monitoring



---

# 🔑 Binance Integration


Connected through Binance API.


Supported:

- API authentication
- BTCUSDT ticker
- Account balance
- Trade history
- Market data
- Trading interface



## Binance Security


Recommended permissions:

```
✅ Read permission

✅ Spot Trading (optional)

❌ Withdraw disabled
```


Never share:

```
API Secret Key
```



---

# 📜 Binance Trade History


The dashboard displays Binance trades.


Table:


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

# 🖥 Application Interface


Tabs:


```
📊 Dashboard

🔑 Binance

🤖 Trading

📜 Trades
```


Technology:

- Python 3
- PyQt6
- Binance API
- JSON Storage
- Docker


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
├── docker-compose.yml
├── requirements.txt
│
├── README.md
├── release.md
├── changes.md
└── dbchangelog.md
```


---

# ⚙ Installation


## Requirements


Install:


- Python 3.11+
- pip
- Git



---

# Clone Repository


```bash
git clone https://github.com/alizedev/pythonbtctradingsignalbot.git

cd pythonbtctradingsignalbot
```



---

# Python Virtual Environment


Create:


```bash
python3 -m venv .venv
```


Activate:


## macOS / Linux


```bash
source .venv/bin/activate
```


## Windows


```bash
.venv\Scripts\activate
```



---

# Install Dependencies


```bash
pip install -r requirements.txt
```



---

# 🔑 Binance Configuration


Create:


```
data/binance.json
```


Example:


```json
{
    "api_key":"YOUR_BINANCE_API_KEY",
    "secret_key":"YOUR_BINANCE_SECRET_KEY"
}
```


Security:


Add:


```
data/binance.json
```


to:


```
.gitignore
```



---

# ▶ Start Application


Run:


```bash
python app.py
```



---

# 🐳 Docker Support


The application supports Docker deployment.


Benefits:


- Automatic restart
- Isolated environment
- Server operation
- 24/7 runtime



---

# Docker Build


Build image:


```bash
docker build -t btc-trading-bot .
```



---

# Docker Run


Start container:


```bash
docker run -d \
--name btc-bot \
--restart always \
-v $(pwd)/data:/app/data \
btc-trading-bot
```



Explanation:


```
--restart always

Automatically restarts bot


-v data:/app/data

Keeps API keys and trades
```



---

# 🍓 Raspberry Pi 5 Setup


The bot supports:


```
Raspberry Pi 5

ARM64

Raspberry Pi OS 64-bit

Ubuntu ARM64

Debian ARM64
```



Recommended hardware:


```
Raspberry Pi 5

8GB RAM

128GB SSD

Active Cooling
```



---

# Install Docker on Raspberry Pi


Update:


```bash
sudo apt update

sudo apt upgrade -y
```


Install Docker:


```bash
curl -fsSL https://get.docker.com | sh
```


Add user:


```bash
sudo usermod -aG docker $USER
```


Restart:


```bash
sudo reboot
```



Check:


```bash
docker --version
```



---

# Raspberry Pi Deployment


Clone project:


```bash
git clone https://github.com/alizedev/pythonbtctradingsignalbot.git

cd pythonbtctradingsignalbot
```



Create data folder:


```bash
mkdir data
```



Add Binance keys:


```
data/binance.json
```



---

# Build ARM64 Image


```bash
docker build \
--platform linux/arm64 \
-t btc-trading-bot .
```



---

# Run Raspberry Pi Container


```bash
docker run -d \
--name btc-bot \
--restart always \
-v $(pwd)/data:/app/data \
btc-trading-bot
```



---

# Docker Compose


Start:


```bash
docker compose up -d
```



Stop:


```bash
docker compose down
```



---

# 📊 Monitoring


Container status:


```bash
docker ps
```


Logs:


```bash
docker logs -f btc-bot
```



Restart:


```bash
docker restart btc-bot
```



---

# 🔄 24/7 Operation


Startup sequence:


```
Raspberry Pi Boot

        ↓

Docker Engine

        ↓

BTC Bot Container

        ↓

Binance Connection

        ↓

Price Monitoring
```



No monitor required.


---

# 🧩 Headless Mode


The bot can run without GUI:


Supported:

- Linux Server
- Raspberry Pi
- VPS
- Home Server


Future:

- Web Dashboard
- Telegram Alerts
- Remote Control



---

# 🛣 Roadmap


# v1.0

✅ Dashboard

✅ Binance API

✅ BTC Price

✅ Trade History



# v1.1

⬜ Raspberry Pi 5 Support

⬜ Docker Deployment

⬜ Telegram Notifications

⬜ SQLite Database



# v1.2

⬜ RSI Signals

⬜ MACD

⬜ Backtesting

⬜ Automated Trading



---

# ⚠ Disclaimer


This project is for educational purposes only.


Cryptocurrency trading involves financial risk.


Never trade money you cannot afford to lose.


---

# 👨‍💻 Author


Created by:

**alizedev**


GitHub:

```
https://github.com/alizedev
```