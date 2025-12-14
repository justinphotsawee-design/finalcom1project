import customtkinter as ctk


class BaseCard(ctk.CTkFrame):
    """
    BaseCard
    =========
    Base class for dashboard cards.
    """

    def __init__(
        self,
        parent,
        title: str = "",
        height: int = 120,
        corner_radius: int = 12,
        **kwargs
    ):
        super().__init__(
            parent,
            height=height,
            corner_radius=corner_radius,
            **kwargs
        )

        # prevent layout jump
        self.grid_propagate(False)
        self.pack_propagate(False)

        self.card_name = self.__class__.__name__
        self._controller = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # -----------------------------
        # HEADER
        # -----------------------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # -----------------------------
        # BODY
        # -----------------------------
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))
        self.body.grid_columnconfigure(0, weight=1)

        self.build_body()

    # =============================
    # Hooks (override)
    # =============================
    def build_body(self): pass
    def update_price(self, price): pass
    def update_trade(self, trade): pass
    def load_24h_open(self, price): pass
    def update_symbol(self, symbol): pass

    # =============================
    # Controller
    # =============================
    def bind_controller(self, controller):
        self._controller = controller
        if hasattr(controller, "add_listener"):
            controller.add_listener(self)

    # =============================
    # Safe UI update (THREAD SAFE)
    # =============================
    def safe(self, fn, *args, **kwargs):
        try:
            self.after(0, fn, *args, **kwargs)
        except RuntimeError:
            pass

    def safe_update(self, fn, *args, **kwargs):
        self.safe(fn, *args, **kwargs)
