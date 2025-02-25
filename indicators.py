# indicators.py
import pandas as pd
import numpy as np

def calculate_indicators(prices):
    if len(prices) < 20:
        return None

    df = pd.DataFrame(prices, columns=["close"])
    df["EMA"] = df["close"].ewm(span=20, adjust=False).mean()
    df["MA"] = df["close"].rolling(window=20).mean()
    df["MA75"] = df["close"].rolling(window=75).mean()
    df["MA150"] = df["close"].rolling(window=150).mean()

    # Cálculo do RSI
    delta = df["close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Cálculo do MACD
    short_ema = df["close"].ewm(span=12, adjust=False).mean()
    long_ema = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = short_ema - long_ema
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df.dropna()  # Remove as linhas sem dados suficientes para os indicadores
