# controllers/controller.py
import threading
import time
import uuid

from utils.binance_rest import get_klines
from utils.binance_websocket import BinanceCombinedWS


class DataController:


    def __init__(self, symbol="BTCUSDT", dashboard=None):
        self.symbol = symbol.upper()
        self.dashboard = dashboard

        self.listeners = []
        self.ws = None
        self._session_id = None

        # 🔑 loading callback (Dashboard จะ set ให้)
        self.on_loading = None

    # ==================================================
    # Listener
    # ==================================================
    def add_listener(self, comp):
        self.listeners.append(comp)

    def _emit(self, method, payload, session_id):
        if session_id != self._session_id:
            return

        for c in self.listeners:
            if hasattr(c, method):
                try:
                    getattr(c, method)(payload)
                except Exception as e:
                    print(f"[Controller] {method} error:", e)

    # ==================================================
    # Symbol change (ENTRY POINT)
    # ==================================================
    def change_symbol(self, symbol):
        symbol = symbol.upper()
        print(f"[Controller] change_symbol → {symbol}")

        # 🔒 new session
        self._session_id = uuid.uuid4().hex

        # stop old WS
        if self.ws:
            try:
                self.ws.stop()
            except:
                pass
            self.ws = None

        self.symbol = symbol

        # reset UI
        for c in self.listeners:
            if hasattr(c, "update_symbol"):
                c.update_symbol(symbol)

        # 🔑 notify loading start
        if callable(self.on_loading):
            self.on_loading(True)

        # start worker thread
        threading.Thread(
            target=self._load_rest_then_ws,
            args=(self._session_id,),
            daemon=True
        ).start()

    # ==================================================
    # REST → WS (BACKGROUND THREAD)
    # ==================================================
    def _load_rest_then_ws(self, session_id):
        # ---------- REST (historical candles)
        while True:
            if session_id != self._session_id:
                return

            try:
                df = get_klines(self.symbol, "1h", 24)
                if df is not None and not df.empty:
                    break
            except:
                pass

            time.sleep(0.8)

        # send to chart
        self._emit("render_historical", df, session_id)

        # ---------- WS callbacks (SESSION SAFE)
        def trade_cb(trade):
            if session_id != self._session_id:
                return
            self._emit("update_trade", trade, session_id)

        def ticker_cb(ticker):
            if session_id != self._session_id:
                return

            # price → PriceCard / EMA / Signal
            price = ticker.get("last_price")
            if isinstance(price, (int, float)):
                self._emit("update_price", price, session_id)

            # full ticker → PriceCard / VolumeCard
            self._emit("update_ticker", ticker, session_id)

        # ---------- start WS
        self.ws = BinanceCombinedWS(
            symbol=self.symbol,
            on_trade=trade_cb,
            on_ticker=ticker_cb
        )
        self.ws.start()

        # 🔑 notify loading end (WS started)
        if callable(self.on_loading):
            self.on_loading(False)
