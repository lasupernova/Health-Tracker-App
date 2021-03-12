# TO DO: make TrackerFrame() work within this script --> line 14, 40 and 47

# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from PIL import ImageTk, Image
import datetime
import sys
# from database.connections import db_transact #NOTE: use python -m frames.login_frame in order to circumvent relative import issue
from frames.signup_frame import SignupWindow
from frames.login_frame import LoginWindow
# from tracker import TrackerFrame

#  ----- class inheriting from tk.Tk -----
class MainWindow(tk.Tk):
    #  ----- initialize -----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #  ----- Frames ----- 

        # save a ttk frame - object in a variable named "container" 
        container = ttk.Frame(self) 
        container.grid() #position the frame in the parent widget in a grid
        container.columnconfigure(0, weight=1)

        # create dictionary to keep track of frames
        self.frames = dict()

        # add login frame that is placed within "container"
        self.login_frame = LoginWindow(container, lambda: self.switch_frame(SignupWindow)) #initiate Timer-class and pass self as the controller
        self.login_frame.grid(row=0, column=0, sticky="NESW") #configure timer frame placed in the first row and first column and to fill the entire frame ("container")

        # add signup frame 
        self.signup_frame = SignupWindow(container, lambda: self.switch_frame(LoginWindow))
        self.signup_frame.grid(row=0, column=0, sticky="NESW") 

        # # # add tracker frame 
        # self.tracker_frame = TrackerFrame('test_df.csv')
        # self.tracker_frame.grid(row=0, column=0, sticky="NESW") 

        # add both frames to dict
        self.frames[LoginWindow] = self.login_frame
        self.frames[SignupWindow] = self.signup_frame
        # self.frames[TrackerFrame] = self.tracker_frame

        # start with timer_frame in front
        self.switch_frame(LoginWindow)

    # ----- function that brings frame on the back to the front -----
    def switch_frame(self, container):
        # indicate which frame to bring to front
        frame = self.frames[container]
        #brings indicated frame to the front
        frame.tkraise() 
        print("WORKS!")


# ----- run app -----
if __name__ == '__main__':
    app = MainWindow() 

    app.mainloop()