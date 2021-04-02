# TO DO: use <FocusIn> for tk.EntryFrame objects without changing self.value_entry_record status (or with function that changes it back)
# TO DO: deal with redundant psce after toggle (.gir_remove()) OR add specification to column behind checkbox instead
# TO DO: got o entry_information and modify all fields to toggle (using "opens" and "on_demand" - keys) if applicable
# TO DO: delete on_demand-field information whenever the controlling field is unchecked -- OR: check how to incorporate this feature directly on the database end

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
                self.create_checkBox(self.building_blocks[option_name], option[option_name],label_name)

            elif option[option_name]["type"] == "MultipleChoice":
                # print("optionmenu", option_name) #uncomment for troubleshooting
                self.create_multiChoice(self.building_blocks[option_name], option[option_name],label_name)

            elif option[option_name]["type"] == "Spinbox":
                self.create_spinBox(self.building_blocks[option_name], option[option_name],label_name)
 
            elif option[option_name]["type"] == "Entryfield":  
                self.create_entryField(option_name, label_name)

            else:
                pass

            if option[option_name]["type"] != "Entryfield":  # for EntryField: self.value_entry_record is set to True upon appenting entry-list
                # start tracing option StringVar-objects AFTER setting up entry-menu, as these objects are changed to a default value for many entry-options -- > this would falsely run check_option()
                self.building_blocks[option_name]["selection"].trace("w", lambda clback1, clback2, clback3, option=option_name: self.check_options(option=option))  #lambda option=option_name, topic=self.building_blocks: self.check_options(option, topic) #trace StringVar-object and change according self.value_entry_record when a write change is recorded


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
    def check_options(self, option=None, value=None):

        if value:
            value = value
        else:
            # print checkbutton variable value (=value of tk.Stringvar-object saved in topic-dict for current option)
            value = self.building_blocks[option]["selection"].get()

        self.value_entry_record[option] = True
        print(self.value_entry_record)
            
        print(value) #uncomment for troubleshooting

    # ---- function toggling specification field, if available ------
    def toggle_checkbox(self, option_info):
        if "opens" in option_info.keys():
            # get label_name for option to toggle
            to_toggle_label = option_info["opens"]
            # get widget based on name
            to_toggle = self.building_blocks[to_toggle_label]["frame"]  #contains 2 children: the label and the entry-field-object (e.g. an OptionMenu-onject)
            # get children of widget to toggle
            label_to_toggle = to_toggle.winfo_children()[0]
            field_to_toggle = to_toggle.winfo_children()[1]

            # toggle
            if label_to_toggle.grid_info():
                label_to_toggle.grid_remove()
                self.building_blocks[to_toggle_label]["selection"].set(0)
                self.value_entry_record[to_toggle_label] = False
                field_to_toggle.grid_remove()
            else:
                label_to_toggle.grid(row=0, column=0, sticky="W", padx =(5,0))
                field_to_toggle.grid(row=0, column=1, sticky="W", padx =(5,0))


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
                # print(option_name,": ", value) #Entryfields take multiple entries saved in a list
            else:
                value = self.building_blocks[option_name]["selection"].get()
                # print(option_name,": ", value) #any otherfields take one entry saved in a tk.StringVar-object

            # account for empty lists
            if len(value) == 0:
                value = None

            # add info of current entry-field to dict
            data_dict[option_name_db] = value

        return data_dict


    # ----- method adding entries from tk.Entry()-fields -----
    def add_entry_to_entrylist(self, option_name):
        '''
        Function adding a string to a list in order to keep track of entries into EntryField-objects
        + calling self.check_options() in order to change corresponding value_entry_record to "True"

        Keyword argument: option_name -- a string 
        '''

        # print(option_name) #uncomment for troubleshooting
        # get information and objects from dict
        field_list = self.building_blocks[option_name]["entries"]
        entry = self.building_blocks[option_name]["selection"].get()
        container = self.building_blocks[option_name]["frame"]
        entry_field = self.building_blocks[option_name]["entry_object"]

        if entry != "Type info + ENTER" and len(entry) > 1:
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
            self.building_blocks[option_name]["entry_object"].delete(0, "end")

        print(self.building_blocks[option_name]["entries"])


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

        # keep only values that have been entered in data-dict (--> exclude default values)
        for key, value in data.items():
            if self.value_entry_record == False:
                del data[key]

        print(f"Inserted into database: {data}")
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
        
    def focus_in(event, field):
        field.delete(0,"end")

    # ----- function creation checkbox-frame with functionality -----
    def create_checkBox(self, frame_info, option_info, label):
        frame_info["frame"].pack(anchor="w")
        ttk.Label(frame_info["frame"] ,text=label, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
        ttk.Checkbutton(frame_info["frame"],
                        command=lambda option_info=option_info: self.toggle_checkbox(option_info), #lambda command refering to method in order to be able to pass current option name as variable
                        variable=frame_info["selection"]).grid(row=0, column=1, sticky="W")

    def create_multiChoice(self, frame_info, option_info, label):
        frame_info["selection"].set(option_info["selection_menu"][0])
        frame_info["frame"].pack(anchor="w")
        if "on_demand" in option_info.keys():
            ttk.Label(frame_info["frame"] ,text=label, width=17) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
            tk.OptionMenu(frame_info["frame"],
                            frame_info["selection"],
                            *option_info["selection_menu"],
                            # command=lambda option=option_name, topic=self.building_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                            )
        else:
            ttk.Label(frame_info["frame"] ,text=label, width=17).grid(row=0, column=0, sticky="W", padx =(5,0))
            tk.OptionMenu(frame_info["frame"],
                            frame_info["selection"],
                            *option_info["selection_menu"],
                            # command=lambda option=option_name, topic=self.building_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                            ).grid(row=0, column=1, sticky="W")

    def create_spinBox(self, frame_info, option_info, label):
        frame_info["increment"] = option_info["increment"]
        frame_info["frame"].pack(anchor="w")
        if "on_demand" in option_info.keys():
            ttk.Label(frame_info["frame"] ,text=label, width=17) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
            frame_info["entry_object"] = tk.Spinbox(frame_info["frame"],
                            # command=lambda option=option_name, topic=self.building_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                            textvariable=frame_info["selection"],
                            from_=option_info["from"],
                            to=option_info["to"],
                            increment=option_info["increment"],
                            justify="center",
                            width=5)
        else:
            ttk.Label(frame_info["frame"] ,text=label, width=17).grid(row=0, column=0, sticky="W", padx =(5,0))
            frame_info["entry_object"] = tk.Spinbox(frame_info["frame"],
                            # command=lambda option=option_name, topic=self.building_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                            textvariable=frame_info["selection"],
                            from_=option_info["from"],
                            to=option_info["to"],
                            increment=option_info["increment"],
                            justify="center",
                            width=5).grid(row=0, column=1, sticky="W", padx =(5,0))

    def create_entryField(self, option_name, label):
        self.building_blocks[option_name]["selection"].set(f"Type info + ENTER")      
        self.building_blocks[option_name]["frame"].pack(anchor="w")
        ttk.Label(self.building_blocks[option_name]["frame"] ,text=label, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
        self.building_blocks[option_name]["entry_object"] = tk.Entry(self.building_blocks[option_name]["frame"],
                        # command=lambda x=(option_name, self.building_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
                        textvariable=self.building_blocks[option_name]["selection"],
                        )
        self.building_blocks[option_name]["entry_object"].grid(row=0, column=1, sticky="W")
        self.building_blocks[option_name]["entries"] = []
        self.building_blocks[option_name]["entry_object"].bind("<Return>", lambda event: self.add_entry_to_entrylist(option_name=option_name))
        self.building_blocks[option_name]["entry_object"].bind("<FocusOut>", lambda event: self.add_entry_to_entrylist(option_name=option_name))

        # return self.building_blocks[option_name]