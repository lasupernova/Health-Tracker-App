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
        self.grid_rowconfigure(1, weight=1)

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
        ttk.Label(uinfo, text=f'Hi {self.user}', width=20).grid(row=0, rowspan=2, column=0, columnspan=2, sticky="EWNS", padx =(5,5)) 


        # ------ Gender ------
        # initiate textvariables to fill in 
        self.gender = tk.StringVar(value=0)

        # Images
        work_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

        male_img = Image.open(os.path.join(work_folder,"media", "images", "male.png"))
        male_img = male_img.resize((100, 100), Image.ANTIALIAS)
        self.male_img = ImageTk.PhotoImage(male_img)

        female_img = Image.open(os.path.join(work_folder,"media", "images", "female.png"))
        female_img = female_img.resize((100, 150), Image.ANTIALIAS)
        self.female_img = ImageTk.PhotoImage(female_img)

        #Buttons
        self.female_button = tk.Button(uinfo, command=self.female, borderwidth=0.25, fg='darkslateblue')
        self.female_button.config(image=self.female_img,width="10",height="10")
        self.female_button.grid(row=3, rowspan=3, column=0, sticky="NSEW", pady =(5,5))
        self.changeOnHover(self.female_button, '#4936ba', 'darkslateblue', '#f8f7ff', 'whitesmoke') #change button color on hover

        self.male_button = tk.Button(uinfo, command=self.male, image=self.male_img, borderwidth=0.25, fg='darkslateblue')
        self.male_button.grid(row=3, rowspan=3, column=1, sticky="NSEW", pady =(5,5))
        self.changeOnHover(self.male_button, '#4936ba', 'darkslateblue', '#f8f7ff', 'whitesmoke') #change button color on hover



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


