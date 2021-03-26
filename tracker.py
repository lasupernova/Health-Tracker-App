
# NOTE: tk.Frame does NOT have access to ttk.Notebook!
# --> convert tracker.py into a main.py instead!!!
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
from frames.signup_frame import SignupWindow
from frames.login_frame import LoginWindow

#  ----- class inheriting from tk.Tk -----
class InputWindow(tk.Tk):
    #  ----- initialize -----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ----- paths -----
        icon_path = f"media{os.sep}icons" #use os.sep for tracker to work in different OS
        # print(icon_path) #uncomment for troubleshooting
        self.img = ImageTk.PhotoImage(Image.open(f"media{os.sep}icons{os.sep}main.png"))

    # ----- Data ------
    #check for command line arguments
        if len(sys.argv) > 1:
            print(f"Currently running: {sys.argv[0]}")
            print(f"Data loading from: {sys.argv[1]}")
            self.tracker = sys.argv[1]
        else:
            print('No data...creating new Tracker-object.')
            self.tracker = ''


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
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        for n in range(20):
            self.grid_rowconfigure(n, weight=1)

        # save todays date on attribute
        self.current_date = datetime.datetime.now().date()

        # list to save EntryFrame objects in to use fot latter iterations
        self.entry_frames = []

        # variable to save info about loggin in user
        self.user = None

    # # ----- Frame Container -----

    #     # save a ttk frame - object in a variable named "container" 
    #     container = ttk.Frame(self) 
    #     container.grid() #position the frame in the parent widget in a grid
    #     container.columnconfigure(0, weight=1)

    #----- Login and SignUp Screen -----

        # add login frame that is placed within "container"
        self.login_frame = LoginWindow(self, self.switch_frame) #initiate Timer-class and pass self as the controller
        self.login_frame.grid(row=0,column=0, rowspan=20, sticky='EWNS') #configure timer frame placed in the first row and first column and to fill the entire frame ("container")

        # add signup frame 
        self.signup_frame = SignupWindow(self, self.switch_frame)
        self.signup_frame.grid(row=0,column=0, rowspan=20, sticky='EWNS')

    # ----- Tabs -----

        # initiate ttk.Notebook as parent for tabs
        self.tabControl = ttk.Notebook(self)#, style="Custom.TNotebook.Tab")

        # create tabs
        mood_tab = ttk.Frame(self.tabControl)
        health_tab = ttk.Frame(self.tabControl) #, relief = tk.SUNKEN
        sleep_tab = ttk.Frame(self.tabControl)
        food_tab = ttk.Frame(self.tabControl)
        fitness_tab = ttk.Frame(self.tabControl)
        period_tab = ttk.Frame(self.tabControl)
        longterm_tab = ttk.Frame(self.tabControl)
        self.all_tabs = [mood_tab, food_tab, fitness_tab, period_tab, longterm_tab, health_tab, sleep_tab]

        # add tabs
        self.tabControl.add(mood_tab, text='Mood')
        self.tabControl.add(health_tab, text='Health')
        self.tabControl.add(sleep_tab, text='Sleep')
        self.tabControl.add(food_tab, text='Food')
        self.tabControl.add(fitness_tab, text='Fitness')
        self.tabControl.add(period_tab, text='Period')
        self.tabControl.add(longterm_tab, text='Longterm Changes')

        # pack tabs - to make them visible 
        # tabControl.pack(expand=0, fill="both", pady=(10,10))
        self.tabControl.grid(row=0,column=0, rowspan=20, sticky='EWNS')
        self.tabControl.grid_columnconfigure(0, weight=1)
        for n in range(15):
            self.tabControl.grid_rowconfigure(n, weight=1)
        tk.Button(self,text="Change date NOW",command=self.change_date, borderwidth=0, fg='darkslateblue').grid(row=1,column=1,rowspan=1, sticky='N')
        # print(tabControl.tab(tabControl.select(), "text")) #uncomment for troubleshooting

    # ----- Labels ----- 
        fontLab = tkFont.Font(family='Verdana', size=40, weight='bold', slant='roman')
        ttk.Label(mood_tab,  text ="How's your head feeling? \n", font=fontLab).grid(row=0, column=0, columnspan=2)
        ttk.Label(food_tab,  text ="How's your stomach feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(fitness_tab,  text ="How's your muscles feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(period_tab,  text ="How's your uterus feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(longterm_tab,  text ="How have you been? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(health_tab,  text ="How's your body feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(sleep_tab,  text ="How's your ZZZZZZZs feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)

    # ----- Tracker df -----

        self.df = TrackerFrame(self.tracker) 

    #  ----- Entry -----

        EntryFrame(mood_tab, mood_info, self.tabControl.tab(mood_tab)['text'], self.df, name='mood_tab').grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(health_tab, health_info, self.tabControl.tab(health_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(food_tab, food_info, self.tabControl.tab(food_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(sleep_tab, sleep_info, self.tabControl.tab(sleep_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(fitness_tab, fitness_info, self.tabControl.tab(fitness_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(period_tab, period_info, self.tabControl.tab(period_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(longterm_tab, longterm_info, self.tabControl.tab(longterm_tab)['text'], self.df).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

        # current tab
        tabName = self.tabControl.select() #get name of current tab
        self.active_tab = self.tabControl.nametowidget(tabName) #the current tab is a frame that contains 3 children: a label, an EntryFrame = a Past_Entry_Frame

        # create dictionary to keep track of frames
        self.frames = dict()

        # add both frames to dict
        self.frames['LoginWindow'] = self.login_frame
        self.frames['SignupWindow'] = self.signup_frame
        self.frames['TC'] = self.tabControl

        # start with timer_frame in front
        self.switch_frame('LoginWindow')
        
    # ----- iterate over all notebook tabs -----
        for tab in self.all_tabs:

            # save each tab's EntryFrame object in list for latter use
            for child in tab.winfo_children():
                if child.winfo_class() == "Frame":
                    self.entry_frames.append(child)

            # get current notebook tab's text
            tab_name = self.tabControl.tab(tab)['text']

            # create tk.Canvas-objects as plotting area
            cur_tab = PastEntryFrame(tab, tab_name)
            cur_tab.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)
            cur_tab.display_plots(tab_name)

    # ----- Date Picker ------
        self.cal = DateEntry(self, width=12, background='darkblue',
                            foreground='white', borderwidth=2)

        # print([obj.winfo_name() for obj in self.entry_frames])


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

    def on_tab_change(self, event):
        import tkinter.messagebox as tkmb
        info_message = f"Event: {event}\nWidget:{event.widget}"
        print(self.tabControl.tab(self.tabControl.select(), "text"))

        #get EntryFrame of interest from current tab and insert tab data in database
        active_entryframe = self.active_tab.winfo_children()[1] 
        active_entryframe.insert_database(self.user, self.current_date)

        # change value of self.active_tab, as the tab was changed - done AFTER calling active_entryframe.insert_database(), otherwise the un-filled newly opened tab info is inserted to database
        tabName = self.tabControl.select() 
        self.active_tab = self.tabControl.nametowidget(tabName) 

        tkmb.showinfo("Tab Change!!!", info_message)

    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.df.save_frame() #save GUI-entries to .csv file
        self.destroy() #destroy window

    # ----- function that brings frame on the back to the front -----
    def switch_frame(self, container):
        # indicate which frame to bring to front
        frame = self.frames[container]
        #brings indicated frame to the front
        frame.tkraise() 
        print("WORKS!")
        print(f'User: {self.user}')

# ----- run app -----
if __name__ == '__main__':
    app = InputWindow() 

    app.mainloop()