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
import datetime
from tkcalendar import Calendar, DateEntry
import sys

#  ----- class inheriting from tk.Tk -----
class InputWindow(tk.Tk):
    #  ----- initialize -----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

            # configure rows and columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        for n in range(20):
            self.grid_rowconfigure(n, weight=1)

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
        self.all_tabs = [mood_tab, food_tab, fitness_tab, period_tab, longterm_tab, health_tab, sleep_tab]

        # add tabs
        tabControl.add(mood_tab, text='Mood')
        tabControl.add(health_tab, text='Health')
        tabControl.add(sleep_tab, text='Sleep')
        tabControl.add(food_tab, text='Food')
        tabControl.add(fitness_tab, text='Fitness')
        tabControl.add(period_tab, text='Period')
        tabControl.add(longterm_tab, text='Longterm Changes')

        # pack tabs - to make them visible 
        # tabControl.pack(expand=0, fill="both", pady=(10,10))
        tabControl.grid(row=0,column=0, rowspan=20, sticky='EWNS')
        tabControl.grid_columnconfigure(0, weight=1)
        for n in range(15):
            tabControl.grid_rowconfigure(n, weight=1)


# ----- run app -----
if __name__ == '__main__':
    app = InputWindow() 

    app.mainloop()