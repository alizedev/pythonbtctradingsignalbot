def generate_signal(df):

    last = df.iloc[-1]

    score = 0

    # RSI
    if last.rsi < 35:
        score += 25

    # MACD
    if last.macd > last.signal:
        score += 25

    # Trend
    if last.close > last.ema200:
        score += 25

    # EMA Cross
    if last.ema50 > last.ema200:
        score += 25

    if score >= 85:

        return {"signal": "BUY", "confidence": score}

    elif score <= 20:

        return {"signal": "SELL", "confidence": score}

    return {"signal": "WAIT", "confidence": score}
