# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from PIL import ImageTk, Image
import datetime
from tkcalendar import Calendar, DateEntry
import sys
from database.connections import db_transact #NOTE: use python -m frames.login_frame in order to circumvent relative import issue
# from signup_frame import SignupWindow


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
        self.grid_rowconfigure(1, weight=1)

        # save todays date on attribute
        self.current_date = datetime.datetime.now().date()

        # parent/root frames;  HERE: the parent widget IS also the root widget (tk.TK) 
        self.root = self._root()

        # sign up user info
        self.user = self.root.signup_frame.username.get()
        self.pw = self.root.signup_frame.password.get()

        print(self.user, self.pw)


    #----- Login Screen -----

        # initiate login screen
        uinfo = ttk.Frame(self, width=50)
        uinfo.grid(row=0,column=0, rowspan=7, columnspan=2, sticky='EWNS')
        uinfo.grid_columnconfigure(0, weight=1)
        uinfo.grid_columnconfigure(1, weight=1)
        for n in range(7):
            uinfo.grid_rowconfigure(n, weight=1)

        # initiate textvariables to fill in using Entryfields or labels
        self.gender = tk.StringVar(value=0)

        #Labels
        ttk.Label(uinfo, text=f'Hi {self.user}', width=20).grid(row=0, rowspan=2, column=0, columnspan=2, sticky="EWNS", padx =(5,5)) 

        #Buttons
        self.female_button = tk.Button(uinfo, command=self.female, text="Female",borderwidth=1, fg='darkslateblue')
        self.female_button.grid(row=3, rowspan=3, column=0, sticky="NSEW", pady =(5,5))
        self.changeOnHover(self.female_button, 'blue', 'darkslateblue', 'lavender', 'whitesmoke') #change button color on hover

        self.male_button = tk.Button(uinfo, command=self.male, text="Male",borderwidth=1, fg='darkslateblue')
        self.male_button.grid(row=3, rowspan=3, column=1, sticky="NSEW", pady =(5,5))
        self.changeOnHover(self.male_button, 'blue', 'darkslateblue', 'lavender', 'whitesmoke') #change button color on hover



    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.destroy() #destroy window

    def focus_in(event, field):
        field.delete(0,"end")

    def test(self, event):
        print("TEST!!!")
    
    def male(self):
        print("Male")

    def female(self):
        print("Female")

        # ----- method changing button text/foreground color on hover
    def changeOnHover(self, button, fgColorOnHover, fgColorOnLeave, bgColorOnHover, bgColorOnLeave): 
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


    def switch_frame_advanced(self, next_frame):
        self.warning.set("")  #reset warning message on tab switch
        self.reset_entry_fields()
        self.switch_frame(next_frame)


