# To DO ; sleep plot does not show xticklabels correctly
#  TO DO: food buttons - if text is currently on display, show "click me" on hover
# TO DO: custom fonts (throughout app)

# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
# from tkinter import ttk
import os
import subprocess
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from .analysis.cycle import plot_cycle
# from.analysis.sleep import plot_sleep
# from .analysis.plots.test import make_plot
from media.plots.cycle import plot_cycle
from media.plots.sleep import plot_sleep
from media.plots.food import create_cloud
from helpers import change_color, changeOnHover

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
        self.root = self.winfo_toplevel()  #get root window/frame
        # print(self.tab_name)
        # self.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)

        # self.plot = plot
        # self.plot_cycle = plot_cycle

    def flip_tile(self, button):
        """
        'Flips' tile by changing button content from image to text and back.

        Parameters:
            button (tk.Button) - button to flip

        Returns:
            void function
        """
        food = button.cget('text').split()[0]
        image = button.cget('image')
        # print(food, ": ", image)  ##uncomment for troubleshooting
        if image != '':
            button.configure(image='')
            button.configure(height=13, width=42)  #manually determined by trial and error --> find better (more universal) way
        else:
            button.configure(image=self.button_dict[food]['image'])
            button.configure(height=200, width=298)


    def display_plots(self, tab_name):

        nothing_to_see = ttk.Label(self, 
                              name='nothing_to_see',
                              text='Nothing to see... yet', 
                              foreground='grey', 
                              background='whitesmoke', 
                              font=('MANIFESTO', 36))

        try:

            if tab_name == "Period":
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

                self.container = tk.Frame(self, borderwidth=0)
                self.container.pack()
                self.container.columnconfigure(0, weight=1)
                self.container.columnconfigure(1, weight=1)

                self.container.rowconfigure(0, weight=1)
                self.container.rowconfigure(1, weight=1)
                
                food_images  = ['unhealthy', 'non_vegan', 'fruits', 'cereal']
                grid_loc  = [(0, 0), (0, 1), (1, 0), (1, 1)]
                self.button_dict = {}
                for food, (row, col) in zip(food_images, grid_loc):
                    self.button_dict[food] = {}
                    # food data
                    self.button_dict[food]['image'] = ImageTk.PhotoImage(Image.open(f"media{os.sep}plots{os.sep}.archive{os.sep}{food}.png").resize((298,200)))
                    self.button_dict[food]['button'] = tk.Button(self.container, 
                                                                borderwidth=0,
                                                                text = f'{food}\n\n\n\n\t\t\tCLICK ME!', 
                                                                image = self.button_dict[food]['image'])  
                    self.button_dict[food]['button'].configure(command=lambda button_=self.button_dict[food]['button']:self.flip_tile(button_))
                    self.button_dict[food]['button'].grid(row=row, column=col, sticky="EW")
                    changeOnHover(self.button_dict[food]['button'], 'red', 'blue')
                
            else:
                # create canvas to place plots in
                self.C1 = tk.Canvas(self, borderwidth=1)
                self.C1.pack()

                # import image
                self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}images{os.sep}test.jpg").resize((200,200)))
                self.C1.create_image(60,60, anchor="nw", image=self.img)



        # print(container.children.keys())
        # print(tab_name) 
    

        except:
            ttk.Label(self, name='nothing_to_see',text='Nothing to see... yet', foreground='grey', background='whitesmoke').pack()
