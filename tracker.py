# ----- import libraries and  xxx ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from style.widget_style import Style

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
        ttk.Label(mood_tab,  text ="Mood Fields here! \n 🡓", font={'size':12}).pack()#.grid(column = 0,  row = 0, padx = 30, pady = 30)  
        ttk.Label(health_tab,  text ="Health Fields here! \n 🡓").grid(column = 0,  row = 0, padx = 30, pady = 30)  

    # ----- Options -----

        # list of all options to add as checkboxes
        self.mood_options = ['angry', 'anxious', 'calm', 'content', 'depressed', 'emotional', 'energetic', 'excited', 'frustrated', 'happy', 'hyper', 'moody', 'motivated', 'relaxed', 'sad', 'sensitive', 'stressed', 'tired']
        # initiate dict to save tk.Stringvar-objects to sabe checkbox states in
        self.mood_selections = {}
        # iterate over options and save tk.Stringvar object as value
        for option in self.mood_options:
            self.mood_selections[option] = tk.StringVar(value=0)


    #  ----- Entry -----

        # iterate over options nand create checkbutton for each option
        for option in self.mood_selections:
            # frame = ttk.Frame(mood_tab).pack(fill="both", anchor="w")
            ttk.Checkbutton(mood_tab,
                            text=option,
                            command=lambda x=option: self.check_mood(x), #lambda command refering to method in order to be able to pass current option name as variable
                            variable=self.mood_selections[option]).pack(anchor="w")

    # ----- Buttons -----
        test = ttk.Button(
            mood_tab,
            command=self.print_all_selected,
            text="Print Selection"
        )
        test.pack()

    # method printing current checkbutton state when clicked
    def check_mood(self, option):
        # print(self.angry_check.state())
        print(self.mood_selections[f"{option}"].get())

    # method printing all current checkbutton states
    def print_all_selected(self):
        for mood in self.mood_selections:
            print(mood,": ", self.mood_selections[mood].get())

# ----- run app -----
if __name__ == '__main__':
    app = InputWindow() 

    app.mainloop()