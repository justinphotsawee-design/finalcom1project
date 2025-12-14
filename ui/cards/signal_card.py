# ui/cards/signal_card.py
import customtkinter as ctk
from ui.cards.base_card import BaseCard


class EMASignalCard(BaseCard):
    def __init__(self, parent):
        self.last_price = None
        self.ema_values = []
        super().__init__(parent, title="EMA Signal")

    def build_body(self):
        self.label = ctk.CTkLabel(
            self.body,
            text="--",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label.pack(anchor="w")

    def update_price(self, price):
        self.last_price = price
        self._update()

    def set_ema_values(self, ema_values):
        self.ema_values = ema_values
        self._update()

    def _update(self):
        if not self.last_price or not self.ema_values:
            return

        above = all(self.last_price > e for e in self.ema_values)
        below = all(self.last_price < e for e in self.ema_values)

        if above:
            self.label.configure(text="BULLISH", text_color="green")
        elif below:
            self.label.configure(text="BEARISH", text_color="red")
        else:
            self.label.configure(text="NEUTRAL", text_color="gray")
