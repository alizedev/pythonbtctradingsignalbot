import statistics


class SignalScanner:

    def __init__(self):

        self.last_signal = "HOLD"

    def calculate_ema(self, prices, period=20):

        if len(prices) < period:
            return None

        multiplier = 2 / (period + 1)

        ema = prices[0]

        for price in prices[1:]:

            ema = ((price - ema) * multiplier) + ema

        return ema

    def calculate_rsi(self, prices, period=14):

        if len(prices) <= period:
            return 50

        gains = []

        losses = []

        for i in range(1, len(prices)):

            change = prices[i] - prices[i - 1]

            if change > 0:

                gains.append(change)
                losses.append(0)

            else:

                gains.append(0)
                losses.append(abs(change))

        avg_gain = statistics.mean(gains[-period:])

        avg_loss = statistics.mean(losses[-period:])

        if avg_loss == 0:

            return 100

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))

    def volume_strength(self, candles):

        volumes = [c["volume"] for c in candles]

        if len(volumes) < 10:

            return False

        avg = statistics.mean(volumes[:-1])

        return volumes[-1] > avg

    def scan(self, candles):

        if len(candles) < 25:

            return {"signal": "WAIT", "confidence": 0}

        closes = [c["close"] for c in candles]

        price = closes[-1]

        ema = self.calculate_ema(closes)

        rsi = self.calculate_rsi(closes)

        volume_ok = self.volume_strength(candles)

        buy_score = 0

        sell_score = 0

        # RSI

        if rsi < 35:

            buy_score += 30

        elif rsi > 70:

            sell_score += 30

        # Trend

        if price > ema:

            buy_score += 25

        else:

            sell_score += 25

        # Momentum

        if closes[-1] > closes[-5]:

            buy_score += 20

        else:

            sell_score += 20

        # Volume

        if volume_ok:

            buy_score += 15

            sell_score += 15

        if buy_score > sell_score:

            signal = "BUY"

            confidence = buy_score

        elif sell_score > buy_score:

            signal = "SELL"

            confidence = sell_score

        else:

            signal = "HOLD"

            confidence = 0

        result = {
            "signal": signal,
            "price": price,
            "rsi": round(rsi, 2),
            "ema": round(ema, 2),
            "confidence": min(confidence, 100),
        }

        self.last_signal = signal

        print("SIGNAL:", result)

        return result
