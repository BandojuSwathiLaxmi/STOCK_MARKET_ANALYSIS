"""
predict.py  ·  QuantEdge AI Price Predictor
Fallback implementation using sklearn LinearRegression on technical features.
Replace this file with your own model to customize predictions.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')


def predict_stock(ticker: str) -> float:
    """
    Predict the next closing price for a given ticker symbol.

    Returns
    -------
    float
        Predicted next close price.
    """
    df = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.dropna(inplace=True)
    close = df['Close'].squeeze()

    # ── Features ──────────────────────────────────
    # SMA
    df['SMA_20'] = close.rolling(20).mean()
    df['SMA_50'] = close.rolling(50).mean()

    # RSI
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    df['RSI'] = 100 - (100 / (1 + gain / loss))

    # MACD
    df['MACD']   = close.ewm(span=12).mean() - close.ewm(span=26).mean()
    df['Signal'] = df['MACD'].ewm(span=9).mean()

    # ATR
    high, low = df['High'].squeeze(), df['Low'].squeeze()
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(14).mean()

    # BB width
    df['BB_Width'] = (
        close.rolling(20).std() * 4 / close.rolling(20).mean()
    )

    # Lag features
    for lag in [1, 2, 3, 5, 10]:
        df[f'lag_{lag}'] = close.shift(lag)

    # ── Model ─────────────────────────────────────
    feature_cols = [
        'SMA_20', 'SMA_50', 'RSI', 'MACD', 'Signal',
        'ATR', 'BB_Width',
        'lag_1', 'lag_2', 'lag_3', 'lag_5', 'lag_10'
    ]

    df.dropna(inplace=True)
    X = df[feature_cols].values
    y = close.loc[df.index].values

    model = LinearRegression()
    model.fit(X, y)

    last_row = df[feature_cols].iloc[-1].values.reshape(1, -1)
    predicted = float(model.predict(last_row)[0])

    return predicted