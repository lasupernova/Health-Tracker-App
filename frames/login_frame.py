# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from PIL import ImageTk, Image
import datetime
from tkcalendar import Calendar, DateEntry
import sys

#  ----- class inheriting from tk.Tk -----
class LoginWindow(tk.Tk):
    #  ----- initialize -----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self.title("Log In")

        # make fullscreen
        self.state('zoomed')

        # closing function
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # configure rows and columns
        self.grid_columnconfigure(0, weight=1)
        for n in range(7):
            self.grid_rowconfigure(n, weight=1)

        # save todays date on attribute
        self.current_date = datetime.datetime.now().date()

    #----- Login Screen -----

        # initiate login screen
        login = ttk.Frame(self)
        login.grid(row=0,column=0, rowspan=7, sticky='EWNS')
        login.grid_columnconfigure(0, weight=1)

        # initiate textvariables to fill in using Entryfields
        self.username = tk.StringVar(value='Username')
        self.password = tk.StringVar(value='Password')

        # fill
        ttk.Label(login, text='Log into your account', width=17).grid(row=0, column=0, sticky="NSEW", padx =(5,5)) 

        user_entry = tk.Entry(login,textvariable=self.username)
        user_entry.grid(row=1, column=0, sticky="NSEW", padx =(5,5), pady =(5,0)) 
        user_entry.bind("<FocusIn>", lambda event, field=user_entry: self.focus_in(field))
        user_entry.bind("<FocusOut>", lambda event, field=user_entry, field_name='username': self.focus_out(event, field, field_name))

        pw_entry = tk.Entry(login,textvariable=self.password)
        pw_entry.grid(row=2, column=0, sticky="NSEW", padx =(5,5), pady =(5,0)) 
        pw_entry.bind("<FocusIn>", lambda event, field=pw_entry: self.focus_in(field))
        pw_entry.bind("<FocusOut>", lambda event, field=pw_entry, field_name='password': self.focus_out(event, field, field_name))


    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.destroy() #destroy window

    def focus_in(event, field):
        field.delete(0,"end")
        # usercheck=True
    
    def focus_out(self, event, field, field_name):

        def process_input(text_var, field_name):
            if text_var != '':
                return text_var
            else:
                if field_name=='username':
                    field.insert(0, "I said ENTER USERNAME!")
                elif field_name=='password':
                    field.insert(0, "I said ENTER PASSWORD!")
                return False

        if field_name=='username':
            text_var = self.username.get() #field.cget("textvariable")
            user = process_input(text_var, field_name)
            print(f"Username: {user}")
        elif field_name=='password':
            text_var = self.password.get() #field.cget("textvariable")
            pw = process_input(text_var, field_name)
            print(f"Password: {pw}")
        # if
        # field.delete(0,"end")
        # # usercheck=True

# ----- run app -----
if __name__ == '__main__':
    app = LoginWindow() 

    app.mainloop()