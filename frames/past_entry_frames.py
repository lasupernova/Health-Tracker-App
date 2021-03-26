# TO DO: Figure out why app does not close after closing window; sleep plot does not show xticklabels correctly

# ----- import libraries and  modules ---
import tkinter as tk
# from tkinter import ttk
import os
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from .analysis.cycle import plot_cycle
# from.analysis.sleep import plot_sleep
# from .analysis.plots.test import make_plot

class PastEntryFrame(tk.Frame):
    def __init__(self, container, tab_name, *args, **kwargs):
        # self.tc = tabcontrol
        self.tab_name = tab_name
        super().__init__(container, *args, **kwargs)

        # ----- Frames -----

        # create and place containing frame
        self["borderwidth"] = 1
        # print(self.tab_name)
        # self.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)

        # self.plot = plot
        # self.plot_cycle = plot_cycle

    def display_plots(self, tab_name):

        if tab_name == "Period":
            # create canvas to place plots in
            self.C1 = tk.Canvas(self, borderwidth=1)
            self.C1.pack()
            # self.C2 = tk.Canvas(self, borderwidth=1)
            # self.C2.pack()

            # import image
            self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}images{os.sep}test.jpg").resize((200,200)))
            # add image to C1
            self.C1.create_image(60,60, anchor="nw", image=self.img)

            # # display custom plot
            # canvas = FigureCanvasTkAgg(plot_cycle(), master=self)
            # canvas.draw()
            # canvas.get_tk_widget().pack(anchor="center")

        elif tab_name == "Sleep":
            # create canvas to place plots in
            self.C1 = tk.Canvas(self, borderwidth=1)
            self.C1.pack()
            # self.C2 = tk.Canvas(self, borderwidth=1)
            # self.C2.pack()

            # import image
            self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}images{os.sep}test.jpg").resize((200,200)))
            # add image to C1
            self.C1.create_image(60,60, anchor="nw", image=self.img)

            # # display custom plot
            # canvas = FigureCanvasTkAgg(plot_sleep(period=14), master=self)
            # canvas.draw()
            # canvas.get_tk_widget().pack(anchor="center")

        else:
            # create canvas to place plots in
            self.C1 = tk.Canvas(self, borderwidth=1)
            self.C1.pack()
            # self.C2 = tk.Canvas(self, borderwidth=1)
            # self.C2.pack()

            # import image
            self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}images{os.sep}test.jpg").resize((200,200)))
            # # self.img = self.img
            # # img = Image.open(f"media{os.sep}images{os.sep}test.jpg")
            # # img.show()
            self.C1.create_image(60,60, anchor="nw", image=self.img)


            # canvas = FigureCanvasTkAgg(make_plot(), master=self)
            # canvas.draw()
            # canvas.get_tk_widget().pack(anchor="center")

    # print(container.children.keys())
    # print(tab_name) 
  
  
        # if tab_name == "Period":
        #     canvas = FigureCanvasTkAgg(self.plot_cycle, master=self)
        #     canvas.draw()
        #     canvas.get_tk_widget().pack(anchor="center")