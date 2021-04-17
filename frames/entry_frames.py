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


    # # ----- Frames -----

        self.create_blank_entryframes()


    # ----- Buttons -----
        button_container = tk.Frame(self)
        button_container.pack(anchor="w", pady=20, padx =(10,10))
        test = ttk.Button(
                button_container,
                command=self.get_all_selected,
                text="Print Selection"
                )
        test.grid(row=0, column=0, sticky="W", padx=10, pady=5)

        test_plotly = ttk.Button(
                button_container,
                command=self.show_plotly,
                text="Open Plotly!"
                )
        test_plotly.grid(row=1, column=0, sticky="W", padx=10, pady=5)   

        logout_button =  ttk.Button(
                button_container,
                command=self.logout,
                text="Log Out"
                )
        logout_button.grid(row=0, column=1, sticky="W", padx=10, pady=5)


    # ----- method printing current checkbutton state when clicked and passing them on to dataframe to be saved -----
    def check_options(self, option=None, value=None):
        '''
        Checks entry value upon textvariable or entrylist change and 
        '''

        if value!=None:
            value = value
        else:
            # print checkbutton variable value (=value of tk.Stringvar-object saved in topic-dict for current option)
            value = self.building_blocks[option]["selection"].get()

        try:  #works for numeric fields saving selection as number (CheckBox and Spinbox)
            if int(value)==0 or value==0 or value == None or len(value) < 1:
                self.value_entry_record[option] = False
            else:
                self.value_entry_record[option] = True 
        except ValueError:  #works for fields saving selection as string (multiChoice)
            if value==0 or value == None or len(value) < 2:
                self.value_entry_record[option] = False
            else:
                self.value_entry_record[option] = True 
        except TypeError:  #works for fields saving selection as list (EntryField)
            if value == None or len(value) < 1:
                self.value_entry_record[option] = False
            else:
                self.value_entry_record[option] = True 


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
                try:
                    self.building_blocks[to_toggle_label]["translated_selection"].set(0)
                except:
                    pass
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

            # convert GUI options text to database-conform text
            option_name_db = self.cols_to_db_name(option_name)

            # check option entry type
            if option[option_name]["type"] == "Entryfield":
                value = self.building_blocks[option_name]["entries"]
                # account for empty lists
                if len(value) == 0:
                    value = None
            elif option[option_name]["type"] == "MultipleChoice":
                value = self.building_blocks[option_name]["translated_selection"].get()
                # print(self.building_blocks[option_name])  #uncomment for troubleshooting
            else:
                value = self.building_blocks[option_name]["selection"].get()
                # print(option_name,": ", value) #any otherfields take one entry saved in a tk.StringVar-object

            # add info of current entry-field to dict
            data_dict[option_name_db] = value

        return data_dict


    def create_blank_entryframes(self):
        """
        Creates entryframes including fields used for user input based on entry_information captured in self.info_list.
        ToDo: elaborate on structures created herein

        Returns: Void function
        """

        # ------ Health Data Entry ------
        # interate over options
        for option in self.info_list:

            # get option string
            option_name = [*option][0]
            label_name = option[option_name]['label']

            # IF frame does not exist yet: create building blocks (frame and stringvar - objects) for each option and save in dict - to access in commands on click
            if option_name not in self.building_blocks.keys():
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
                    self.building_blocks[option_name]["selection"].trace("w", lambda clback1, clback2, clback3, option=option_name: self.check_options(option=option))  #lambda option=option_name, topic=self.building_blocks: self.check_options(option, topic) #trace StringVar-object and change according self.value_entry_record when a write change is recorded`
           
            else:  #if frame already exists: reset value
                if option[option_name]["type"] == "Checkbox":
                    self.building_blocks[option_name]["selection"].set(0)

                elif option[option_name]["type"] == "MultipleChoice":
                    # print("optionmenu", option_name) #uncomment for troubleshooting
                    self.building_blocks[option_name]["selection"].set(option[option_name]["selection_menu"][0])

                elif option[option_name]["type"] == "Spinbox":
                    self.building_blocks[option_name]["selection"].set(0)

                elif option[option_name]["type"] == "Entryfield":  
                    self.building_blocks[option_name]["selection"].set(f"Type info + hit ENTER")
                    if len(self.building_blocks[option_name]["frame"].winfo_children()) > 2:  #more than 2 children only if entries are printed--> if so, destroy entry container
                        self.building_blocks[option_name]["frame"].winfo_children()[-1].destroy() 

                else:
                    pass
        


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
            # self.print_entries(field_list, container)
            self.print_entries(option_name)

            # # for troubleshooting
            # print(field_list)

            # save changes to dataframe
            # print(option_name) #uncomment for troubleshooting
            self.check_options(option=option_name, value=field_list)

            # clear text typed in entry-fieldc
            self.building_blocks[option_name]["entry_object"].delete(0, "end")

        print(self.building_blocks[option_name]["entries"])


    # ----- method displaying tk.Entry()-field entries to new tk.Label()-field next to entry field -----
    # def print_entries(self, entry_list, container):
    def print_entries(self, option_name, entry_list=None):
        '''
        Create tk.Frame-object that contains entries made to currently used EntryField-object'.
        New entries are .pack()-ed to end as buttons with label aestetics.
        These buttons delete entries from entry_list and themselves, when clicked.
        NOTE: the tk.Frame object is destroyed + recreated every time that a new entry is added to the list
               --> the number of children within the container is used to decide if the tk.Frame object already exists 
                   (and needs to be destroyed and recreated) OR if it does not exist yet and can simply be created

        Parameters:
            option_name: string
            entry_list: None or string - None when getting input from user; string when getting input from database
        '''

        def _create_entry_container(container, option_name, entry_list):
            '''
            Created tk.Frame-object packing and containing  "label-buttons" for entries.

            Parameters:
                entry_list: list-type object if obtained from GUI(self.building_blocks[option_name]["entries"]), string if obtained from database
                container: tk.Frame-object, that is stored in a class-globally accessible parameter (self.building_blocks[option_name]["frame"])
            '''

            if not entry_list:
                entry_list = self.building_blocks[option_name]["entries"]
            else:
                entry_list = entry_list.split(",")  #split string into list by ","

            entry_container = tk.Frame(container)
            entry_container.grid(row=1, column=1, sticky="W")  

            for entry in entry_list:
                label_button = tk.Button(entry_container, 
                                                text=entry, 
                                                borderwidth=0, 
                                                command=lambda str_entry=entry, container_=entry_container, option_name=option_name: self._delete_entry(str_entry, container_, entry_list, option_name),
                                                fg='grey', #"#b8b6b0", 
                                                bg='whitesmoke' #"SystemButtonFace"
                                                )

                label_button.pack(side="left")
                self.changeOnHover(label_button, 'red', "#b8b6b0") #change button color on hover 
        
        container = self.building_blocks[option_name]["frame"]

        # check if entry_container already exists (--> if main container contains more than 2 children [field-label and field-entryfield], then entry_field was previosuly created)
        if len(container.winfo_children()) == 2:
            _create_entry_container(container, option_name, entry_list)
        else:   #if entry_container already exist, destroy it and create new from new entry_list
            print(f"Destroy: ", container.winfo_children()[-1])
            container.winfo_children()[-1].destroy()
            _create_entry_container(container, option_name, entry_list)

    def _delete_entry(self, entry, container, entry_list, option_name):
        '''
        Deletes entry from entry_list as well as corresponding button.
        This function is called upon clicking one of the "label-buttons" created by the print_entries()-method.

        Parameters:
            entry: string-object - name of the entry/item to delete
            container: tk.frame-object - "entry_container" created by print_entries()-method containing the "label-buttons"
            entry_list: list-type object, that is stored in a class-globally accessible parameter (self.building_blocks[option_name]["entries"])
        '''
        for button in container.winfo_children():
            if button["text"] == entry:
                print("Deleting Entry...")
                button.destroy()
                entry_list.remove(entry)
                if len(entry_list) == 0:  #if no more entries printed, destroy container, to toggle space in
                    container.destroy()
                self.check_options(option=option_name, value=entry_list)  #record if changes need to be submitted to database


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
        """
        Updates shown selection upon date change

        Parameters:
            data_dict: dict - contains options and database info of all tabs, obtained by db_transact.query_data_by_date_and_user()-function (called in root)
            date: string - contains date info

        Returns: Void function
        """

        def __update_checkbox__(option, value):
            """
            Updates value for specified checkbox entryfield

            Parameters:
                option: string - field name
                value: bool - field is going to be set to this value
            
            Returns: 0 (success) or -1 (Error)
            """
            try:
                self.building_blocks[option]["selection"].set(str(int(value))) #get int-version, as only 0 or 1 are accepted for Checkbox
                option_info = [info[option] for info in self.info_list if option in info.keys()][0]  #get option's entry-info from info_list-list (a list of tables)
                if "opens" in option_info.keys() and value:
                    to_open = option_info["opens"]
                    to_open_info = [info[to_open] for info in self.info_list if to_open in info.keys()][0]  #get info of option to open, based on controller parent info
                    to_open_value = data[to_open]
                    self.toggle_checkbox(option_info)
                    if to_open["type"] == "Spinbox":
                        __update_spinbox__(to_open, to_open_value)
                    elif to_open["type"] == "MultipleChoice":
                        __update_multichoice__(to_open, to_open_value)
                    del data[to_open]  #delete optional entry-option, to avoid duplicate addition
                elif "opens" in option_info.keys() and not value:
                    to_open = option_info["opens"]
                    del data[to_open]
                return 0
            except Exception as e:
                print(f"Selection change not possible for: {option}; reason: {e}")            
                return -1

        def __update_spinbox__(option, value):
            """
            Updates value for specified spinbox entryfield

            Parameters:
                option: string - field name
                value: int or float - field is going to be set to this value
            
            Returns: 0 (success) or -1 (Error)
            """

            if value:
                try:
                    if self.building_blocks[option]["increment"] < 1: #use float for increments <1
                        converted_value = str(value)
                        self.building_blocks[option]["selection"].set(converted_value)
                    else: #use integers for increments > 1 -> otherwise diplay will not update because decimal points cannot be displayed for increments larger than 1
                        converted_value = str(int(value)) 
                        self.building_blocks[option]["selection"].set(converted_value)
                except Exception as e:
                    print(f"Selection change not possible for: {option}; reason: {e}")  
                    return -1

        def __update_multichoice__(option, value):
            """
            Updates value for specified multichoice entryfield

            Parameters:
                option: string - field name
                value: string or int - field is going to be set to this value
            
            Returns: 0 (success) or -1 (Error)
            """
            if  value:
                try:
                    self.building_blocks[option]["selection"].set(value) #get int-version, as only 0 or 1 are accepted for Checkbox
                except Exception as e:
                    print(f"Selection change not possible for: {option}; reason: {e}")   

        def __update_entryfield__(option, value):
            """
            Updates value for specified text entryfield

            Parameters:
                option: string - field name
                value: string (representing a list) - field is going to be set to this value
            
            Returns: 0 (success) or -1 (Error)
            """
            try:
                if value:
                    entry_string = value.strip("[]").replace("'","") # value is a list as a string -> to get desired output strip square bracets and remove single quotes
                    if (value) and (entry_string != 'nan'):
                        # print(f">>>Entry String: {entry_string}")  #uncomment for troubleshooting
                        self.print_entries(option, entry_list=entry_string)
                    else:
                        for child in self.building_blocks[option]["frame"].winfo_children():
                            if child.winfo_name() == 'former_entries':
                                child.grid_remove()
            except Exception as e:
                print(f"Selection change not possible for: {option}; reason: {e}") 


        # get tab-relevant data for current EntryFrame()-object
        data = data_dict[self.tab]

        # update fields
        # for option in data.columns:
        for option in list(data.keys()):  #make iterator a list, in order to be able to modify it while iterating over it (see in checkbox-section)
            try:
                try: 
                    # value = data.loc[date, option] #get value for according field in df
                    value = data[option] #get value for according field in df
                    # print(option,": ", value) #uncomment for troubleshooting

                    if self.building_blocks[option]["type"] == "Checkbox":
                        __update_checkbox__(option, value)

                    elif self.building_blocks[option]["type"] == "Spinbox":
                        __update_spinbox__(option, value)

                    elif self.building_blocks[option]["type"] == "Entryfield":
                        __update_entryfield__(option, value)
                              
                    elif self.building_blocks[option]["type"] == "MultipleChoice":
                        __update_multichoice__(option, value)
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
        
    def focus_in(self, event):
        field = event.widget
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
        frame_info["translated_selection"] = tk.StringVar(value=0)
        frame_info["translation_dict"] = translate_dict = {}

        for counter, opt in enumerate(option_info["selection_menu"]):
            frame_info["translation_dict"][opt] = counter+1

        if "on_demand" in option_info.keys():
            ttk.Label(frame_info["frame"] ,text=label, width=17) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
            tk.OptionMenu(frame_info["frame"],
                            frame_info["selection"],
                            *option_info["selection_menu"],
                            command=lambda selection=frame_info["selection"], trans_dict=frame_info["translation_dict"],translated=frame_info["translated_selection"]: self.translate_multiChoice(selection, trans_dict, translated)
                            )
        else:
            ttk.Label(frame_info["frame"] ,text=label, width=17).grid(row=0, column=0, sticky="W", padx =(5,0))
            tk.OptionMenu(frame_info["frame"],
                            frame_info["selection"],
                            *option_info["selection_menu"],
                            command=lambda selection=frame_info["selection"], trans_dict=frame_info["translation_dict"],translated=frame_info["translated_selection"]: self.translate_multiChoice(selection, trans_dict, translated)
                            ).grid(row=0, column=1, sticky="W")

    def translate_multiChoice(self, selection, trans_dict, translated):
        '''
        Takes selected string from multiChoice-fields and converts value to numeric for insertion to database.

        Parameters:
            selection: str - selection/entry to tk.OptionMenu-object entry field
            trans_dict: dict - maps string value to numeric (dict created in create_multiChoice()-method)
            translated: tk.StringVar-object - numeric value saved here until insertion to database
        '''
        translated.set(trans_dict[selection])


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

        # bindings using input
        self.building_blocks[option_name]["entry_object"].bind("<Return>", lambda event: self.add_entry_to_entrylist(option_name=option_name))
        self.building_blocks[option_name]["entry_object"].bind("<FocusOut>", lambda event: self.add_entry_to_entrylist(option_name=option_name))
        # binding deleting placeholder text
        self.building_blocks[option_name]["entry_object"].bind("<FocusIn>", lambda event: self.focus_in(event))   


    def logout(self):
        print("Log Out Now!")
        root = self.master.master.master  #get root window, harboring switch_frame()-method
        root.user = None  #remove user
        root.switch_frame('LoginWindow')