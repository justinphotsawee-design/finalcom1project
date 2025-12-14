# utils/binance_websocket.py
import json
import threading
import websocket
import time


class BinanceCombinedWS:
    """
    Streams:
    - trade
    - ticker (24hr)
    """

    def __init__(self, symbol, on_trade=None, on_ticker=None):
        self.symbol = symbol.lower()
        self.on_trade = on_trade
        self.on_ticker = on_ticker

        self.ws = None
        self.running = False

    # ==================================================
    def _on_message(self, ws, message):
        try:
            msg = json.loads(message)
        except:
            return

        stream = msg.get("stream")
        data = msg.get("data")

        if not stream or not isinstance(data, dict):
            return

        # ---------- TRADE ----------
        if stream.endswith("@trade") and self.on_trade:
            try:
                trade = {
                    "price": float(data["p"]),
                    "qty": float(data["q"]),
                    "side": "sell" if data["m"] else "buy",
                    "trade_time": int(data["T"]),
                }
                self.on_trade(trade)
            except:
                pass

        # ---------- 24h TICKER ----------
        elif stream.endswith("@ticker") and self.on_ticker:
            try:
                ticker = {
                    "last_price": float(data["c"]),
                    "price_change": float(data["p"]),
                    "price_change_pct": float(data["P"]),
                    "volume": float(data["v"]),          # BASE volume (BTC)
                    "quote_volume": float(data["q"]),    # ✅ 24h Volume (USDT)
                }
                self.on_ticker(ticker)
            except:
                pass

    # ==================================================
    def _run(self):
        url = (
            "wss://stream.binance.com:9443/stream?"
            f"streams={self.symbol}@trade/{self.symbol}@ticker"
        )

        self.running = True

        while self.running:
            try:
                self.ws = websocket.WebSocketApp(
                    url,
                    on_message=self._on_message
                )
                self.ws.run_forever(ping_interval=20, ping_timeout=10)
            except:
                time.sleep(1)

    # ==================================================
    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self.running = False
        try:
            if self.ws:
                self.ws.close()
        except:
            pass
