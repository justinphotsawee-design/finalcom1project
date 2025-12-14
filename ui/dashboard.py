import customtkinter as ctk

# =========================
# UI Components
# =========================
from ui.title_bar import TitleBar
from ui.chart_panel import ChartPanel

# =========================
# Controller
# =========================
from controllers.controller import DataController

# =========================
# Cards
# =========================
from ui.cards.price_card import PriceCard
from ui.cards.recent_trade_card import RecentTradeCard
from ui.cards.volume_card import Volume24hCard
from ui.cards.signal_card import EMASignalCard


class Dashboard(ctk.CTk):
    """
    Dashboard
    =========
    Left  : Chart + EMA
    Right : Market Monitor (Realtime Cards)
    """

    def __init__(self):
        super().__init__()

        # =============================
        # WINDOW
        # =============================
        self.title("Dashboard")
        self.geometry("1200x800")
        self.minsize(1000, 600)
        self.configure(fg_color="#183039")

        # =============================
        # ROOT GRID
        # =============================
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # =============================
        # TITLE BAR
        # =============================
        TitleBar(self).grid(row=0, column=0, sticky="ew")

        # =============================
        # CONTENT
        # =============================
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(
            row=1, column=0,
            sticky="nsew",
            padx=12,
            pady=12
        )
        self.content_frame.grid_columnconfigure(0, weight=5)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # =============================
        # CONTROLLER
        # =============================
        self.controller = DataController(
            symbol="BTCUSDT",
            dashboard=self
        )

        # 🔑 bind loading hook
        self.controller.on_loading = self._set_loading

        self._build_left()
        self._build_right()
        self._build_loading_overlay()

        # initial load
        self.controller.change_symbol("BTCUSDT")

    # ======================================================
    # LOADING OVERLAY
    # ======================================================
    def _build_loading_overlay(self):
        self.loading_overlay = ctk.CTkFrame(
            self.content_frame,
            fg_color="#020506",
            corner_radius=12
        )

        self.loading_overlay.place(
            relx=0, rely=0,
            relwidth=1, relheight=1
        )
        self.loading_overlay.lift()
        self.loading_overlay.place_forget()

        self.loading_label = ctk.CTkLabel(
            self.loading_overlay,
            text="Loading market data...",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")

    def _set_loading(self, is_loading: bool):
        def _ui():
            if is_loading:
                self.loading_overlay.place(
                    relx=0, rely=0,
                    relwidth=1, relheight=1
                )
                self.loading_overlay.lift()
            else:
                self.loading_overlay.place_forget()

        self.after(0, _ui)

    # ======================================================
    # LEFT COLUMN
    # ======================================================
    def _build_left(self):
        self.left = ctk.CTkFrame(self.content_frame)
        self.left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.left.grid_rowconfigure(0, weight=0)
        self.left.grid_rowconfigure(1, weight=1)
        self.left.grid_rowconfigure(2, minsize=180, weight=0)
        self.left.grid_columnconfigure(0, weight=1)

        # -----------------------------
        # SYMBOL TABS
        # -----------------------------
        self.tabs = ctk.CTkTabview(
            self.left,
            height=0,
            corner_radius=0,
            fg_color="transparent"
        )
        self.tabs._segmented_button.configure(
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self._on_symbol_change
        )
        self.tabs.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        for s in ("BTC", "ETH", "SOL", "BNB", "XRP"):
            self.tabs.add(s)

        # -----------------------------
        # CHART
        # -----------------------------
        chart_box = ctk.CTkFrame(self.left)
        chart_box.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 8))

        self.chart = ChartPanel(
            chart_box,
            symbol="BTCUSDT",
            interval="1h",
            on_refresh=self._refresh_chart
        )
        self.chart.pack(fill="both", expand=True)

        self.controller.add_listener(self.chart)

        # -----------------------------
        # EMA PANEL
        # -----------------------------
        self._build_ema_panel()

    # ======================================================
    # EMA PANEL
    # ======================================================
    def _build_ema_panel(self):
        self.ema_container = ctk.CTkFrame(self.left, height=180)
        self.ema_container.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.ema_container.grid_propagate(False)
        self.ema_container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.ema_container,
            text="Use EMA",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(10, 8))

        self.edit_frame = ctk.CTkFrame(self.ema_container, fg_color="transparent")
        self.edit_frame.grid(row=1, column=0, sticky="nsew", padx=14)
        self.edit_frame.grid_columnconfigure(0, weight=1)

        self.ema_entry = ctk.CTkEntry(
            self.edit_frame,
            placeholder_text="e.g. 9, 21, 50",
            height=34
        )
        self.ema_entry.grid(row=0, column=0, sticky="ew")

        self.ema_status = ctk.CTkLabel(
            self.edit_frame,
            text="Enter positive integers separated by commas"
        )
        self.ema_status.grid(row=1, column=0, sticky="w", pady=(4, 8))

        btn_row = ctk.CTkFrame(self.edit_frame)
        btn_row.grid(row=2, column=0, sticky="w")

        ctk.CTkButton(
            btn_row, text="Apply", width=90,
            command=self._apply_ema
        ).grid(row=0, column=0, padx=(0, 8))

        ctk.CTkButton(
            btn_row, text="Disable", width=90,
            command=self._disable_ema
        ).grid(row=0, column=1)

    # ======================================================
    # RIGHT COLUMN
    # ======================================================
    def _build_right(self):
        self.right = ctk.CTkFrame(self.content_frame)
        self.right.grid(row=0, column=1, sticky="nsew")
        self.right.grid_rowconfigure(1, weight=1)
        self.right.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self.right, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Market Monitor",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Realtime market statistics & EMA signals",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        ).grid(row=1, column=0, sticky="w")

        self.card_stack = ctk.CTkFrame(self.right, fg_color="transparent")
        self.card_stack.grid(row=1, column=0, sticky="nsew", padx=10, pady=(4, 10))
        self.card_stack.grid_columnconfigure(0, weight=1)

        self.cards = [
            PriceCard(self.card_stack),
            RecentTradeCard(self.card_stack),
            Volume24hCard(self.card_stack),
            EMASignalCard(self.card_stack),
        ]

        for card in self.cards:
            card.pack(fill="x", pady=(0, 10))
            card.bind_controller(self.controller)

    # ======================================================
    # EMA CALLBACKS
    # ======================================================
    def _apply_ema(self):
        raw = self.ema_entry.get()
        periods = [int(x) for x in raw.split(",") if x.strip().isdigit()]

        if not periods:
            self.ema_status.configure(
                text="Invalid EMA. Use format like: 9, 21, 50",
                text_color="yellow"
            )
            return

        self.ema_status.configure(
            text=f"EMA applied: {', '.join(map(str, periods))}",
            text_color="green"
        )

        self.chart.set_ema(True, periods)

        for card in self.cards:
            if isinstance(card, EMASignalCard):
                card.set_ema_values(self.chart.get_last_ema_values())

    def _disable_ema(self):
        self.chart.set_ema(False, [])
        self.ema_status.configure(
            text="EMA disabled",
            text_color="gray70"
        )

        for card in self.cards:
            if isinstance(card, EMASignalCard):
                card.set_ema_values([])

    # ======================================================
    # SYMBOL CHANGE
    # ======================================================
    def _on_symbol_change(self, symbol):
        mapping = {
            "BTC": "BTCUSDT",
            "ETH": "ETHUSDT",
            "SOL": "SOLUSDT",
            "BNB": "BNBUSDT",
            "XRP": "XRPUSDT"
        }
        self.controller.change_symbol(mapping[symbol])
        self.chart.set_symbol(mapping[symbol])

    # ======================================================
    # REFRESH
    # ======================================================
    def _refresh_chart(self):
        self.controller.change_symbol(self.controller.symbol)
