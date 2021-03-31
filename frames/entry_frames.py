# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkcalendar import Calendar, DateEntry
import datetime
import os
# from .analysis.dataframes.dataframe import TrackerFrame
import database.connections.db_transact as db_transact

class EntryFrame(tk.Frame):
    def __init__(self, container, info_list:dict, tab_name, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # ----- Parameters -----
        self.info_list = info_list
        self.building_blocks = {}
        self.value_entry_record = {} #records info about if a new value was entered --> if False - any value is the default value, that does not need to be saved in database
        self.all_options = [[*option][0] for option in info_list]
        # self.tracker = tracker
        self.current_date = datetime.datetime.now().date()
        if tab_name == "Longterm Changes":
            self.tab = "longterm"
        else:
            self.tab = tab_name.lower()
            
        # print('\ntabname: ', self.tab)
        # print('\tContainer children: ', container.winfo_children())
        # print('\tContainer children values: ',container.children.values())
        # print('\tContainer children class: ',container.winfo_class())
        # print('\tContainer parent: ',container.winfo_parent())
        # print('\t\tSiblings: ', container.master.winfo_children())
        # for child in container.master.winfo_children():
        #     print(f"Sibling: {child}")
        #     for childchild in child.winfo_children():
        #         print(f"\tSiblings child: {childchild}")
        #         print('\t\tClass:', childchild.winfo_class())
        #         if childchild.winfo_class() == 'Frame':
        #             for entryframe in childchild.winfo_children():
        #                 print(f"\t\t\tEntryframe: {entryframe}")
        #                 for widget in entryframe.winfo_children():
        #                     print(f"\t\t\t\tWidget: {widget}")
        #                     print('\t\t\t\t\tClass:', widget.winfo_class())
        #                 if not entryframe.winfo_children():
        #                     print('\t\t\t\t\tNo Children!')
        #                     print('\t\t\t\t\tName: ', entryframe.winfo_name())
        #                     # entryframe.config(state=tk.DISABLED)
        #                     if entryframe.winfo_name() == '!button3':
        #                         print('\t\t\t\t\tButton OF INTEREST!')
        #                         print('\t\t\t\t\t', entryframe['text'])
        # print("\n\n")


    # ----- Frames -----

        # create and place containing frame
        # self.entry_frame = tk.Frame(container)        
        # self.grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

        # ------ Health Data Entry ------
        # interate over options
        for option in self.info_list:

            # get option string
            option_name = [*option][0]
            label_name = option[option_name]['label']

            # create building blocks (frame and stringvar - objects) for each option and save in dict - to access in commands on click
            self.building_blocks[option_name] = {}
            self.building_blocks[option_name]["frame"] = tk.Frame(self)
            self.building_blocks[option_name]["type"] = option[option_name]["type"]
            self.building_blocks[option_name]["selection"] = tk.StringVar(value=0)   #entered value (or default values) is saved here
            self.value_entry_record[option_name] = False   

            # create object based on the given type information
            if option[option_name]["type"] == "Checkbox":
                self.building_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.building_blocks[option_name]["frame"] ,text=label_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                ttk.Checkbutton(self.building_blocks[option_name]["frame"],
                                command=lambda option=option_name, topic=self.building_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                                variable=self.building_blocks[option_name]["selection"]).grid(row=0, column=1, sticky="W")

            elif option[option_name]["type"] == "MultipleChoice":
                # print("optionmenu", option_name) #uncomment for troubleshooting
                self.building_blocks[option_name]["selection"].set(option[option_name]["selection_menu"][0])
                self.building_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.building_blocks[option_name]["frame"] ,text=label_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                tk.OptionMenu(self.building_blocks[option_name]["frame"],
                                # command=lambda x=(option_name, self.building_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
                                self.building_blocks[option_name]["selection"],
                                *option[option_name]["selection_menu"]).grid(row=0, column=1, sticky="W")

            elif option[option_name]["type"] == "Spinbox":
                self.building_blocks[option_name]["increment"] = option[option_name]["increment"]
                self.building_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.building_blocks[option_name]["frame"] ,text=label_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                self.building_blocks[option_name]["entry_object"] = tk.Spinbox(self.building_blocks[option_name]["frame"],
                                command=lambda option=option_name, topic=self.building_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                                textvariable=self.building_blocks[option_name]["selection"],
                                from_=option[option_name]["from"],
                                to=option[option_name]["to"],
                                increment=option[option_name]["increment"],
                                justify="center",
                                width=5)
                self.building_blocks[option_name]["entry_object"].grid(row=0, column=1, sticky="W")
                self.building_blocks[option_name]["entry_object"].bind("<FocusOut>", lambda event, option=option_name, topic=self.building_blocks: self.check_options(option, topic))

            elif option[option_name]["type"] == "Entryfield":  
                self.building_blocks[option_name]["selection"].set(f"Type info + ENTER")      
                self.building_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.building_blocks[option_name]["frame"] ,text=label_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                self.building_blocks[option_name]["entry_object"] = tk.Entry(self.building_blocks[option_name]["frame"],
                                # command=lambda x=(option_name, self.building_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
                                textvariable=self.building_blocks[option_name]["selection"],
                                )
                self.building_blocks[option_name]["entry_object"].grid(row=0, column=1, sticky="W")
                self.building_blocks[option_name]["entries"] = []
                self.building_blocks[option_name]["entry_object"].bind("<Return>", lambda event, x=(self.building_blocks, option_name): self.add_entry_to_entrylist(entry_info_dict, option_name)(*x))

            else:
                pass

    # ----- Buttons -----
        test = ttk.Button(
                self,
                command=self.get_all_selected,
                text="Print Selection"
                )
        test.pack(anchor="w", pady =15, padx = (5,5))

        test_plotly = ttk.Button(
                self,
                command=self.show_plotly,
                text="Open Plotly!"
                )
        test_plotly.pack(anchor="w", pady =15, padx = (5,5))    


    # ----- method printing current checkbutton state when clicked and passing them on to dataframe to be saved -----
    def check_options(self, option, topic=None, value=None):

        if value:
            value = value
            # print(value) #uncomment for troubleshooting
        else:
            # print checkbutton variable value (=value of tk.Stringvar-object saved in topic-dict for current option)
            value = topic[option]["selection"].get()

        self.value_entry_record[option_name] = True  
            
        # self.tracker.update_frame(self.tab, option, value, self.current_date) #update for when using .csv-file as storage
        print(value) #uncomment for troubleshooting

    # ----- method printing all current checkbutton states -----
    def get_all_selected(self):
        '''
        Gets all selected values from current EntryFrame;
        Saves data in dict to pass on to database-functions;
        Return dict for each entry field: key - entry-field (option), value - entered value
        '''

        data_dict = {}
        # iterate over info_dicts within list
        for option in self.info_list:

            # grab outer key for current dict --> each outer dict has only one outer key
            option_name = [*option][0]
            if option_name == 'cramps' or option_name == 'spotting':  # workaround loop that is going to be removed once .csv usage is completely removed
                continue

            # convert GUI options text to database-conform text
            option_name_db = self.cols_to_db_name(option_name)

            # check option entry type
            if option[option_name]["type"] == "Entryfield":
                value = self.building_blocks[option_name]["entries"]
                print(option_name,": ", value) #Entryfields take multiple entries saved in a list
            else:
                value = self.building_blocks[option_name]["selection"].get()
                print(option_name,": ", value) #any otherfields take one entry saved in a tk.StringVar-object

            # account for empty lists
            if len(value) == 0:
                value = None

            # add info of current entry-field to dict
            data_dict[option_name_db] = value

        return data_dict

    # ----- method adding entries from tk.Entry()-fields -----
    def add_entry_to_entrylist(self, entry_info_dict, option_name):

        # print(option_name) #uncomment for troubleshooting
        # get information and objects from dict
        field_list = entry_info_dict[option_name]["entries"]
        entry = entry_info_dict[option_name]["selection"].get()
        container = entry_info_dict[option_name]["frame"]
        entry_field = entry_info_dict[option_name]["entry_object"]

        # append new entry to entry list
        field_list.append(entry)

        # print entries (including new entry) to screen (next to entry field)
        self.print_entries(field_list, container)

        # # for troubleshooting
        # print(field_list)

        # save changes to dataframe
        # print(option_name) #uncomment for troubleshooting
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

    # ----- method updating displayed entries based on selected date -----
    def update_selection(self, data_dict, date):

        # get tab-relevant data for current EntryFrame()-object
        data = data_dict[self.tab]

        # update fields
        # for option in data.columns:
        for option in data.keys():
            try:
                try: 
                    # value = data.loc[date, option] #get value for according field in df
                    value = data[option] #get value for according field in df
                    # print(option,": ", value) #uncomment for troubleshooting

                    if self.building_blocks[option]["type"] == "Checkbox":
                        try:
                            self.building_blocks[option]["selection"].set(str(int(value))) #get int-version, as only 0 or 1 are accepted for Checkbox
                        except:
                            print(f"Selection change not possible for: {option}")

                    elif self.building_blocks[option]["type"] == "Spinbox":
                        try:
                            if self.building_blocks[option]["increment"] < 1: #use float for increments <1
                                converted_value = str(value)
                                self.building_blocks[option]["selection"].set(converted_value)
                            else: #use integers for increments > 1 -> otherwise diplay will not update because decimal points cannot be displayed for increments larger than 1
                                converted_value = str(int(value)) 
                                self.building_blocks[option]["selection"].set(converted_value)
                        except:
                            print(f"Selection change not possible for: {option}")                                          
                    elif self.building_blocks[option]["type"] == "Entryfield":
                        try:
                            entry_string = value.strip("[]").replace("'","") # value is a list as a strin -> to get desired output strip square bracets and remove single quotes
                            if (value) and (entry_string != 'nan'):
                                ttk.Label(self.building_blocks[option]["frame"], name='former_entries',text=entry_string, foreground='grey', background='whitesmoke').grid(row=1, column=1, sticky="W") #add label displaying previosu entries under Entryfield
                            else:
                                for child in self.building_blocks[option]["frame"].winfo_children():
                                    if child.winfo_name() == 'former_entries':
                                        child.grid_remove()
                        except:
                            print(f"Selection change not possible for: {option}") 
                              
                    elif self.building_blocks[option]["type"] == "MultipleChoice":
                        try:
                            self.building_blocks[option]["selection"].set(value) #get int-version, as only 0 or 1 are accepted for Checkbox
                        except:
                            print(f"Selection change not possible for: {option}")                               
                    else:
                        print(f'The {option}-field is of type {self.building_blocks[option]["type"]}.')
                except Exception as e:
                    print(f"Data for {date} not available. \n\t Error: {e}")  
            except KeyError as e: #KeyError will be thrown if no entryfield with the current options value exists
                print(f"There is no entry field with the value {option}. \n\t Error: {e}") 

    def insert_database(self, user, date):
        '''
        Insert selection of current tab to database for specified date and logged in user
        '''
        
        # get selection
        data = self.get_all_selected()

        # append user and date to data
        data['date'] = date  #do not use today's date, in case Date Picker was used to change current health tracker date

        # insert into database
        db_transact.add_data(self.tab, data, user)

    def cols_to_db_name(self, option_name):
        '''
        Work-around function until .csv file usage is completely removed -- to be removed
        '''
        gui_options = ['REM', 'frequent wakeups', 'sleep medication', 'timezone change', 'cheats/sweets/unhealthy']
        db_col_names = ['rem', 'freq_wakes', 'sleep_meds', 'tz_change', 'unhealthy_food']

        for gui, db in zip(gui_options, db_col_names):
            if option_name in gui:
                option_name_translated = option_name.replace(gui, db)
                return option_name_translated
            elif option_name == 'frequent wakeups':
                return 'freq_wakes'
            elif option_name == 'sleep medication':
                return 'sleep_meds'
            elif option_name == 'timezone change':
                return 'tz_change'
            elif option_name == 'cheats/sweets/unhealthy':
                return 'unhealthy_food'
            elif option_name == 'hiking':
                return 'cardio'
            else:
                option_name_translated = option_name.replace(" ", "_")
                option_name_translated = option_name_translated.replace("?", "")
                return option_name_translated

        
