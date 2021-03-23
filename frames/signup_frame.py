# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from PIL import ImageTk, Image
import datetime
from tkcalendar import Calendar, DateEntry
import sys
from database.connections import db_transact #NOTE: use python -m frames.login_frame in order to circumvent relative import issue OR add to tracker.py script in root directory and run from there


#  ----- class inheriting from tk.Tk -----
class SignupWindow(tk.Frame):
    #  ----- initialize -----
    def __init__(self, parent, switch_frame, *args, **kwargs):
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

        self.switch_frame = switch_frame

        # # title
        # self.title("Log In")

        # # make fullscreen
        # # self.state('zoomed')

        # # set size
        # self.geometry("300x200")

        # # closing function
        # self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # configure rows and columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # save todays date on attribute
        self.current_date = datetime.datetime.now().date()

    #----- Login Screen -----

        # initiate login screen
        signup = ttk.Frame(self, width=50)
        signup.grid(row=0,column=0, rowspan=7, columnspan=2, sticky='EWNS')
        signup.grid_columnconfigure(0, weight=1)
        signup.grid_columnconfigure(1, weight=1)
        for n in range(7):
            signup.grid_rowconfigure(n, weight=1)

        # initiate textvariables to fill in using Entryfields
        self.username = tk.StringVar(value='Username')
        self.password = tk.StringVar(value='Password')
        self.warning = tk.StringVar(value=None)

        # label
        ttk.Label(signup, text='Sign Up', width=17).grid(row=0, column=0, sticky="NSEW", padx =(5,5)) 
        ttk.Label(signup, textvariable=self.warning, foreground='red').grid(row=3, column=0, sticky="N", columnspan=2, padx =(5,5)) 


        # Entry-fields 
        self.user_entry = tk.Entry(signup,textvariable=self.username)
        self.user_entry.grid(row=1, column=0, sticky="NSEW", columnspan=2, padx =(5,5), pady =(5,0)) 
        self.user_entry.bind("<FocusIn>", lambda event, field=self.user_entry: self.focus_in(field))
        self.user_entry.bind("<FocusOut>", lambda event, field=self.user_entry, field_name='username': self.focus_out(event, field, field_name))

        self.pw_entry = tk.Entry(signup,textvariable=self.password)
        self.pw_entry.grid(row=2, column=0, sticky="NSEW", columnspan=2, padx =(5,5), pady =(5,0)) 
        self.pw_entry.bind("<FocusIn>", lambda event, field=self.pw_entry: self.focus_in(field))
        self.pw_entry.bind("<FocusOut>", lambda event, field=self.pw_entry, field_name='password': self.focus_out(event, field, field_name))

        #Buttons
        self.submit_button = tk.Button(signup, command=self.sign_up, text="Sign Up!",borderwidth=1, fg='darkslateblue')
        self.submit_button.grid(row=4, column=0, sticky="NSEW", columnspan=2, padx =(5,5), pady =(5,5))
        self.changeOnHover(self.submit_button, 'blue', 'darkslateblue') #change button color on hover

        self.login_button = tk.Button(signup, command=lambda: switch_frame('LoginWindow'), text="⟵ Back to Login", borderwidth=0, fg='blue', bg="#DCDAD5")
        self.login_button.grid(row=5, column=0, sticky="NEW", padx =(5,5), pady =(5,0))
        self.changeOnHover(self.login_button, 'red', 'blue') #change button color on hover

        self.forgotPW_button = tk.Button(signup, command=self.funfact, text="Fun fact of the day", borderwidth=0, fg='blue', bg="#DCDAD5")
        self.forgotPW_button.grid(row=5, column=1, sticky="NEW", padx =(5,5), pady =(5,0))
        self.changeOnHover(self.forgotPW_button, 'red', 'blue') #change button color on hover


    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.destroy() #destroy window

    def focus_in(event, field):
        field.delete(0,"end")
        # usercheck=True
    
    def focus_out(self, event, field, field_name):
        '''
        Get's inserted value on focus out or adds placeholder prompting for input if no input was given;
        Works for both the username and the password - fields
        '''
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
            self.username.set(user)
            print(user)

        elif field_name=='password':
            text_var = self.password.get() #field.cget("textvariable")
            pw = process_input(text_var, field_name)
            self.password.set(pw)

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

    def sign_up(self):
        user = self.username.get()
        pw= self.password.get()
        status = db_transact.sign_up(user, pw)
        print('Signed Up!' if status==1 else 'Something went wrong! Please try again' if status==0 else 'A user with that name already exist. Please choose another username!' if status==-1 else 'Unknown error!')
        if status == 1:
            self.switch_frame('LoginWindow') #To DO: once df data is loaded into database -> load user data into TC-frame
        elif status == 0:
            self.warning.set("Something went wrong. Please try again")
        elif status == -1:
            self.warning.set("User already exists!")


    def funfact(self):
        print("Switch to password recovery page!")



# # ----- run app -----
# if __name__ == '__main__':
#     app = SignupWindow() 

#     app.mainloop()