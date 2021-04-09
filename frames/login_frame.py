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
class LoginWindow(tk.Frame):
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
        # customed_style.configure('Custom.TNotebook.Tab', padding=[12, 12], font=('Helvetica', 10))

    # ----- customize -----

        # configure rows and columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # save todays date on attribute
        self.current_date = datetime.datetime.now().date()

        # parent frame
        self.parent = parent

    #----- Login Screen -----

        # initiate login screen
        login = ttk.Frame(self, width=50)
        login.grid(row=0,column=0, rowspan=7, columnspan=2, sticky='EWNS')
        login.grid_columnconfigure(0, weight=1)
        login.grid_columnconfigure(1, weight=1)
        for n in range(7):
            login.grid_rowconfigure(n, weight=1)

        # initiate textvariables to fill in using Entryfields or labels
        self.username = tk.StringVar(value='Username')
        self.password = tk.StringVar(value='Password')
        self.warning = tk.StringVar(value=None)

        # label
        ttk.Label(login, text='Log into your account', width=17).grid(row=0, column=0, sticky="NSEW", padx =(5,5)) 
        ttk.Label(login, textvariable=self.warning, foreground='red').grid(row=3, column=0, sticky="N", columnspan=2, padx =(5,5)) 

        #lbl.grid_forget()


        # Entry-fields 
        self.user_entry = tk.Entry(login,textvariable=self.username)
        self.user_entry.grid(row=1, column=0, sticky="NSEW", columnspan=2, padx =(5,5), pady =(5,0)) 
        self.user_entry.bind("<FocusIn>", lambda event, field=self.user_entry: self.focus_in(field))
        self.user_entry.bind("<FocusOut>", lambda event, field=self.user_entry, field_name='username': self.focus_out(event, field, field_name))
        self.user_entry.bind("<Return>", self.check_credentials)

        self.pw_entry = tk.Entry(login,textvariable=self.password, show="*")
        self.pw_entry.grid(row=2, column=0, sticky="NSEW", columnspan=2, padx =(5,5), pady =(5,0)) 
        self.pw_entry.bind("<FocusIn>", lambda event, field=self.pw_entry: self.focus_in(field))
        self.pw_entry.bind("<FocusOut>", lambda event, field=self.pw_entry, field_name='password': self.focus_out(event, field, field_name))
        self.pw_entry.bind("<Return>", self.check_credentials)

        #Buttons
        self.submit_button = tk.Button(login, command=self.check_credentials, text="Login",borderwidth=1, fg='darkslateblue')
        self.submit_button.grid(row=4, column=0, sticky="NSEW", columnspan=2, padx =(5,5), pady =(5,5))
        self.changeOnHover(self.submit_button, 'blue', 'darkslateblue') #change button color on hover - use function to bind events for re-use (below)

        self.signup_button = tk.Button(login, command=lambda: self.switch_frame_advanced('SignupWindow'), text="Sign Up", borderwidth=0, fg='blue', bg="#DCDAD5")
        self.signup_button.grid(row=5, column=0, sticky="NEW", padx =(5,5), pady =(5,0))
        self.changeOnHover(self.signup_button, 'red', 'blue')

        self.forgotPW_button = tk.Button(login, command=self.forgot_pw, text="Forgot Password", borderwidth=0, fg='blue', bg="#DCDAD5")
        self.forgotPW_button.grid(row=5, column=1, sticky="NEW", padx =(5,5), pady =(5,0))
        self.changeOnHover(self.forgotPW_button, 'red', 'blue')

        # while True:
        #     if self.winfo_viewable():



    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.destroy() #destroy window

    def focus_in(event, field):
        field.delete(0,"end")
        # usercheck=True

    def test(self, event):
        print("TEST!!!")
    
    def focus_out(self, event, field, field_name):
        '''
        Get's inserted value on focus out or adds placeholder prompting for input if no input was given;
        Works for both the username and the password - fields
        '''
        def process_input(text_var, field, field_name):
            if text_var != '' and text_var!='0' and text_var!=0:
                return text_var
            else:
                field.insert(0, f"I said ENTER {field_name.upper()}!")
                return 
                
        text_var = field.get()
        process_input(text_var, field, field_name)
        

        # ----- method changing button text/foreground color on hover
    def changeOnHover(self, button, colorOnHover, colorOnLeave): 
        # background on cursor entering widget 
        button.bind("<Enter>", 
                    func=lambda e: button.config(fg=colorOnHover) 
                    ) 
            
        # background color on cursor leaving widget 
        button.bind("<Leave>", 
                    func=lambda e: button.config(fg=colorOnLeave)
                    )  

    def check_credentials(self, event=None):
        print(event)
        user = self.username.get()
        pw= self.password.get()
        status = db_transact.login_user(user, pw)
        print('Logged in!' if status==1 else 'Wrong password!' if status==0 else 'User does not exist!' if status==-1 else 'Unknown error!')
        if status == 1:
            self.parent.user = user  #save logged in user to main tracker frame
            self.parent.sex = db_transact.get_gender(user)
            print(">>> Sex determined: ",self.parent.sex)
            self.parent.switch_frame('TC')  #To DO: once df data is loaded into database -> load user data into TC-frame
            self.parent.tabControl.bind("<<NotebookTabChanged>>", self.parent.on_tab_change)
        elif status == 0:
            self.warning.set("Wrong Password, please try again!") #pop-up label with 'wrong password' here
            self.reset_entry_fields()
        elif status == -1:
            self.warning.set("User not found!") #pop-up label with 'user not found' here
            self.reset_entry_fields()

    def sign_up(self, container):
        print("Switch to sign up page!")
        # indicate which frame to bring to front
        frame = self.frames[container]
        #brings indicated frame to the front
        frame.tkraise() 
        # if timer is not running, automatically reset time on frame change to changes times
        if not self.timer_frame.timer_running:
            self.timer_frame.reset_timer()  

    def forgot_pw(self):
        print("Switch to password recovery page!")

    def switch_frame_advanced(self, next_frame):
        self.warning.set("")  #reset warning message on tab switch
        self.reset_entry_fields()
        self.parent.switch_frame(next_frame)

    def reset_entry_fields(self):
        self.username.set("Username")
        self.password.set("Password")

