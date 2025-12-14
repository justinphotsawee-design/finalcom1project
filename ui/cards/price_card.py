# ui/cards/price_card.py
import customtkinter as ctk
from ui.cards.base_card import BaseCard


class PriceCard(BaseCard):
    """
    PriceCard
    =========
    - Shows LAST PRICE
    - Shows % CHANGE 24H
    - Source:
        - ticker → main source
        - trade price → realtime override
    """

    def __init__(self, parent):
        self.symbol = None
        self.last_price = None  
        super().__init__(parent, title="Last Price")

    # ==================================================
    # UI
    # ==================================================
    def build_body(self):
        self.price_label = ctk.CTkLabel(
            self.body,
            text="--",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.price_label.grid(row=0, column=0, sticky="w")

        self.change_label = ctk.CTkLabel(
            self.body,
            text="24h: --",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        self.change_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

    # ==================================================
    # SYMBOL CHANGE → RESET
    # ==================================================
    def update_symbol(self, symbol: str):
        self.symbol = symbol
        self.last_price = None

        def _ui():
            self.price_label.configure(text="--")
            self.change_label.configure(
                text="24h: --",
                text_color="gray70"
            )

        self.safe_update(_ui)

    # ==================================================
    # TICKER UPDATE (PRIMARY SOURCE)
    # ==================================================
    def update_ticker(self, ticker: dict):
        """
        ticker = {
            last_price,
            price_change,
            price_change_pct,
            volume
        }
        """
        try:
            price = float(ticker["last_price"])
            diff = float(ticker["price_change"])
            pct = float(ticker["price_change_pct"])
        except Exception:
            return

        self.last_price = price
        color = "green" if diff >= 0 else "red"

        def _ui():
            self.price_label.configure(text=f"{price:,.2f}")
            self.change_label.configure(
                text=f"24h: {diff:+,.2f} ({pct:+.2f}%)",
                text_color=color
            )

        self.safe_update(_ui)

    # ==================================================
    # TRADE PRICE UPDATE (REALTIME)
    # ==================================================
    def update_price(self, price):
        try:
            price = float(price)
        except Exception:
            return

        self.last_price = price

        def _ui():
            self.price_label.configure(text=f"{price:,.2f}")

        self.safe_update(_ui)
