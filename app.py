import sys
import dash
from dash.dependencies import Input, Output, MATCH, State, ALL
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from entry import create_entry_fields
from assets.entry_information import * 
from assets.grains_seeds import g_and_s
from assets.fruits import fruits
from flask_app.dashapps.populate import return_full_entrytab
from datetime import datetime
from database.connections import db_transact
import ast

external_stylesheets = [dbc.themes.LUX]

tab_to_db = ''

entry_info = {'mood':mood_info, 'health':health_info, 'food':food_info, 
              'fitness': fitness_info, 'period':period_info, 'sleep':sleep_info, 'longterm':longterm_info}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_ignore='.*css.*', suppress_callback_exceptions=True)

# create tabs
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.ConfirmDialog(
        id='confirm',
        message='',
        ),
    html.Div([
        dbc.Row(
            [dbc.Col([
                dcc.Loading([
                    dcc.Tabs(className='row', id="tabs", value='tab-1-example', children=[
                        dcc.Tab(id='mood_tab', label='Mood', value='mood'),
                        dcc.Tab(id='health_tab', label='Health', value='health'),
                        dcc.Tab(id='food_tab', label='Food', value='food'),
                        dcc.Tab(id='fitness_tab', label='Fitness', value='fitness'),
                        dcc.Tab(id='period_tab', label='Period', value='period'),
                        dcc.Tab(id='sleep_tab', label='Sleep', value='sleep'),
                        dcc.Tab(id='longterm_tab', label='Longterm', value='longterm')
                    ],  vertical=False, parent_style={'float': 'left'})
                ], type='circle', fullscreen=True) 
            ], width = 9),
            dbc.Col([
                    dcc.DatePickerSingle(
                        id="date_picker",
                        date=datetime.today().date()),
                    html.Div(id="current_date", children=["BLUB"]),
                    html.Div(id="previous_date", hidden=True),    #division saving previous date to save last tab to db (-> no tab change necessary for saving data in final tab before switching dates)
                    html.Div(id="db_data", children=[], style={'display': 'none'})
                    ], width = "auto"),


        ]),
    html.Div(id="values_to_db", children=['None'], style={'display':'block'}),
    html.Div(id="values_to_db2", children=['None'], hidden=True),
    html.Div(id="test", children=['None'], style={'display':'block'})
    ])
])

@app.callback([Output('hover_test', 'title')], 
               Input('hover_test', 'title'))
def testHover(hoverdata):
    print(hoverdata)
    return ["SUCCESS!!"]

@app.callback([Output('mood_tab', 'children'),
               Output('health_tab', 'children'),
               Output('food_tab', 'children'),
               Output('fitness_tab', 'children'),
               Output('period_tab', 'children'),
               Output('sleep_tab', 'children'),
               Output('longterm_tab', 'children')],
              [Input('url', 'pathname')])   ##callback on page load
def display_page(pathname):
    """
    Fills in entry fields and graphs for each tab, based on information in assets.entry_information.py.
    Function will run when the URL pathname changes and will therefore be called on first dashboard start-up.
    NOTE: page will not be refreshed when (URL-)location is updated due to URL 'refresh'-parameter being set to 'False'.

    PARAMETERS:
        pathname - str

    Returns:
        lay out templates for each of the Outputs
    """
    if pathname=="/":
        return_vals = {}
        for k, v in entry_info.items():
            entry_options = return_full_entrytab(k, v)
            template=dbc.Row([
                dbc.Col(entry_options, id=f'{k}-content', width = "auto"), 
                dbc.Col([
                        dcc.Graph(
                            id=f'{k}_graph',
                            figure={
                                'data': [
                                    {'x': [1,2], 'y': [3,1]}
                                        ],
                                'layout': dict(title='Placeholder') 
                                },
                            style = dict(display='inline-block')
                        )
                        ], width = "auto")
                    ])
            return_vals[k] = template
    ## TO DO: modify to return ONE list in order to be more easily scalable later one
    return return_vals['mood'], return_vals['health'], return_vals['food'], return_vals['fitness'], return_vals['period'], return_vals['sleep'], return_vals['longterm']


# toggle entryfields for checkboxed for which additional info is necessary
@app.callback(Output({'name': MATCH, 'type': 'div'}, 'style'),
              [Input({'name': MATCH, 'type': 'check_toggle', "list":"entry"}, 'value')])
            #   ,State({'name': MATCH, 'type': 'div'}, 'style'))
def toggle_checkbox(check_button):
    """
    'Toggles' checkboxes on checkbox-click, by changing adjacent html.Div object style to show adjacent element (if available).

    Parameters:
        check_button - list: list will be empty of checkbox is not selected and will contain string (checkbox name/value) otherwise

    Returns:
        dict containing the style description that should be used for the adjacent html.Div object
    """
    if len(check_button) > 0:
        # print('SELECTED')  ##uncomment for troubleshooting
        return {'display': 'inline-block', 'width':'30%'}
    else:
        return {'display': 'none', 'width':'30%'}


def insert_database(data, tab, date, user='gabri'):
    '''
    Insert selection of current tab to database for specified date and logged in user

    Returns:
        void function
    '''
    print(f"Inserted into database: {data}")
    # append user and date to data
    data['date'] = date  #do not use today's date, in case Date Picker was used to change current health tracker date
    # insert into database
    db_transact.add_data(tab, data, user)

def send_to_db(tab, values, names, tab_to_db, date):
    """
    Sends entryfield data for specific tab to db for specific date and user.
    Function is used for 2 different callbacks with the following differences for the function call:
        - callback triggered by changed date in date_picker 
            date - previous date, as this callback is used to save data  in final tab to db without tab change
            tab_to_db -  is equal to tab (tab_to_db is only used to record filled in tab previous to tab change, which is not necessary when running this function using this callback, as tab did not change)
        - callback triggered by tab change (date - date currently selected in date_picker)
            date - current date (=date currently selected in date_picker)
            tab_to_db -  not equal to 'tab'-parameter, as function is used on tab change, but data for tab selected BEFORE tab change must be passed to db       
    
    Parameters:
        tab - str: value of currently selected tab
        values - list: list of current values for all entry fields (NOTE: only entry field values from current tab will be filtered out and be sent to database during any one callback)
        names - list: list of ids for all entry field values (see NOTE above)
        tab_to_db - str: tab name of tab/category entry field values to send to db
        date - str: date to use as value for db entry

    Returns:
        tab - str: tab name for currently selected tab --> will be saved to (['values_to_db[2]', 'children']) which will then serve as 'tab_to_db' when this function is called the next time 
    """
    # print('TAB TO DB: ', tab_to_db)  ##status of last tab (the one to send data to db for) is returned and saved
    if (tab != 'tab-1-example') and (tab_to_db != 'tab-1-example'):
        # print("VALUES: ", [x for x in zip(names, values)])  ##uncomment for troubleshooting
        info = {n['name']: v for n, v in zip(names, values) if n['name'].startswith(tab_to_db)} # and n['type'] != 'div' ##get only values when corresponding names contain category name as substring
        name = [k for k in info.keys()]
        values = [v for k, v in info.items()]
        type_ = [n['type'] for n in names if n['name'].startswith(tab_to_db)]  #and n['type'] != 'div') ##use startswith() instead of tab_to_db in n['name'], as 'health' also in 'food_unhealthy_food'
        to_db = {}
        print(len(name), len(values), len(type_))
        if len(name) != len(type_) != len(values):  ##need to be of same length in order to successfully pass data to db
                print("An Error Occured! Lengths of name, value and type lists are unequal!")
                return "ERROR!"
        for n, v, t in zip(name, values, type_):  #zip all three if type is 'div' for one - continue (as that will be a div as oppossed to a dcc)
            print(f"NAME: {n} - VALUE: {v}")
            if (t != 'div'):  #checklists that are not checked return empty list (if <empty_list> - returns False); other entryfields without entry will return None
                entry_name = "_".join(n.split('_')[1:])  ##first part of n is the category --> grab only relevant entry name like used in db
                if "check" in t:
                    if v:
                        entry_val = True
                    else:
                        entry_val = False
                else:
                    if v:
                        entry_val = v
                    else:
                        entry_val = None
                to_db[entry_name] = entry_val
                print(f"{entry_name} : {1 if (('check' in t) and v) else 0 if not v else v}")

            else:
                continue
                # print(f"Div: {n} - {v}")  ##uncomment for troubleshooting
        print(f">>>DATA: {to_db}")
        if len(to_db) > 0:
            insert_database(to_db, tab_to_db, date=date)
    return tab


# get values for all entry fields in current tab --> to be passed on to db in dict form
@app.callback(Output('values_to_db', 'children'),
              [Input('tabs', 'value')],
              [State({'name': ALL, 'type': ALL, "list":"entry"}, 'value'),
              State({'name': ALL, 'type': ALL, "list":"entry"}, 'id'),
              State('values_to_db', 'children'),
              State('date_picker', 'date')])
def to_db_from_current_date(tab, values, names, tab_to_db, date):
    return send_to_db(tab, values, names, tab_to_db, date)

# get values for all entry fields in current tab --> to be passed on to db in dict form (without tab change, but triggered by date change)
@app.callback([Output('values_to_db2', 'children'),
               Output('previous_date', 'children')],
              [Input('date_picker', 'date')],
              [State({'name': ALL, 'type': ALL, "list":"entry"}, 'value'),
              State({'name': ALL, 'type': ALL, "list":"entry"}, 'id'),
              State('previous_date', 'children'),
              State('tabs', 'value')])
def to_db_from_previous_date(date, values, names, prev_date, tab):
    print(f"TAB: {tab}; TAB TO DB: {tab_to_db}")
    if prev_date:
        return send_to_db(tab, values, names, tab, prev_date), date  #NOTE: parameters 'tab' and 'tab_to_db' are same for this call
    else:
        print(f"to_db_from_previous_date: no action as prev_date is {prev_date}")
        return tab, date


# get values from date picker
@app.callback([Output("current_date", 'children'),
               Output("db_data", 'children')],
              [Input("date_picker", 'date')])
def change_date(date_):
    """
    Function triggered by callback for date-picker date change.
    Date needs to be converted from string to datetime object in order to be passed on to
    database query.
    Values for new date and specified user are retrieved and
    return retrieved data and a status message that is printed to dashboard.

    Parameters:
        date - str: date selected from date-picker in string format

    Returns:
        status message - str: message (data loaded/no data for this date) passed to "current_date" html.Div
        data - str: returned data is passed to hidden db_data html.Div children, which in turn triggers follow-up callback
        (NOTE: str(data) instead od data returned as a workaround, as children of html.Div-objects can NOT be objects, but need to be strings)
    """
    ##status of last tab (the one to send data to db for) is returned and saved
    date_conv = datetime.strptime(date_, '%Y-%m-%d')

    data = db_transact.query_data_by_date_and_user(date_conv, user='gabri', end_date=None)
    print(f">>>>DATE (change_date): {data}")
    if data != 2:
        return "Data for selected date loaded", str(data)
    else:
        return "No data for this date yet!", "No data for this date yet!"


def db_vals_to_list(data_dict, values, ids):
    """
    Iterates over current entry values and replaces each value:
    with db value (if entry available in db for specified date and user) 
    or 
    [] (checklist entry fields) or "" (non-checklist entry fields) if no value returned from db.
    NOTE: "" and not None used for empty value in non-checkfields, as None would not remove entry from previous date in entryfield

    Parameters:
        data - dict: dict of values returned from db for each entry per category
        values - list: current values for all entry fields
        ids - list: ids for all entry fields in specified form (e.g {"name":xxx, "type:"yyy})

    Returns:
        values_for_date - list: list of values to fill into dashboard entry field in correct order (corresponding to order from values/ids)
    """
    values_for_date = []

    for id_, val in zip(ids, values):  

        #extract category, entry_name and entry_type for each entry_id from composite id including {"name":xxx, "type":yyy}
        entry_type = id_['type']
        category = id_["name"].split("_")[0]
        entry_name = "_".join(id_["name"].split("_")[1:])

        # check if value was returned from db for current entry, otherwise append empty value (depending on entry type)
        try:
            db_val = data_dict[category][entry_name] if data_dict[category][entry_name] else ""
            print(f"{entry_name}: {db_val}")
            # multiple values (per entry) are returned from db as string with values surrounded by "{}" --> convert to list with individual values
            if type(db_val)==str and "{" in db_val:
                db_val = db_val.strip("{}")
                db_val = db_val.replace('"', '').split(",")
        except:
            empty_val = [] if "check" in entry_type else ""
            values_for_date.append(empty_val)
            continue

        if ('check' in entry_type):
            current_val = [entry_name] if db_val==True else []
            values_for_date.append(current_val)

        elif (entry_type == "permanent"):
            values_for_date.append(db_val)
        
        elif entry_type == "on_demand":  #only fill on-demand fields if correspongding caller was checked
            caller_name = "_".join(entry_name.split("_")[:-1])
            try:
                caller_value = data_dict[category][caller_name]
            except:
                caller_value = None
            if caller_value:
                values_for_date.append(db_val)
            else:
                values_for_date.append("")  ##HERE
    return values_for_date

@app.callback(Output({"name": ALL ,"type":ALL, "list":"entry"}, 'value'),
              [Input("db_data", 'children')],
              [State({"name": ALL ,"type":ALL, "list":"entry"}, 'value'),
              State({"name": ALL ,"type":ALL, "list":"entry"}, 'id')])
def fill_entryfields(data, values, ids):  #fill entry field values
    """
    Fills entry fields with values based on current date (as per date-picker) and user.
    Correct entry field order is determined by taking in all entryfield ids (+values),
    iterating over these and assign the values retrieved from db to them by returning 
    a tuple of values in the correct order.
    Database values are passed as "data" parameter, which is a dict in string form
    -> this data string is converted back to dict-format using as.literal_eval().

    Parameters:
        data - str: data retrieved from db as a dict in string form
        values - list: list of current entry field values 
        ids - list: list of entry field ids

    Returns:
        values_for_date/vals - list: list of retrieved values in correct order and format for corresponding entry fields
    """
    if data == "No data for this date yet!":
        vals = [[] if "check" in entry_type["type"] else None for entry_type in ids]
        return vals
    else:
        data_dict = ast.literal_eval(data)   ##convert data string into dict

        values_for_date = db_vals_to_list(data_dict, values, ids)
        print(f">>>>RESULTS: {values_for_date} number of return vals {len(values_for_date)}")
        return values_for_date


if __name__ == '__main__':
    app.run_server(debug=True) 