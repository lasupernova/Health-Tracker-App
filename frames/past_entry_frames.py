# ----- import libraries and  xxx ---
import tkinter as tk
# from tkinter import ttk
import os
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PastEntryFrame(tk.Frame):
    def __init__(self, container, plot, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # ----- Frames -----

        # create and place containing frame
        self["borderwidth"] = 1
        # self.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)

        self.plot = plot

        # create canvas to place plots in
        self.C1 = tk.Canvas(self, borderwidth=1)
        self.C1.pack()
        # self.C2 = tk.Canvas(self, borderwidth=1)
        # self.C2.pack()

        # # import image
        self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}images{os.sep}test.jpg").resize((200,200)))
        # # self.img = self.img
        # # img = Image.open(f"media{os.sep}images{os.sep}test.jpg")
        # # img.show()
        self.C1.create_image(60,60, anchor="nw", image=self.img)
        canvas = FigureCanvasTkAgg(self.plot, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(anchor="center")