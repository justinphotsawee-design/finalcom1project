import customtkinter as ctk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates


# ======================================================
# EMA helper (UNCHANGED)
# ======================================================
def compute_ema(values, period):
    ema = []
    k = 2 / (period + 1)
    for i, price in enumerate(values):
        ema.append(price if i == 0 else price * k + ema[-1] * (1 - k))
    return ema


# ======================================================
# ChartPanel
# ======================================================
class ChartPanel(ctk.CTkFrame):
    def __init__(self, parent, symbol="BTCUSDT", interval="1h", on_refresh=None):
        super().__init__(parent)

        self.symbol = symbol
        self.interval = interval
        self.on_refresh = on_refresh

        self.use_ema = False
        self.ema_periods = []
        self._last_df = None
        self._last_ema_values = []

        # =============================
        #  STYLE ZONE 
        # =============================
        self.COLOR_UP = "#16a34a"      # green
        self.COLOR_DOWN = "#dc2626"    # red
        self.COLOR_GRID = "#cbd5e1"    # light gray
        self.COLOR_BG = "#263f4f"

        self.GRID_ALPHA_PRICE = 0.7
        self.GRID_ALPHA_VOLUME = 0.3

        self._build_ui()

    # ==================================================
    # UI
    # ==================================================
    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ---------------- HEADER ----------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=6)
        header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            header,
            text=f"Historical Chart • {self.symbol} • 24h",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.time_label = ctk.CTkLabel(
            header,
            text="Last updated: --",
            text_color="gray70"
        )
        self.time_label.grid(row=0, column=1, padx=10)

        if self.on_refresh:
            ctk.CTkButton(
                header,
                text="Refresh",
                width=90,
                command=self.on_refresh
            ).grid(row=0, column=2)

        # ---------------- CHART ----------------
        chart_box = ctk.CTkFrame(self)
        chart_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.fig = Figure(figsize=(12, 4), dpi=120, facecolor=self.COLOR_BG)
        grid = self.fig.add_gridspec(4, 1)

        self.ax_price = self.fig.add_subplot(grid[:3, 0])
        self.ax_volume = self.fig.add_subplot(grid[3, 0], sharex=self.ax_price)

        # ----- GRID (NEW) -----
        self.ax_price.grid(True, linestyle="--", alpha=self.GRID_ALPHA_PRICE, color=self.COLOR_GRID)
        self.ax_volume.grid(True, linestyle="--", alpha=self.GRID_ALPHA_VOLUME, color=self.COLOR_GRID)

        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_box)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ==================================================
    # PUBLIC API (UNCHANGED)
    # ==================================================
    def set_symbol(self, symbol):
        self.symbol = symbol
        self.title_label.configure(text=f"Historical Chart • {self.symbol} • 24h")

    def set_ema(self, enabled, periods):
        self.use_ema = enabled
        self.ema_periods = periods
        if self._last_df is not None:
            self._render(self._last_df)

    def get_last_ema_values(self):
        return self._last_ema_values.copy()

    def render_historical(self, df):
        self._last_df = df
        self._render(df)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=f"Last updated: {now}")

    # ==================================================
    # RENDER (LOGIC UNCHANGED)
    # ==================================================
    def _render(self, df):
        self.ax_price.clear()
        self.ax_volume.clear()

        # re-apply grid after clear
        self.ax_price.grid(True, linestyle="--", alpha=self.GRID_ALPHA_PRICE, color=self.COLOR_GRID)
        self.ax_volume.grid(True, linestyle="--", alpha=self.GRID_ALPHA_VOLUME, color=self.COLOR_GRID)

        ts = list(df.index.map(mdates.date2num))
        o, h, l, c, v = (
            df["open"].tolist(),
            df["high"].tolist(),
            df["low"].tolist(),
            df["close"].tolist(),
            df["volume"].tolist()
        )

        for t, _o, _h, _l, _c, _v in zip(ts, o, h, l, c, v):
            color = self.COLOR_UP if _c >= _o else self.COLOR_DOWN

            self.ax_price.plot([t, t], [_l, _h], color=color, linewidth=1)
            self.ax_price.add_patch(
                Rectangle(
                    (t - 0.01, min(_o, _c)),
                    0.02,
                    max(abs(_c - _o), 1e-9),
                    facecolor=color,
                    edgecolor=color
                )
            )

            self.ax_volume.bar(t, _v, width=0.02, color=color, alpha=0.6)

        # ----- EMA -----
        self._last_ema_values = []
        if self.use_ema and self.ema_periods:
            for p in self.ema_periods:
                ema = compute_ema(c, p)
                self.ax_price.plot(ts, ema, linewidth=1.5, label=f"EMA {p}")
                self._last_ema_values.append(ema[-1])
            self.ax_price.legend(loc="upper left")

        # ----- AXIS -----
        self.ax_volume.set_xlabel("Time",color="white")
        self.ax_price.set_ylabel("Price",color="white")
        self.ax_volume.set_ylabel("Volume",color="white")
        self.ax_price.tick_params(axis="both", labelcolor="white")
        self.ax_volume.tick_params(axis="both", labelcolor="white")

        

        self.ax_volume.xaxis.set_major_formatter(
            mdates.DateFormatter("%m-%d %H:%M")
        )

        self.fig.autofmt_xdate()
        self.canvas.draw()
