# ----- import libraries and  xxx ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
import sys


class Style():
    def __init__(self, controller):
        self.controller = controller

        # colors
        # ----- Colors ----- 
        COL_PRIM = "#585278"
        COL_SEC = "#6f6898"
        COL_LIGHT_BG = "#ebe4ea" #"fff"
        COL_LIGHT_TXT = "#eee"
        COL_DARK_TXT = "#311a80"
        COL_HIGHLIGHT = "#e3007d"


        # create custom style
        style = ttk.Style(self.controller)
        style.theme_use("clam")
        style.configure("Timer.TFrame", background=COL_LIGHT_BG) #style 1
        style.configure("Background.TFrame", background=COL_LIGHT_BG) #style 2
        style.configure("Timer.TFrame", background=COL_LIGHT_BG) #style 3 
        style.configure("TimerText.TLabel", background=COL_LIGHT_BG, foreground=COL_DARK_TXT, font="Courier 38") #style 4
        style.configure("LightText.TLabel", background=COL_PRIM, foreground=COL_LIGHT_TXT) #style 5
        style.configure("PomodoroButton.TButton", background=COL_SEC, foreground=COL_LIGHT_TXT) #style 6
        style.map("PomodoroButton.TButton", background=[("active", COL_PRIM), ("disabled",COL_LIGHT_TXT)], bordercolor=[("active", COL_HIGHLIGHT)], borderwidth=[("active", 3)]) #style 7

print(sys.path)