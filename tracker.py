# ----- import libraries and  xxx ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os

#  ----- class inheriting from tk.Tk -----
class MainWindow(tk.Tk):
    #  ----- initialize -----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ----- paths -----
        icon_path = f"media{os.sep}icons" #use os.sep for tracker to work in different OS
        # print(icon_path) #uncomment for troubleshooting

    # ----- Styles -----

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
        mood_tab = ttk.Frame(tabControl, style="Test.TFrame")
        health_tab = ttk.Frame(tabControl, relief = tk.SUNKEN)
        sleep_tab = ttk.Frame(tabControl)
        food_tab = ttk.Frame(tabControl)
        fitness_tab = ttk.Frame(tabControl)
        period_tab = ttk.Frame(tabControl)
        longterm_tab = ttk.Frame(tabControl)

        # add tabs
        tabControl.add(mood_tab, text='Mood')
        tabControl.add(health_tab, text='Health')
        tabControl.add(sleep_tab, text='Sleep')
        tabControl.add(food_tab, text='Food')
        tabControl.add(fitness_tab, text='Fitness')
        tabControl.add(period_tab, text='Period')
        tabControl.add(longterm_tab, text='Longterm Changes')

        # pack tabs - to make them visible 
        tabControl.pack(expand=1, fill="both")

    # ----- Labels ----- 
        ttk.Label(mood_tab,  text ="Mood Fields here! \n 🡓", font={'size':12}).grid(column = 0,  row = 0, padx = 30, pady = 30)  
        ttk.Label(health_tab,  text ="Health Fields here! \n 🡓").grid(column = 0,  row = 0, padx = 30, pady = 30)  

# ----- run app -----
app = MainWindow() 

app.mainloop()