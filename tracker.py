# TO DO: add daving all info to db to _on_exit()-method
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
# from frames.analysis.dataframes.dataframe import TrackerFrame
import datetime
from tkcalendar import Calendar, DateEntry
import sys
from frames.signup_frame import SignupWindow
from frames.login_frame import LoginWindow
from frames.userInfo_frame import UserinfoWindow
import database.connections.db_transact as db_transact

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
            # self.tracker = sys.argv[1]
        else:
            print('No data...creating new Tracker-object.')
            # self.tracker = ''


    # ----- Styles -----

        style = Style(self)

        # colors
        self.BG_COL_1 = "#DCDAD5"

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

        # variable to save info about user logging in
        self.user = None
        self.sex = None

    # # ----- Frame Container -----

    #     # save a ttk frame - object in a variable named "container" 
    #     container = ttk.Frame(self) 
    #     container.grid() #position the frame in the parent widget in a grid
    #     container.columnconfigure(0, weight=1)

    #----- Login and SignUp Screen -----

        # add login frame that is placed within "container"
        self.login_frame = LoginWindow(self) #initiate Timer-class and pass self as the controller #, self.switch_frame
        self.login_frame#.grid(row=0,column=0, rowspan=20, columnspan=2, sticky='EWNS') #configure timer frame placed in the first row and first column and to fill the entire frame ("container")

        # add signup frame 
        self.signup_frame = SignupWindow(self, name="signup")
        self.signup_frame#.grid(row=0,column=0, rowspan=20, columnspan=2, sticky='EWNS')

        # add signup frame 
        self.userinfo_frame = UserinfoWindow(self)

    # ----- Tabs -----

        # initiate ttk.Notebook as parent for tabs
        self.tabControl = ttk.Notebook(self)#, style="Custom.TNotebook.Tab")

        # create tabs
        self.mood_tab = ttk.Frame(self.tabControl)
        self.health_tab = ttk.Frame(self.tabControl) #, relief = tk.SUNKEN
        self.sleep_tab = ttk.Frame(self.tabControl)
        self.food_tab = ttk.Frame(self.tabControl)
        self.fitness_tab = ttk.Frame(self.tabControl)
        self.period_tab = ttk.Frame(self.tabControl)
        self.longterm_tab = ttk.Frame(self.tabControl)

        # add tabs
        self.tabControl.add(self.mood_tab, text='Mood')
        self.tabControl.add(self.health_tab, text='Health')
        self.tabControl.add(self.sleep_tab, text='Sleep')
        self.tabControl.add(self.food_tab, text='Food')
        self.tabControl.add(self.fitness_tab, text='Fitness')
        self.tabControl.add(self.period_tab, text='Period')
        self.tabControl.add(self.longterm_tab, text='Longterm Changes')

        # # pack tabs - to make them visible 
        # # tabControl.pack(expand=0, fill="both", pady=(10,10))
        # self.tabControl.grid(row=0,column=0, rowspan=20, sticky='EWNS')
        # self.tabControl.grid_columnconfigure(0, weight=1)
        # for n in range(15):
        #     self.tabControl.grid_rowconfigure(n, weight=1)
        # tk.Button(self,text="Change date NOW",command=self.change_date, borderwidth=0, fg='darkslateblue').grid(row=1,column=1,rowspan=1, sticky='N')
        # # print(tabControl.tab(tabControl.select(), "text")) #uncomment for troubleshooting

    # ----- Labels ----- 
        fontLab = tkFont.Font(family='Verdana', size=40, weight='bold', slant='roman')
        ttk.Label(self.mood_tab,  text ="How's your head feeling? \n", font=fontLab).grid(row=0, column=0, columnspan=2)
        ttk.Label(self.food_tab,  text ="How's your stomach feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(self.fitness_tab,  text ="How's your muscles feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(self.longterm_tab,  text ="How have you been? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(self.health_tab,  text ="How's your body feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(self.period_tab,  text ="How's your uterus feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        ttk.Label(self.sleep_tab,  text ="How's your ZZZZZZZs feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)

    #  ----- Entry -----

        EntryFrame(self.mood_tab, mood_info, self.tabControl.tab(self.mood_tab)['text'], name='mood_tab').grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(self.health_tab, health_info, self.tabControl.tab(self.health_tab)['text']).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(self.food_tab, food_info, self.tabControl.tab(self.food_tab)['text']).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(self.sleep_tab, sleep_info, self.tabControl.tab(self.sleep_tab)['text']).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(self.fitness_tab, fitness_info, self.tabControl.tab(self.fitness_tab)['text']).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(self.period_tab, period_info, self.tabControl.tab(self.period_tab)['text']).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        EntryFrame(self.longterm_tab, longterm_info, self.tabControl.tab(self.longterm_tab)['text']).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

        # if self.sex != 'male':
        #     period_tab = ttk.Frame(self.tabControl)
        #     self.tabControl.add(period_tab, text='Period')
        #     ttk.Label(period_tab,  text ="How's your uterus feeling? \n", font={'size':12}).grid(row=0, column=0, columnspan=2)
        #     EntryFrame(period_tab, period_info, self.tabControl.tab(period_tab)['text']).grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        #     self.all_tabs = [mood_tab, food_tab, fitness_tab, period_tab, longterm_tab, health_tab, sleep_tab]
        # else:
        #     self.all_tabs = [mood_tab, food_tab, fitness_tab, longterm_tab, health_tab, sleep_tab]

        self.all_tabs = [self.mood_tab, self.food_tab, self.fitness_tab, self.period_tab, self.longterm_tab, self.health_tab, self.sleep_tab]

        # current tab
        tabName = self.tabControl.select()  #get name of current tab
        self.active_tab = self.tabControl.nametowidget(tabName)  #get widget-object from widget name (string)

        # create dictionary to keep track of frames
        self.frames = dict()
        self.frames_visibility = dict()

        # add both frames to dict
        self.frames['LoginWindow'] = self.login_frame
        self.frames['SignupWindow'] = self.signup_frame
        self.frames['UinfoWindow'] = self.userinfo_frame
        self.frames['TC'] = self.tabControl

        # start with timer_frame in front
        self.switch_frame('LoginWindow')

        self.tabControl.grid(row=0,column=0, rowspan=20, sticky='EWNS')
        self.tabControl.grid_columnconfigure(0, weight=1)
        for n in range(15):
            self.tabControl.grid_rowconfigure(n, weight=1)

        self.date_button = tk.Button(self,text="Change date NOW",command=self.change_date, borderwidth=0, fg='darkslateblue')

    # ----- Date Picker ------
        self.cal = DateEntry(self, width=12, background='darkblue',
                            foreground='white', borderwidth=2)

        # print([obj.winfo_name() for obj in self.entry_frames])


    # function printing selected date from calendar
    def print_sel(self, event=None):
        """
        Changes selected data in Entryframes

        Parameters:
            event: event - not None when called by self.change_date(); None when called by self.reset_tracker()
        """
        if event:
            try:
                old_date = self.current_date
            except:
                old_date = datetime.datetime.now().date()
            new_date = self.cal.get_date()
            self.current_date = new_date
            print(f"Date changed from {old_date} to {self.current_date}")
        else:
            self.current_date = datetime.datetime.now().date()  

        date_string = self.current_date.strftime("%Y-%m-%d") #convert datetime object to string in order to be able to pass it to .loc[]
        # get data
        data = db_transact.query_data_by_date_and_user(date_string, self.user)
        # update all EntryFrame fields based on date
        for entry_frame in self.entry_frames:
            if type(data) != dict:  #check if any data was returned from database for specified date and user
                entry_frame.create_blank_entryframes()
            else:
                entry_frame.update_selection(data, date_string) 


        # ----- method toggling date picker and printing selection ------
    def change_date(self):

        self.cal.bind("<<DateEntrySelected>>", lambda event: self.print_sel(event=event))

        if self.cal.winfo_ismapped():
            self.cal.grid_remove()
        else:
            self.cal.grid(row=3,column=1,rowspan=1, sticky='N')


    def on_tab_change(self, *event):

        #get EntryFrame of interest from current tab (2nd child object in current tab)
        '''
        The current tab (saved in self.active_tab) is a custom object parameter is used to save info on current active tab outside of native tkinter functionality ).
        The active tab is a ttk.Frame-object, that contains 3 children: a label, an EntryFrame and a Past_Entry_Frame.
        --> below: get the 2nd child-object from active tab - this is an EntryFrame-type object
        '''
        active_entryframe = self.active_tab.winfo_children()[1]  

        # check if any information was entered in current EntryFrame (-> changes for each information field saved as TRUE-values in value_entry_record-property) 
        if any(v==True for v in active_entryframe.value_entry_record.values()):  #check for any True-values in active_entryframe.value_entry_record-dict
            # insert EntryFrame data in database and display success message
            active_entryframe.insert_database(self.user, self.current_date) 
            message = f"""Database table {active_entryframe.tab} filled with values"""
            # change all values in entry-dict back to False, in order to avoid unneccesary database connections when re-opening this tab
            active_entryframe.value_entry_record = {k: False for k in active_entryframe.value_entry_record}
            self.toplevel_message('Success!', message, 1500)

        # change value of self.active_tab, as the tab was changed - done AFTER calling active_entryframe.insert_database(), otherwise the un-filled newly opened tab info is inserted to database
        tabName = self.tabControl.select() 
        self.active_tab = self.tabControl.nametowidget(tabName) 
        # print(self.tabControl.tab(self.tabControl.select(), "text"))  #uncomment for troubleshooting


    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        print("Exiting app...")
        self.on_tab_change()  #save entries of last tab without tab change
        self.destroy()  #destroy window


    def add_plots(self):
        # ----- iterate over all notebook tabs -----
        for tab in self.all_tabs:

            # save each tab's EntryFrame object in list for latter use
            for child in tab.winfo_children():
                if child.winfo_class() == "EntryFrame":
                    self.entry_frames.append(child)

            # get current notebook tab's text
            tab_name = self.tabControl.tab(tab)['text']

            # create tk.Canvas-objects as plotting area
            cur_tab = PastEntryFrame(tab, tab_name)
            cur_tab.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)
            cur_tab.display_plots(tab_name)


    # ----- function that brings frame on the back to the front -----
    def switch_frame(self, container):

        # ungrid current frame --> to avoid seeing "background"-frame, as frames are of different size, to avoid seeing "background"-frame
        for fname, frame in self.frames.items():
            if frame.winfo_viewable():
                frame.grid_forget()
    
        # indicate which frame to bring to show
        frame = self.frames[container]

        # create UI if frame to switch to is 'TC' - important to load TC after login only and to directly load correct user data based on self.user
        if frame == self.frames['TC']:
            if self.sex == 'male':
                self.change_tab_state(self.period_tab)
            else:
                self.change_tab_state(self.period_tab, method="enable")
            self.add_plots()
            self.date_button.grid(row=1,column=1,rowspan=1, sticky='N')
            frame.grid(row=0,column=0, rowspan=20, sticky='EWNS') 
        else:
            frame.grid(row=0,column=0, rowspan=20, columnspan=2,sticky='EWNS') 

        #brings indicated frame to the front
        frame.tkraise()  #keep tk.raise() in addition to .grid_forget() as 'TC' is always loaded to grid


    def toplevel_message(self, title, message, duration):
        top = tk.Toplevel()
        top.title(title)
        tk.Message(top, text=message, padx=20, pady=20).pack()
        top.after(duration, top.destroy)

    
    def change_tab_state(self, tab, method="disable"):
        """
        Changes status of specified ttk.Notebook-tab.
        If state change to "enabled", the state needs to be checked, as enabling from hidden vs disabled status use different functions.

        Parameters:
            tab: variable name of tab (NOT a string) - e.g. mood_tab
            method: string - "disable" (default) or "hide" or "enable"

        Returns: Void function
        """

        if method == "disable":
            self.tabControl.tab(tab, state="disabled")
            print(self.tabControl.tab(tab)['state'])
        elif method == "hide":
            self.tabControl.hide(tab)
            print(self.tabControl.tab(tab)['state'])
        elif method == "enable":
            state = self.tabControl.tab(tab)['state']
            if state == "hidden":
                self.tabControl.add(tab)
            elif state == "disabled":
                self.tabControl.tab(tab, state="normal")


    def reset_tracker(self):
        """
        Resets tracker interface (=ttk.Notebook object) and tkcalendar.DateEntry-object, when switching between users.
        This method is run from LoginWindow-object.


        Returns: Void function
        """

        self.tabControl.select(0)  #make first tab current tab every time new TC loads
        self.current_date = datetime.datetime.now().date()  
        self.cal.set_date(self.current_date)  #reset DateEntry-object
        self.print_sel()

# ----- run app -----
if __name__ == '__main__':
    print("Opening app...")
    app = InputWindow() 

    app.mainloop()