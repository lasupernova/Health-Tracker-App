# ----- import libraries and  xxx ---
import tkinter as tk
# from tkinter import ttk
import os
from PIL import ImageTk, Image

class PastEntryFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # ----- Frames -----

        # create and place containing frame
        self["borderwidth"] = 1
        # self.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)

        # create canvas to place plots in
        self.C1 = tk.Canvas(self, borderwidth=1)
        self.C1.pack()
        self.C2 = tk.Canvas(self, borderwidth=1)
        self.C2.pack()

        # import image
        self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}images{os.sep}test.jpg").resize((200,200)))
        # self.img = self.img
        # img = Image.open(f"media{os.sep}images{os.sep}test.jpg")
        # img.show()
        self.C1.create_image(60,60, anchor="nw", image=self.img)
        self.C2.create_image(60,60, anchor="nw", image=self.img)