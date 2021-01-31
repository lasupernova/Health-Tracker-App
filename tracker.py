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
        tabControl.pack(expand=1, fill="both")

    # ----- Labels ----- 
        ttk.Label(mood_tab,  text ="Mood Fields here! \n 🡓", font={'size':12}).pack()#.grid(column = 0,  row = 0, padx = 30, pady = 30)  
        ttk.Label(health_tab,  text ="Health Fields here! \n 🡓").pack()

    # ----- Options -----

        # list of all options to add as checkboxes
        self.mood_options = ['angry', 'anxious', 'calm', 'content', 'depressed', 'emotional', 'energetic', 'excited', 'frustrated', 'happy', 'hyper', 'moody', 'motivated', 'relaxed', 'sad', 'sensitive', 'stressed', 'tired']
        
        self.food_options = ['animal products', 'cereal', 'cheats/sweets/unhealthy', 'enough water?', 'fruits', 'healthy', 'laxatives', 'supplements']

        self.fitness_options = ['cycling [mins]', 'gym', 'hiking', 'running/cardio [mins]', 'stretching [mins]']

        self.vaginal_options = ['cramps', 'cycle day', 'infection', 'ovulation', 'period', 'intercourse', 'spotting']

        self.longterm_changes_options = ['anatomical', 'climate', 'hormonal', 'nutritional', 'social']

        self.health_options = ['RHR', 'STDs', 'acidity', 'backache', 'bloating', 'breakouts', 'chestpain', 'constipation', 'defecation', 'diarrhea', 'dizziness', 'hard stool', 'headache', 'indigestion', 'medication', 'nausea', 'numbness', 'other symptoms', 'palpitations', 'panic attack', 'shortness of breath', 'sick?', 'stomachpain']

        self.sleep_options = ['REM', 'awake', 'deep sleep', 'frequent wakeups', 'insomnia', 'light sleep', 'sleep', 'sleep medication', 'sleep score', 'timezone change']

        all_lists = [self.mood_options, self.food_options, self.fitness_options, self.vaginal_options, self.longterm_changes_options, self.health_options, self.sleep_options]

        # initiate dict to save tk.Stringvar-objects to sabe checkbox states in
        self.mood_selections = {}
        self.food_selections = {}
        self.fitness_selections = {}
        self.vaginal_selections = {}
        self.longterm_changes_selections = {}
        self.health_selections = {}
        self.sleep_selections = {}
        all_topics = [self.mood_selections, self.food_selections, self.fitness_selections, self.vaginal_selections,self.longterm_changes_selections, self.health_selections, self.sleep_selections]

        # iterate over options and save tk.Stringvar object as value
        for topic, tab, options in zip(all_topics, all_tabs, all_lists):
            print(tab)
            for option in options:
                topic[option] = {}
                topic[option]["selection"] = tk.StringVar(value=0)
                topic[option]["frame"] = tk.Frame(tab)

    #  ----- Entry -----

        # iterate over tabs with correpsonding tk-objects (saved in all_topics) and options-lists
        for tab, topic, options in zip(all_tabs, all_topics, all_lists):
            # # iterate over options nand create checkbutton and label for each option
            for option in options:
                topic[option]["frame"].pack(anchor="w")
                ttk.Label(topic[option]["frame"],text=option, width=10).grid(row=0, column=0, sticky="W") #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                ttk.Checkbutton(topic[option]["frame"],
                                command=lambda x=(option, topic): self.check_options(x), #lambda command refering to method in order to be able to pass current option name as variable
                                variable=topic[option]["selection"] ).grid(row=0, column=1, sticky="W")

        # ----- Buttons -----
            test = ttk.Button(
                tab,
                command=lambda x=(options, topic): self.print_all_selected(x),
                text="Print Selection"
            )
            test.pack(anchor="w", pady =15)

    # method printing current checkbutton state when clicked
    def check_options(self, selection_choice):
        # extract clicked option and topic-dict from 'selection_choice'-parameter
        option, topic = self._get_selection_parameters(selection_choice)
        # print chackbutton state (=value of tk.Stringvar-object saved in topic-dict for current option)
        print(topic[option]["selection"].get())

    # method printing all current checkbutton states
    def print_all_selected(self, selection_choice):
        # extract clicked option and topic-dict from 'selection_choice'-parameter
        options, topic = self._get_selection_parameters(selection_choice)
        for option in options:
            print(option,": ", topic[option]["selection"].get())

    def _get_selection_parameters(self, selection_choice):
        option = selection_choice[0]
        topic = selection_choice[1]
        return option, topic




# ----- run app -----
if __name__ == '__main__':
    app = InputWindow() 

    app.mainloop()