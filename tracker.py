# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from style.widget_style import Style
from frames.entry_frames import EntryFrame
from frames.past_entry_frames import PastEntryFrame
from assets.entry_information import *
from PIL import ImageTk, Image
from frames.analysis.dataframes.dataframe import TrackerFrame

#  ----- class inheriting from tk.Tk -----
class InputWindow(tk.Tk):
    #  ----- initialize -----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ----- paths -----
        icon_path = f"media{os.sep}icons" #use os.sep for tracker to work in different OS
        # print(icon_path) #uncomment for troubleshooting
        self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}icons{os.sep}main.png"))


    # ----- Styles -----

        style = Style(self)

        # colors

        # custom styles
        style = ttk.Style()
        style.theme_use("clam")
        f = tkFont.Font(family='helvetica', size=15)
        style.configure('Test.TFrame', font=f)
        # customed_style.configure('Custom.TNotebook.Tab', padding=[12, 12], font=('Helvetica', 10))

    # ----- customize -----

        # title
        self.title("Health Tracker")

        # change taskbar icon
        # self.iconphoto(False, ImageTk.PhotoImage(file=os.path.join(icon_path, "main.png"))) 
        self.iconphoto(False, self.img) 

        # make fullscreen
        self.state('zoomed')

        # closing function
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    # ----- Tabs -----

        # initiate ttk.Notebook as parent for tabs
        tabControl = ttk.Notebook(self)#, style="Custom.TNotebook.Tab")

        # create tabs
        mood_tab = ttk.Frame(tabControl)
        health_tab = ttk.Frame(tabControl) #, relief = tk.SUNKEN
        sleep_tab = ttk.Frame(tabControl)
        food_tab = ttk.Frame(tabControl)
        fitness_tab = ttk.Frame(tabControl)
        period_tab = ttk.Frame(tabControl)
        longterm_tab = ttk.Frame(tabControl)
        all_tabs = [mood_tab, food_tab, fitness_tab, period_tab, longterm_tab, health_tab, sleep_tab]

        # add tabs
        tabControl.add(mood_tab, text='Mood')
        tabControl.add(health_tab, text='Health')
        tabControl.add(sleep_tab, text='Sleep')
        tabControl.add(food_tab, text='Food')
        tabControl.add(fitness_tab, text='Fitness')
        tabControl.add(period_tab, text='Period')
        tabControl.add(longterm_tab, text='Longterm Changes')

        # pack tabs - to make them visible 
        tabControl.pack(expand=1, fill="both", pady=(10,10))
        # print(tabControl.tab(tabControl.select(), "text")) #uncomment for troubleshooting

    # ----- Labels ----- 
        ttk.Label(mood_tab,  text ="How's your head feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(food_tab,  text ="How's your stomach feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(fitness_tab,  text ="How's your muscles feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(period_tab,  text ="How's your uterus feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(longterm_tab,  text ="How have you been? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(health_tab,  text ="How's your body feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(sleep_tab,  text ="How's your ZZZZZZZs feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)

    # ----- Tracker df -----

        self.df = TrackerFrame('nono.csv') 

    #  ----- Entry -----

        EntryFrame(mood_tab, mood_info, tabControl.tab(mood_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(health_tab, health_info, tabControl.tab(health_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(food_tab, food_info, tabControl.tab(food_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(sleep_tab, sleep_info, tabControl.tab(sleep_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(fitness_tab, fitness_info, tabControl.tab(fitness_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(period_tab, period_info, tabControl.tab(period_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(longterm_tab, longterm_info, tabControl.tab(longterm_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

        for tab in all_tabs:
            # get current notebook tab's text
            tab_name = tabControl.tab(tab)['text']
            # create tk.Canvas-objects as plotting area
            cur_tab = PastEntryFrame(tab_name, tab)
            cur_tab.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)
            cur_tab.display_plots(tab_name)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1) 

    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.df.save_frame() #save GUI-entries to .csv file
        self.destroy() #destroy window

# ----- run app -----
if __name__ == '__main__':
    app = InputWindow() 

    app.mainloop()