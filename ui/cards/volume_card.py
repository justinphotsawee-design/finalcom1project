import customtkinter as ctk
from ui.cards.base_card import BaseCard


def format_volume(v: float) -> str:
    """
    Format large volume numbers
    """
    if v >= 1_000_000_000:
        return f"{v / 1_000_000_000:.2f} B"
    if v >= 1_000_000:
        return f"{v / 1_000_000:.2f} M"
    if v >= 1_000:
        return f"{v / 1_000:.2f} K"
    return f"{v:,.0f}"


class Volume24hCard(BaseCard):
    """
    Volume24hCard
    ==============
    - Shows 24h trading volume (QUOTE VOLUME)
    - Source: WS TICKER ONLY
    - Unit: USDT
    """

    def __init__(self, parent):
        self.symbol = None
        super().__init__(parent, title="Volume 24h")

    # ======================================================
    # UI
    # ======================================================
    def build_body(self):
        self.vol_label = ctk.CTkLabel(
            self.body,
            text="--",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="gray70"
        )
        self.vol_label.grid(row=0, column=0, sticky="w")

        self.unit_label = ctk.CTkLabel(
            self.body,
            text="USDT (24h)",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        )
        self.unit_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

    # ======================================================
    # SYMBOL CHANGE → RESET
    # ======================================================
    def update_symbol(self, symbol):
        self.symbol = symbol

        self.safe(
            lambda: self.vol_label.configure(
                text="--",
                text_color="gray70"
            )
        )

    # ======================================================
    # WS → TICKER UPDATE (SOURCE OF TRUTH)
    # ======================================================
    def update_ticker(self, ticker):
        """
        ticker must contain:
        - quote_volume (USDT)
        """
        try:
            volume = float(
                ticker.get("quote_volume")
                or ticker.get("quoteVolume")
            )
        except:
            return

        formatted = format_volume(volume)

        def _ui():
            self.vol_label.configure(
                text=formatted,
                text_color="white"
            )

        self.safe(_ui)
