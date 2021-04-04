# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os.path
from PIL import ImageTk, Image
import datetime
from tkcalendar import Calendar, DateEntry
import sys
from database.connections import db_transact #NOTE: use python -m frames.login_frame in order to circumvent relative import issue


#  ----- class inheriting from tk.Tk -----
class UserinfoWindow(tk.Frame):
    #  ----- initialize -----
    def __init__(self, parent, *args, **kwargs):
        super().__init__(None)

    # ----- Styles -----

        # colors

        # custom styles
        style = ttk.Style()
        style.theme_use("clam")
        f = tkFont.Font(family='helvetica', size=15)
        style.configure('Test.TFrame', font=f)

    # ----- customize -----

        # configure rows and columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # save todays date on attribute
        self.current_date = datetime.datetime.now().date()

        # parent/root frames;  HERE: the parent widget IS also the root widget (tk.TK) 
        self.root = self._root()

        # sign up user info
        self.user = self.root.signup_frame.username.get()
        self.pw = self.root.signup_frame.password.get()

        print(self.user, self.pw)


    #----- User Info Screen -----

        # initiate login screen
        uinfo = ttk.Frame(self, width=50)
        uinfo.grid(row=0,column=0, rowspan=7, columnspan=2, sticky='EWNS')
        uinfo.grid_columnconfigure(0, weight=1)
        uinfo.grid_columnconfigure(1, weight=1)
        for n in range(7):
            uinfo.grid_rowconfigure(n, weight=1)

        #Labels
        label_cont1 = tk.Frame(uinfo, bg=self.root.BG_COL_1)
        label_cont1.grid(row=0, rowspan=2, column=0, columnspan=2, padx =(5,5)) 
        label_cont1.grid_rowconfigure(0, weight=1)
        label_cont1.grid_columnconfigure(0, weight=1)
        ttk.Label(label_cont1, text=f'             Hi {self.user}', width=20, font=('MANIFESTO', 18)).grid(row=0, column=0, padx =(5,5)) 

        print(tk.font.families())

        # ------ Gender ------
        # initiate textvariables to fill in 
        self.gender = tk.StringVar(value=0)
        self.dob_day = tk.StringVar(value="Day")
        self.dob_month = tk.StringVar(value="Month")
        self.dob_year = tk.StringVar(value="Year")

        # Images
        work_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

        male_img = Image.open(os.path.join(work_folder,"media", "images", "male.png"))
        male_img = male_img.resize((100, 100), Image.ANTIALIAS)
        self.male_img = ImageTk.PhotoImage(male_img)

        female_img = Image.open(os.path.join(work_folder,"media", "images", "female.png"))
        female_img = female_img.resize((100, 150), Image.ANTIALIAS)
        self.female_img = ImageTk.PhotoImage(female_img)

        dob_img = Image.open(os.path.join(work_folder,"media", "images", "dob.png"))
        dob_img = dob_img.resize((75, 75), Image.ANTIALIAS)
        self.dob_img = ImageTk.PhotoImage(dob_img)

        #Buttons

        self.female_button = tk.Button(uinfo, command=self.female, image=self.female_img, borderwidth=0.5, fg='darkslateblue') #, relief='sunken'
        self.female_button.grid(row=3, rowspan=3, column=0, sticky="NSEW", pady =(5,5))
        self.changeOnHover(self.female_button, '#4936ba', 'darkslateblue', '#f8f7ff', 'whitesmoke') #change button color on hover

        self.male_button = tk.Button(uinfo, command=self.male, image=self.male_img, borderwidth=0.5, fg='darkslateblue') #
        self.male_button.grid(row=3, rowspan=3, column=1, sticky="NSEW", pady =(5,5))
        self.changeOnHover(self.male_button, '#4936ba', 'darkslateblue', '#f8f7ff', 'whitesmoke') #change button color on hover

        # --- DOB ---


        # Label
        self.dob_container = tk.Frame(uinfo, bg=self.root.BG_COL_1)  #container in order to be able to center correctly
        for n in range(3):
            self.dob_container.grid_rowconfigure(n, weight=1)
        for n in range(7):
            self.dob_container.grid_columnconfigure(n, weight=1)
        ttk.Label(self.dob_container, image=self.dob_img, width=20).grid(row=0, column=3, padx =(5,5)) 

        # Spinboxes
        curr_year = self.root.current_date.year

        self.selected_day = ttk.Combobox(self.dob_container, 
                    values=[i for i in range(32)], 
                    font=('MANIFESTO', 12), 
                    textvariable=self.dob_day, 
                    width=8
                    )
        self.selected_day.grid(row=2, rowspan=3, column=2, padx =(5,5))
        self.selected_day.bind("<<ComboboxSelected>>", self.check_dob)


        self.selected_month = ttk.Combobox(self.dob_container, 
                    values=[i for i in range(13)], 
                    font=('MANIFESTO', 12), 
                    textvariable=self.dob_month, 
                    width=8,
                    )
        self.selected_month.grid(row=2, rowspan=3, column=3, padx =(5,5))
        self.selected_month.bind("<<ComboboxSelected>>", self.check_dob)

        self.selected_year = ttk.Combobox(self.dob_container, 
                    values=[i for i in range(1950,curr_year+1)], 
                    font=('MANIFESTO', 12), 
                    textvariable=self.dob_year, 
                    width=8
                    )
        self.selected_year.grid(row=2, rowspan=3, column=4, padx =(5,5))
        self.selected_year.bind("<<ComboboxSelected>>", self.check_dob)

        # Button
        self.submit_button = tk.Button(uinfo, command=self.dob, text="NEXT", borderwidth=0, fg='blue', bg="#DCDAD5")
        self.changeOnHover(self.submit_button, 'red', 'blue') #change button color on hover


        

    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.destroy() #destroy window


    
    def male(self):
        self.gender.set('male')
        self.female_button.grid_forget()
        self.male_button.grid_forget()
        self.dob_container.grid(row=2,column=0, columnspan=2, sticky="EWNS", padx =(5,5))

    def female(self):
        self.gender.set('male')
        self.female_button.grid_forget()
        self.male_button.grid_forget()
        self.dob_container.grid(row=2,column=0, columnspan=2, sticky="EWNS", padx =(5,5)) 

        # ----- method changing button text/foreground color on hover
    def changeOnHover(self, button, fgColorOnHover, fgColorOnLeave, bgColorOnHover="#DCDAD5", bgColorOnLeave="#DCDAD5"): 
        def _modify(e, fgcol, bgcol):
            button.config(fg=fgcol)
            button.config(bg=bgcol)
        # background on cursor entering widget 
        button.bind("<Enter>", 
                    func=lambda e, fgcol=fgColorOnHover, bgcol=bgColorOnHover: _modify(e, fgcol, bgcol)
                    )  
            
        # background color on cursor leaving widget 
        button.bind("<Leave>", 
                    func=lambda e, fgcol=fgColorOnLeave, bgcol=bgColorOnLeave: _modify(e, fgcol, bgcol)
                    )  

    def sign_up(self, container):
        print("Switch to sign up page!")
        # indicate which frame to bring to front
        frame = self.frames[container]
        #brings indicated frame to the front
        frame.tkraise() 

    def check_dob(self, event):
        '''
        Callback function for dob-comboboxes.
        Checks if values were selected for all 3 Comboboxes and adds sumbit_button to grid if True.
        '''
        if self.dob_day.get() !="Day" and self.dob_month.get() !="Month" and self.dob_year.get() !="Year":
            self.submit_button.grid(row=4, column=0, columnspan=2, padx =(5,5), pady =(5,0))


    def dob(self):
        '''
        Function called on submit_button - click.

        '''
        print(self.dob_day.get(), self.dob_month.get(), self.dob_year.get())
        


