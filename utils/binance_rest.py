# utils/binance_rest.py
import requests
import pandas as pd


def get_klines(symbol="BTCUSDT", interval="1h", limit=200):
    """Fetch historical kline data from Binance REST."""

    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}

    response = requests.get(url, params=params, timeout=5)
    raw = response.json()

    df = pd.DataFrame(
        raw,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_volume",
            "num_trades",
            "taker_buy_volume",
            "taker_buy_quote",
            "ignore",
        ],
    )

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.set_index("open_time", inplace=True)
    df = df.astype(float)

    return df


def get_24h_stats(symbol):
    """Optional REST call for stats."""
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}"
    return requests.get(url, timeout=5).json()

def get_24h_ticker(symbol):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    r = requests.get(url, params={"symbol": symbol})
    r.raise_for_status()
    return r.json()