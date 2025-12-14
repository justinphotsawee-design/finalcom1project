from ui.dashboard import Dashboard
import customtkinter as ctk


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("./themes/breeze.json")
    app = Dashboard()
    app.mainloop()  