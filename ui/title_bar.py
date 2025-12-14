import customtkinter as ctk


class TitleBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            height=64,
            fg_color="#183039",
            corner_radius=0
        )
        self.grid_propagate(False)

        # =========================
        # GRID
        # =========================
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # =========================
        # LEFT : TITLE STACK
        # =========================
        left = ctk.CTkFrame(self, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w", padx=20)

        self.title_label = ctk.CTkLabel(
            left,
            text="Crypto Dashboard",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            left,
            text="Historical Price with EMA Crossover",
            font=ctk.CTkFont(size=13),
            text_color="gray60"
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        # =========================
        # RIGHT : STATUS BAR
        # =========================
        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, sticky="e", padx=20)

        status_row = ctk.CTkFrame(right, fg_color="transparent")
        status_row.pack(anchor="e")

        # LIVE DOT
        self.live_dot = ctk.CTkLabel(
            status_row,
            text="●",
            font=ctk.CTkFont(size=14),
            text_color="#ff4d4f"
        )
        self.live_dot.pack(side="left", padx=(0, 6))

        self.live_text = ctk.CTkLabel(
            status_row,
            text="LIVE",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ff4d4f"
        )
        self.live_text.pack(side="left")

        # divider
        ctk.CTkLabel(
            status_row,
            text="|",
            font=ctk.CTkFont(size=14),
            text_color="gray50"
        ).pack(side="left", padx=10)

        self.connection_label = ctk.CTkLabel(
            status_row,
            text="Connected",
            font=ctk.CTkFont(size=13),
            text_color="#3a9f41"
        )
        self.connection_label.pack(side="left")
