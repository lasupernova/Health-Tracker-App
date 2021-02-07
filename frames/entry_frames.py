# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkcalendar import Calendar, DateEntry
import datetime
import os
from .analysis.dataframes.dataframe import TrackerFrame

class EntryFrame(tk.Frame):
    def __init__(self, container, info_list:dict, tab_name, tracker, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # ----- Parameters -----
        self.info_list = info_list
        self.bulding_blocks = {}
        self.all_options = [[*option][0] for option in info_list]
        self.tracker = tracker
        if tab_name == "Longterm Changes":
            self.tab = "longterm"
        else:
            self.tab = tab_name.lower()
        print(self.tab)


    # ----- Frames -----

        # create and place containing frame
        # self.entry_frame = tk.Frame(container)        
        # self.grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

        # ------ Health Data Entry ------
        # interate over options
        for option in self.info_list:

            # get option string
            option_name = [*option][0]

            # create building blocks (frame and stringvar - objects) for each option and save in dict - to access in commands on click
            self.bulding_blocks[option_name] = {}
            self.bulding_blocks[option_name]["frame"] = tk.Frame(self)
            self.bulding_blocks[option_name]["selection"] = tk.StringVar(value=0)

            # create object based on the given type information
            if option[option_name]["type"] == "Checkbox":
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                ttk.Checkbutton(self.bulding_blocks[option_name]["frame"],
                                command=lambda option=option_name, topic=self.bulding_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                                variable=self.bulding_blocks[option_name]["selection"]).grid(row=0, column=1, sticky="W")

            elif option[option_name]["type"] == "MultipleChoice":
                # print("optionmenu", option_name) #uncomment for troubleshooting
                self.bulding_blocks[option_name]["selection"].set(option[option_name]["selection_menu"][0])
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                tk.OptionMenu(self.bulding_blocks[option_name]["frame"],
                                # command=lambda x=(option_name, self.bulding_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
                                self.bulding_blocks[option_name]["selection"],
                                *option[option_name]["selection_menu"]).grid(row=0, column=1, sticky="W")

            elif option[option_name]["type"] == "Spinbox":
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                self.bulding_blocks[option_name]["entry_object"] = tk.Spinbox(self.bulding_blocks[option_name]["frame"],
                                command=lambda option=option_name, topic=self.bulding_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                                textvariable=self.bulding_blocks[option_name]["selection"],
                                from_=option[option_name]["from"],
                                to=option[option_name]["to"],
                                increment=option[option_name]["increment"],
                                justify="center",
                                width=5)
                self.bulding_blocks[option_name]["entry_object"].grid(row=0, column=1, sticky="W")
                self.bulding_blocks[option_name]["entry_object"].bind("<FocusOut>", lambda event, option=option_name, topic=self.bulding_blocks: self.check_options(option, topic))

            elif option[option_name]["type"] == "Entryfield":  
                self.bulding_blocks[option_name]["selection"].set(f"Type info + ENTER")      
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                self.bulding_blocks[option_name]["entry_object"] = tk.Entry(self.bulding_blocks[option_name]["frame"],
                                # command=lambda x=(option_name, self.bulding_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
                                textvariable=self.bulding_blocks[option_name]["selection"],
                                )
                self.bulding_blocks[option_name]["entry_object"].grid(row=0, column=1, sticky="W")
                self.bulding_blocks[option_name]["entries"] = []
                self.bulding_blocks[option_name]["entry_object"].bind("<Return>", lambda event, x=(self.bulding_blocks, option_name): self.add_entry(*x))

            else:
                pass

                # insert elements by their 
                # index and names. 
                # for i in range(1,len(option[option_name]["selection_menu"])+1):
                #     print(i)
                # for selection_option, index in zip(option[option_name]["selection_menu"],range(1,len(option[option_name]["selection_menu"])+1)):
                #     listbox.insert(index, selection_option) 


    # ----- Buttons -----
        test = ttk.Button(
                self,
                command=lambda x=(self.all_options, self.bulding_blocks): self.print_all_selected(*x),
                text="Print Selection"
                )
        test.pack(anchor="w", pady =15, padx = (5,5))

        test_plotly = ttk.Button(
                self,
                command=self.show_plotly,
                text="Open Plotly!"
                )
        test_plotly.pack(anchor="w", pady =15, padx = (5,5))    

        select_date = ttk.Button(
                self,
                command=self.change_date,
                text="Change date"
                )
        select_date.pack(anchor="w", pady =15, padx = (5,5))    

    # ----- Date Picker -----
        today = datetime.datetime.now().date() 

    def change_date(self):
        def print_sel(e):
            print(cal.get_date())
        cal = DateEntry(self, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        cal.pack(padx=10, pady=10)
        cal.bind("<<DateEntrySelected>>", print_sel)

    # ----- method printing current checkbutton state when clicked and passing them on to dataframe to be saved -----
    def check_options(self, option, topic=None, value=None):

        if value:
            value = value
            self.tracker.update_frame(self.tab, option, value)
            print(value)
        else:
            # print checkbutton variable value (=value of tk.Stringvar-object saved in topic-dict for current option)
            value = topic[option]["selection"].get()
            self.tracker.update_frame(self.tab, option, value)
            print(value)


    # ----- method printing all current checkbutton states -----
    def print_all_selected(self, options, topic):

        # iterate over info_dicts within list
        for option in self.info_list:

            # grab outer key for current dict --> each outer dict has only one outer key
            option_name = [*option][0]

            # check option entry type
            if option[option_name]["type"] == "Entryfield":
                print(option_name,": ", topic[option_name]["entries"]) #Entryfields take multiple entries saved in a list
            else:
                print(option_name,": ", topic[option_name]["selection"].get()) #any otherfields take one entry saved in a tk.StringVar-object


    # ----- method adding entries from tk.Entry()-fields -----
    def add_entry(self, entry_info_dict, option_name):

        print(option_name)
        # get information and objects from dict
        field_list = entry_info_dict[option_name]["entries"]
        entry = entry_info_dict[option_name]["selection"].get()
        container = entry_info_dict[option_name]["frame"]
        entry_field = entry_info_dict[option_name]["entry_object"]

        # append new entry to entry list
        field_list.append(entry)

        # print entries (including new entry) to screen (next to entry field)
        self.print_entries(field_list, container)

        # for troubleshooting
        print(field_list)

        # save changes to dataframe
        print(option_name)
        self.check_options(option=option_name, value=field_list)

        # clear text typed in entry-fieldc
        entry_info_dict[option_name]["entry_object"].delete(0, "end")


    # ----- method displaying tk.Entry()-field entries to new tk.Label()-field next to entry field -----
    def print_entries(self, entry_list, container):

        # convert list to string with list items separated by commas
        entry_string = ', '.join([str(i) for i in entry_list])

        # create a Label to display string
        tk.Label(container, text=entry_string).grid(row=0, column=2, sticky="W")

    def show_plotly(self):
        import plotly.express as px

        gapminder = px.data.gapminder()
        fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
                hover_name="country", log_x=True, size_max=60)
        fig.show()