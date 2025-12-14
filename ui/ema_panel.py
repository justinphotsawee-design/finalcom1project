import customtkinter as ctk


class EMAPanel(ctk.CTkFrame):
    """
    EMA Control Panel
    - Edit EMA periods
    - Apply replaces existing EMA
    - Disable removes EMA
    """

    def __init__(self, parent, chart):
        super().__init__(parent, corner_radius=12)

        self.chart = chart
        self.grid_columnconfigure(1, weight=1)

        # ==================================================
        # TITLE
        # ==================================================
        ctk.CTkLabel(
            self,
            text="Use EMA",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=14,
            pady=(14, 6)
        )

        # ==================================================
        # INPUT ROW
        # ==================================================
        ctk.CTkLabel(
            self,
            text="Periods",
            font=ctk.CTkFont(size=14),
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(14, 6)
        )

        self.entry_periods = ctk.CTkEntry(
            self,
            placeholder_text="e.g. 9, 21, 50",
            height=34,
            font=ctk.CTkFont(size=14)
        )
        self.entry_periods.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=6
        )

        # ==================================================
        # BUTTONS
        # ==================================================
        btn_box = ctk.CTkFrame(self)
        btn_box.grid(
            row=1,
            column=2,
            padx=(6, 14)
        )

        self.apply_btn = ctk.CTkButton(
            btn_box,
            text="Apply",
            width=90,
            height=34,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.apply_ema
        )
        self.apply_btn.pack(side="top", pady=(0, 6))

        self.disable_btn = ctk.CTkButton(
            btn_box,
            text="Disable",
            width=90,
            height=34,
            command=self.disable_ema
        )
        self.disable_btn.pack(side="top")

        # ==================================================
        # HELPER TEXT
        # ==================================================
        self.helper_label = ctk.CTkLabel(
            self,
            text=(
                "Enter EMA periods as positive integers, separated by commas.\n"
                "Example: 9, 21 or 9, 21, 50"
            ),
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        self.helper_label.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="w",
            padx=14,
            pady=(4, 8)
        )

        # ==================================================
        # STATUS
        # ==================================================
        self.status_label = ctk.CTkLabel(
            self,
            text="EMA not applied",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="w",
            padx=14,
            pady=(0, 14)
        )

    # ==================================================
    # ACTIONS
    # ==================================================
    def apply_ema(self):
        raw = self.entry_periods.get().strip()

        periods = [
            int(p)
            for p in raw.split(",")
            if p.strip().isdigit() and int(p.strip()) > 0
        ]

        if not periods:
            self.status_label.configure(
                text="Invalid input. Please enter comma-separated positive numbers (e.g. 9, 21)."
            )
            return

        # Apply / replace EMA
        self.chart.set_ema(True, periods)

        self.status_label.configure(
            text=f"EMA applied: {', '.join(map(str, periods))}"
        )

    def disable_ema(self):
        self.chart.set_ema(False, [])
        self.status_label.configure(
            text="EMA disabled"
        )
