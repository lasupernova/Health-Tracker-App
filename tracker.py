# ----- import libraries and  xxx ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from style.widget_style import Style
from frames.entry_frames import EntryFrame
from assets.entry_information import *

#  ----- class inheriting from tk.Tk -----
class InputWindow(tk.Tk):
    #  ----- initialize -----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ----- paths -----
        icon_path = f"media{os.sep}icons" #use os.sep for tracker to work in different OS
        # print(icon_path) #uncomment for troubleshooting

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
        self.iconphoto(False, tk.PhotoImage(file=os.path.join(icon_path, "main.png"))) 

        # make fullscreen
        self.state('zoomed')

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

    # ----- Labels ----- 
        ttk.Label(mood_tab,  text ="How's your head feeling? \n", font={'size':12}).pack()
        ttk.Label(food_tab,  text ="How's your stomach feeling? \n", font={'size':12}).pack()
        ttk.Label(fitness_tab,  text ="How's your muscles feeling? \n", font={'size':12}).pack()
        ttk.Label(period_tab,  text ="How's your uterus feeling? \n", font={'size':12}).pack()
        ttk.Label(longterm_tab,  text ="How have you been? \n", font={'size':12}).pack()
        ttk.Label(health_tab,  text ="How's your body feeling? \n", font={'size':12}).pack()
        ttk.Label(sleep_tab,  text ="How's your ZZZZZZZs feeling? \n", font={'size':12}).pack()

    #  ----- Entry -----

        EntryFrame(mood_tab, mood_info).pack()
        EntryFrame(health_tab, health_info).pack()
        EntryFrame(food_tab, food_info)
        EntryFrame(sleep_tab, sleep_info)
        EntryFrame(fitness_tab, fitness_info)
        EntryFrame(period_tab, period_info)
        EntryFrame(longterm_tab, longterm_info)

# ----- run app -----
if __name__ == '__main__':
    app = InputWindow() 

    app.mainloop()