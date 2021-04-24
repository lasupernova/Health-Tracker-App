# TO DO: Figure out why app does not close after closing window !!!!
# To DO ; sleep plot does not show xticklabels correctly

# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
# from tkinter import ttk
import os
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from .analysis.cycle import plot_cycle
# from.analysis.sleep import plot_sleep
# from .analysis.plots.test import make_plot
from media.plots.cycle import plot_cycle
from media.plots.sleep import plot_sleep
from media.plots.food import create_cloud

BG_COLOR = "whitesmoke"

class PastEntryFrame(tk.Frame):
    def __init__(self, container, tab_name, *args, **kwargs):
        # self.tc = tabcontrol
        self.tab_name = tab_name
        super().__init__(container, *args, **kwargs)

        # ----- Frames -----

        # create and place containing frame
        self["borderwidth"] = 1
        self.container = container
        self.user = self.container.master.master.user   # get value for 'user'-parameter of main frame (=container's grandparent)
        self.date = self.container.master.master.current_date   # get value for 'current_date'-parameter of main frame (=container's grandparent)

        # print(self.tab_name)
        # self.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)

        # self.plot = plot
        # self.plot_cycle = plot_cycle

    def display_plots(self, tab_name):

        nothing_to_see = ttk.Label(self, 
                              name='nothing_to_see',
                              text='Nothing to see... yet', 
                              foreground='grey', 
                              background='whitesmoke', 
                              font=('MANIFESTO', 36))

        try:

            if tab_name == "Period":
                pass
            # https://stackoverflow.com/questions/50846947/interference-between-the-matplotlib-graphs-in-tkinter-gui
            # https://stackoverflow.com/questions/55542813/tkinter-plt-figure-does-not-plot-but-figure-does
            # https://stackoverflow.com/questions/17535766/tkinter-matplotlib-backend-conflict-causes-infinite-mainloop
            # http://staff.ltam.lu/feljc/software/python/matplotlib_tkinter.pdf
                # # get plot 
                if plot_cycle(self.user, self.date) == -1:
                    nothing_to_see.pack()

                self.plot = plot_cycle(self.user, self.date)

                # create canvas, add plot, pack + draw
                self.canvas = FigureCanvasTkAgg(self.plot, master=self)
                self.canvas.get_tk_widget().pack()
                self.canvas.draw()


            elif tab_name == "Sleep":

                if plot_sleep(self.user, self.date) == -1:
                    nothing_to_see.pack()

                self.plot = plot_sleep(self.user, self.date)

                # create canvas, add plot, pack + draw
                self.canvas = FigureCanvasTkAgg(self.plot, master=self)
                self.canvas.get_tk_widget().pack()
                self.canvas.draw()

            elif tab_name == "Food":

                # if plot_sleep(self.user, self.date) == -1:
                #     nothing_to_see.pack()

                # self.plot = plot_sleep(self.user, self.date)

                # create cloud and save to png
                os.system('python media\plots\\food.py')
                print(os.getcwd())
                print(">>>WORKS!")
                # create canvas to place plots in
                self.C1 = tk.Canvas(self, borderwidth=1, bg=BG_COLOR)
                self.C1.pack()

                # import image
                self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}plots{os.sep}.archive{os.sep}new2.png").resize((300,200)))

                self.C1.create_image(60,60, anchor="nw", image=self.img)


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

        except:
            ttk.Label(self, name='nothing_to_see',text='Nothing to see... yet', foreground='grey', background='whitesmoke').pack()
