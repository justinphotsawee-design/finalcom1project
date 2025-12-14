Binance REST Utilities
A lightweight Python utility for fetching cryptocurrency market data from the Binance REST API.
Designed for data analysis, trading bots, and research workflows using Pandas.
Features
 Fetch OHLCV (Kline / Candlestick) data
 Configurable symbol, interval, and history length
 Returns clean pandas.DataFrame objects
 Retrieve 24-hour market statistics
 No API key required (public endpoints)
Project Structure
.
├── main.py
├── requirements.txt
└── utils/
    └── binance_rest.py
Installation
Clone the repository
git clone <your-repo-url>
cd <your-project-folder>
Install dependencies
pip install -r requirements.txt
Recommended: use a virtual environment (venv or conda)
Usage
Run the application
python main.py
Example: Fetch Candlestick (Kline) Data
from utils.binance_rest import get_klines

df = get_klines(
    symbol="BTCUSDT",
    interval="1h",
    limit=200
)

print(df.head())
Fetch 24-Hour Statistics
from utils.binance_rest import get_24h_stats

stats = get_24h_stats("BTCUSDT")
print(stats)
Fetch 24-Hour Ticker (With HTTP Validation)
from utils.binance_rest import get_24h_ticker

ticker = get_24h_ticker("BTCUSDT")
print(ticker)
This function uses raise_for_status() and will raise an exception if the API request fails.
