"""
TO DO: write loop to change information in ALL tabs based on date;
conditional to display retrieved information differently depending on input method;
try to not save EntryFrames in variables to change displayed info, but instead to retreive them based on .winfo_children() of the root window in tracker.py;
methods of relevance: tracker.py/change_date ; entry_frames.py/update_selection ; (dataframe.py/get_date)
""" 

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

        # configure rows and columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        for n in range(20):
            self.grid_rowconfigure(n, weight=1)

        # save todays date on attribute
        self.current_date = datetime.datetime.now().date()

        # list to save EntryFrame objects in to use fot latter iterations
        self.entry_frames = []

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
        tk.Button(self,text="Change date NOW",command=self.change_date, borderwidth=0, fg='darkslateblue').grid(row=1,column=1,rowspan=1, sticky='N')
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

        self.df = TrackerFrame('test_df.csv') 

    #  ----- Entry -----

        EntryFrame(mood_tab, mood_info, tabControl.tab(mood_tab)['text'], self.df, name='mood_tab').grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(health_tab, health_info, tabControl.tab(health_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(food_tab, food_info, tabControl.tab(food_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(sleep_tab, sleep_info, tabControl.tab(sleep_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(fitness_tab, fitness_info, tabControl.tab(fitness_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(period_tab, period_info, tabControl.tab(period_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(longterm_tab, longterm_info, tabControl.tab(longterm_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)


        # ----- Date Picker ------
        self.cal = DateEntry(self, width=12, background='darkblue',
                            foreground='white', borderwidth=2)
        

        # ----- iterate over all notebook tabs -----
        for tab in self.all_tabs:

            # save each tab's EntryFrame object in list for latter use
            for child in tab.winfo_children():
                if child.winfo_class() == "Frame":
                    self.entry_frames.append(child)

            # get current notebook tab's text
            tab_name = tabControl.tab(tab)['text']

            # create tk.Canvas-objects as plotting area
            cur_tab = PastEntryFrame(tab_name, tab)
            cur_tab.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)
            cur_tab.display_plots(tab_name)

        print([obj.winfo_name() for obj in self.entry_frames])


        # ----- method toggling date picker and printing selection ------
    def change_date(self):
        # function printing selected date from calendar
        def print_sel(e):
            try:
                old_date = self.current_date
            except:
                old_date = datetime.datetime.now().date()
            new_date = self.cal.get_date()
            self.current_date = new_date
            print(f"Date changed from {old_date} to {self.current_date}")
            date_string = self.current_date.strftime("%Y-%m-%d") #convert datetime object to string in order to be able to pass it to .loc[]
            # update all EntryFrame fields based on date
            for entry_frame in self.entry_frames:
                entry_frame.update_selection(date=date_string) 
        self.cal.bind("<<DateEntrySelected>>", print_sel) 

        # toggle (=pack/unpack) calendar if it exists 
        # try:
        if self.cal.winfo_ismapped():
            self.cal.grid_remove()
        else:
            self.cal.grid(row=3,column=1,rowspan=1, sticky='N')
            # # create and pack calendar if it does not yet exist and bind it to function
            # except AttributeError:
            #     # print(type(e).__name__)
            #     self.cal = DateEntry(self, width=12, background='darkblue',
            #                     foreground='white', borderwidth=2)
            #     self.cal.bind("<<DateEntrySelected>>", print_sel)    #run print_sel() on date entry selection
            #     self.cal.pack(padx=5, pady=5)   

    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.df.save_frame() #save GUI-entries to .csv file
        self.destroy() #destroy window

# ----- run app -----
if __name__ == '__main__':
    app = InputWindow() 

    app.mainloop()