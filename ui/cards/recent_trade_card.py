# ui/cards/recent_trade_card.py
import customtkinter as ctk
from ui.cards.base_card import BaseCard


class RecentTradeCard(BaseCard):
    """
    RecentTradeCard
    ===============
    - Shows LAST TRADE price only
    """

    def __init__(self, parent):
        self.symbol = None
        self.last_price = None
        self.side = None
        super().__init__(parent, title="Recent Trade")

    def build_body(self):
        self.trade_label = ctk.CTkLabel(
            self.body,
            text="--",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="gray70"
        )
        self.trade_label.grid(row=0, column=0, sticky="w")

    def update_symbol(self, symbol: str):
        self.symbol = symbol
        self.last_price = None
        self.side = None

        self.safe_update(
            lambda: self.trade_label.configure(
                text="--",
                text_color="gray70"
            )
        )

    def update_trade(self, trade):
        try:
            price = float(trade["price"])
            side = trade["side"]
        except:
            return

        color = "green" if side == "buy" else "red"

        def _ui():
            self.trade_label.configure(
                text=f"{price:,.2f}",
                text_color=color
            )

        self.safe_update(_ui)


