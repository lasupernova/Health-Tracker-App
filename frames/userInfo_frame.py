# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os.path
from PIL import ImageTk, Image
import datetime
from tkcalendar import Calendar, DateEntry
import sys
import time
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
        self.signup = [child for child in self.root.winfo_children() if child.winfo_name() == "!signupwindow"][0]

    #----- User Info Screen -----

        # initiate login screen
        uinfo = ttk.Frame(self, width=50)
        uinfo.grid(row=0, column=0, sticky='EWNS')
        uinfo.grid_columnconfigure(0, weight=1)
        uinfo.grid_columnconfigure(1, weight=1)
        for n in range(7):
            uinfo.grid_rowconfigure(n, weight=1)

        # initiate textvariables to fill in 
        self.gender = tk.StringVar(value=0)
        self.dob_day = tk.StringVar(value="Day")
        self.dob_month = tk.StringVar(value="Month")
        self.dob_year = tk.StringVar(value="Year")
        self.warning = tk.StringVar(value=None)

        #Labels
        self.label_cont1 = tk.Frame(uinfo, bg=self.root.BG_COL_1)
        self.label_cont1.grid(row=0, rowspan=2, column=0, columnspan=2, padx =(5,5)) 
        self.label_cont1.grid_rowconfigure(0, weight=1)
        self.label_cont1.grid_columnconfigure(0, weight=1)

        # print(tk.font.families())  #uncomment to get overview of available font families

        # ------ Gender ------

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

        self.female_button = tk.Button(uinfo, command=self.female, image=self.female_img, borderwidth=0.5, fg='darkslateblue') 
        self.female_button.grid(row=3, rowspan=3, column=0, sticky="NSEW", pady =(5,5))
        self.changeOnHover(self.female_button, '#4936ba', 'darkslateblue', '#f8f7ff', 'whitesmoke') 

        self.male_button = tk.Button(uinfo, command=self.male, image=self.male_img, borderwidth=0.5, fg='darkslateblue') #
        self.male_button.grid(row=3, rowspan=3, column=1, sticky="NSEW", pady =(5,5))
        self.changeOnHover(self.male_button, '#4936ba', 'darkslateblue', '#f8f7ff', 'whitesmoke') 


        # --- DOB ---

        # Label
        self.dob_container = tk.Frame(uinfo, bg=self.root.BG_COL_1)  #container in order to be able to center correctly
        for n in range(5):
            self.dob_container.grid_rowconfigure(n, weight=1)
        for n in range(7):
            self.dob_container.grid_columnconfigure(n, weight=1)
        ttk.Label(self.dob_container, image=self.dob_img, width=20).grid(row=0, column=3, padx =(5,5)) 

        # Comboboxes
        curr_year = self.root.current_date.year

        self.selected_day = ttk.Combobox(self.dob_container, 
                    values=[i for i in range(32)], 
                    font=('MANIFESTO', 12), 
                    textvariable=self.dob_day, 
                    width=8,
                    name="day"
                    )
        self.selected_day.grid(row=2, rowspan=3, column=2, padx =(5,5))
        self.selected_day.bind("<<ComboboxSelected>>", self.check_dob)
        self.selected_day.bind("<Button-1>", lambda event: self.focus_in(event))
        self.selected_day.bind("<FocusOut>", lambda event: self.focus_out(event))

        self.selected_month = ttk.Combobox(self.dob_container, 
                    values=[i for i in range(13)], 
                    font=('MANIFESTO', 12), 
                    textvariable=self.dob_month, 
                    width=8,
                    name="month"
                    )
        self.selected_month.grid(row=2, rowspan=3, column=3, padx =(5,5))
        self.selected_month.bind("<<ComboboxSelected>>", self.check_dob)
        self.selected_month.bind("<Button-1>", lambda event: self.focus_in(event))
        self.selected_month.bind("<FocusOut>", lambda event: self.focus_out(event))

        self.selected_year = ttk.Combobox(self.dob_container, 
                    values=[i for i in range(1950,curr_year+1)], 
                    font=('MANIFESTO', 12), 
                    textvariable=self.dob_year, 
                    width=8,
                    name="year"
                    )
        self.selected_year.grid(row=2, rowspan=3, column=4, padx =(5,5))
        self.selected_year.bind("<<ComboboxSelected>>", self.check_dob)
        self.selected_year.bind("<Button-1>", lambda event: self.focus_in(event))
        self.selected_year.bind("<FocusOut>", lambda event: self.focus_out(event))

        # Button
        self.submit_button = tk.Button(self.dob_container, command=self.sign_up, text="NEXT »", borderwidth=0, fg='blue', bg="#DCDAD5", font=('MANIFESTO', 15))
        self.changeOnHover(self.submit_button, 'red', 'blue') #change button color on hover

        # warning 
        warning_container = ttk.Frame(self.dob_container)
        warning_container.grid(row=1, column=2, columnspan=3, padx =(5,5)) 
        warning_container.columnconfigure(0, weight=1)
        ttk.Label(warning_container, textvariable=self.warning, foreground='red').grid(row=0, column=0, padx =(5,5)) 


    # ----- funtion to run upon closing the window -----
    def on_exit(self):
        self.destroy() #destroy window

    def info_from_signup(self):
        self.user = self.signup.username.get()
        self.pw = self.signup.password.get()
        ttk.Label(self.label_cont1, text=f'             Hi {self.signup.username.get()}', width=20, font=('MANIFESTO', 18)).grid(row=0, column=0, padx =(5,5)) 
   
    def focus_in(self, event):
        """
        Deletes text shown in Combobox upon right mouse click, to facilitate direct typing as alternative to drop down menu.
        Note: <Button-1> used instead of <FocusIn>, as <FocusIn> will prevent value to be set while focus is on the widget

        Parameters:
            event: event handler - automatically passed to callback function
        """
        if event.widget.get() =="Day" or event.widget.get() =="Month" or event.widget.get() =="Year":
            event.widget.set("")

    def focus_out(self, event):
        """
        Adds original text back to Combobox on <FocusOut>-event, if no selection from dropdown menu was made.
        Upon dropdown menu selection, the textvariable of the selected Combobox will not be an empty string anymore.
        The Combobox-object value can directly be accessed by calling the .get()-method on the Combobox-object OR by calling .get() on the associated StringVar-object

        Parameters:
            event: event handler - automatically passed to callback function; 
                                   this handler contains information about the widget, including the value (event.widget.get()) and the widget name (event.widget.winfo_name())
        """
        if event.widget.get() == "":
            if event.widget.winfo_name() == "day":
                event.widget.set("Day")
            elif event.widget.winfo_name() == "month":
                event.widget.set("Month")
            elif event.widget.winfo_name() == "year":
                event.widget.set("Year")
    
    def male(self):
        self.gender.set(0)
        self.female_button.grid_forget()
        self.male_button.grid_forget()
        self.dob_container.grid(row=2, rowspan=3, column=0, columnspan=2, sticky="EWNS", padx =(5,5))

    def female(self):
        self.gender.set(1)
        self.female_button.grid_forget()
        self.male_button.grid_forget()
        self.dob_container.grid(row=2, rowspan=3,column=0, columnspan=2, sticky="EWNS", padx =(5,5)) 

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

    def sign_up(self):
        user = self.user
        pw = self.pw
        sex = self.gender.get()
        day = self.dob_day.get()
        month = self.dob_month.get()
        year = self.dob_year.get()
        dob = datetime.datetime.strptime(f'{day}-{month}-{year}', '%d-%m-%Y')
        status = db_transact.sign_up(user, pw, sex, dob)
        print('Signed Up!' if status==1 else 'Something went wrong! Please try again' if status==0 else 'A user with that name already exist. Please choose another username!' if status==-1 else 'Unknown error!')
        if status == 1:
            self.root.switch_frame('LoginWindow') #To DO: once df data is loaded into database -> load user data into TC-frame
        elif status == 0:
            self.warning.set("Something went wrong. Please try again")
        elif status == -1:
            self.warning.set("User already exists!")

    def check_dob(self, event):
        '''
        Callback function for dob-comboboxes.
        Checks if values were selected for all 3 Comboboxes and adds sumbit_button to grid if True.
        '''
        if self.dob_day.get() !="Day" and self.dob_month.get() !="Month" and self.dob_year.get() !="Year":
            self.submit_button.grid(row=5, column=4, columnspan=2, padx =(5,5), pady =(5,0))
            self.change_color(self.submit_button)
        else:
            print(f"Day: {self.dob_day.get()}\nMonth: {self.dob_month.get()}\nYear: {self.dob_year.get()}")


    def dob(self):
        '''
        Function called on submit_button - click.

        '''
        print(self.dob_day.get(), self.dob_month.get(), self.dob_year.get())

    def change_color(self, widget):
        '''
        NOTE1: running .after() in a loop (e.g. for) does not work, as the loop runs while after-round is still waiting
        NOTE2: subsequent .after()-calls, need to have increasing delays, as the first after-call delay time nis substracted from the 2nd one, the 2nd from the 3rd etc.
        --> solutions:
            1) extend tint-list by how often should be ran through
            2) call .enumerate() and multiply the enumerator by the desired time for each color
        '''
        def _color_text(widget, color):
            ''' Change font color of widget to "color" '''
            widget.config(fg=color)

        tints_of_blue = ["#0000FF", "#1919ff", "#3232ff", "#4c4cff", "#6666ff", "#7f7fff", "#9999ff", "#b2b2ff", "#ccccff", "#e5e5ff"]  #list of blue with decreasing saturation
        tints_of_blue += tints_of_blue[::-1]  #append reversed list to list
        tints_of_blue *= 3
        time_per_col = int(4000/len(tints_of_blue))   #each "blink" should take 60 seconds


        for n, tint in enumerate(tints_of_blue):
            self.after(time_per_col*n, _color_text, widget, tint)


        


