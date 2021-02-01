# ----- import libraries and  xxx ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os

class EntryFrame(tk.Frame):
    def __init__(self, container, info_list:dict, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # ----- Parameters -----
        self.info_list = info_list
        self.bulding_blocks = {}
        self.all_options = [[*option][0] for option in info_list]

        # ----- Frames -----

        # interate over options
        for option in self.info_list:

            # get option string
            option_name = [*option][0]

            # create building blocks (frame and stringvar - objects) for each option and save in dict - to access in commands on click
            self.bulding_blocks[option_name] = {}
            self.bulding_blocks[option_name]["frame"] = tk.Frame(container)
            self.bulding_blocks[option_name]["selection"] = tk.StringVar(value=0)

            # create object based on the given type information
            if option[option_name]["type"] == "Checkbox":
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                ttk.Checkbutton(self.bulding_blocks[option_name]["frame"],
                                command=lambda x=(option_name, self.bulding_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
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
                tk.Spinbox(self.bulding_blocks[option_name]["frame"],
                                command=lambda x=(option_name, self.bulding_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
                                textvariable=self.bulding_blocks[option_name]["selection"],
                                from_=option[option_name]["from"],
                                to=option[option_name]["to"],
                                increment=option[option_name]["increment"],
                                justify="center",
                                width=5).grid(row=0, column=1, sticky="W")

            elif option[option_name]["type"] == "Entryfield":        
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
                container,
                command=lambda x=(self.all_options, self.bulding_blocks): self.print_all_selected(*x),
                text="Print Selection"
                )
        test.pack(anchor="w", pady =15, padx = (5,5))

    # method printing current checkbutton state when clicked
    def check_options(self, option, topic):
        # print checkbutton variable value (=value of tk.Stringvar-object saved in topic-dict for current option)
        print(topic[option]["selection"].get())


    # method printing all current checkbutton states
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

    def add_entry(self, entry_info_dict, option_name):
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
        # clear text typed in entry-fieldc
        entry_info_dict[option_name]["entry_object"].delete(0, "end")

    def print_entries(self, entry_list, container):
        # convert list to string with list items separated by commas
        entry_string = ', '.join([str(i) for i in entry_list])
        # create a Label to display string
        tk.Label(container, text=entry_string).grid(row=0, column=2, sticky="W")




        # [{"angry":{"type":"Checkbox", "Options":""}}]