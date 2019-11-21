import tkinter as tk
import logging

from layout import MainView

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1000x600")
    root.title("Level designer")
    root.mainloop()
