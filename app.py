# TO DO: create function creating children-return value for callback function

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
        dbc.Row([dcc.Tabs(className='row', id="tabs", value='tab-1-example', children=[
            dcc.Tab(id='mood_tab', label='Mood', value='mood'),
            dcc.Tab(id='health_tab', label='Health', value='health'),
            dcc.Tab(id='food_tab', label='Food', value='food'),
            dcc.Tab(id='fitness_tab', label='Fitness', value='fitness'),
            dcc.Tab(id='period_tab', label='Period', value='period'),
            dcc.Tab(id='sleep_tab', label='Sleep', value='sleep'),
            dcc.Tab(id='longterm_tab', label='Longterm', value='longterm'),
        ],  vertical=False, parent_style={'float': 'left'})])

    ]),
    html.Div(id="values_to_db", children=['None'], style={'display':'block'}),
    html.Div(id="test", children=['None'], style={'display':'block'})
])

# def test():
#     for k, v in entry_info.items():
#         # if tab == k:
#         entry_options = return_full_entrytab(v)
#         return entry_options
@app.callback([Output('mood_tab', 'children'),
               Output('health_tab', 'children'),
               Output('food_tab', 'children'),
               Output('fitness_tab', 'children'),
               Output('period_tab', 'children'),
               Output('sleep_tab', 'children'),
               Output('longterm_tab', 'children')],
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname=="/":
        return_vals = {}
        for k, v in entry_info.items():
            entry_options = return_full_entrytab(k, v)
            template=dbc.Row([
                dbc.Col(entry_options, id=f'{k}-content', width = "auto"), 
                dbc.Col([
                        dcc.Graph(
                            id='{k}_graph',
                            figure={
                                'data': [
                                    {'x': [1,2], 'y': [3,1]}
                                        ],
                                'layout': dict(title='Placeholder') 
                                },
                            style = dict(display='inline-block')
                        )
                        ], width = "auto"),
                dbc.Col([
                        dcc.DatePickerSingle(
                            id='{k}-startdate-input',
                            date=datetime.today().date()),
                        html.Div(id='{k}-picked_date', children=[])
                        ], width = "auto") 
                    ])
            return_vals[k] = template
    return return_vals['mood'], return_vals['health'], return_vals['food'], return_vals['fitness'], return_vals['period'], return_vals['sleep'], return_vals['longterm']
    # return True, f"The pathname is: {pathname}"

# #  add tab content as tabs' children using call back
# @app.callback(Output('tabs-content', 'children'),
#               [Input('tabs', 'value')],
#               State('tabs-content', 'children'))
# def render_content(tab, info):
#     # if info:  ##uncomment for troubleshooting
#     #     # print(info[0]['props'])
#     #     for x in info:
#     #         if 'id' in x['props'].keys():
#     #             print(x['props']['id']['name'], '\n')
#     #         else:
#     #             pass
#     #     print('\n')
#     for k, v in entry_info.items():
#         if tab == k:
#             entry_options = return_full_entrytab(v)
#             return entry_options

# toggle entryfields for checkboxed for which additional info is necessary
@app.callback(Output({'name': MATCH, 'type': 'div'}, 'style'),
              [Input({'name': MATCH, 'type': 'check_toggle'}, 'value')])
            #   ,State({'name': MATCH, 'type': 'div'}, 'style'))
def toggle_checkbox(check_button):
    if len(check_button) > 0:
        # print('SELECTED')  ##uncomment for troubleshooting
        return {'display': 'inline-block', 'width':'30%'}
    else:
        return {'display': 'none', 'width':'30%'}


def insert_database(data, tab, user='gabri', date=datetime.now().date()):
    '''
    Insert selection of current tab to database for specified date and logged in user
    '''

    print(f"Inserted into database: {data}")
    # append user and date to data
    data['date'] = date  #do not use today's date, in case Date Picker was used to change current health tracker date

    # insert into database
    db_transact.add_data(tab, data, user)


# get values for all entry fields in current tab --> to be passed on to db in dict form
@app.callback(Output('values_to_db', 'children'),
              [Input('tabs', 'value')],
              [State({'name': ALL, 'type': ALL}, 'value'),
              State({'name': ALL, 'type': ALL}, 'id'),
              State('values_to_db', 'children')])
def send_to_db(tab, values, names, tab_to_db):
    # print('TAB TO DB: ', tab_to_db)  ##status of last tab (the one to send data to db for) is returned and saved
    if (tab != 'tab-1-example') and (tab_to_db != 'tab-1-example'):
        print("VALUES: ", [x for x in zip(names, values)])
        info = {n['name']: v for n, v in zip(names, values) if (n['name'].startswith(tab_to_db) and n['type'] != 'div')}  ##get only values when corresponding names contain category name as substring
        name = [k for k in info.keys()]
        values = [v for k, v in info.items()]
        type_ = [n['type'] for n in names if (n['name'].startswith(tab_to_db) and n['type'] != 'div')]  ##use startswith() instead of tab_to_db in n['name'], as 'health' also in 'food_unhealthy_food'
        to_db = {}
        print(len(name), len(values), len(type_))
        if len(name) != len(type_) != len(values):  ##need to be of same lenght in order to successfully pass data to db
                print("An Error Occured! Lengths of name, value and type lists are unequal!")
                return "ERROR!"
        for n, v, t in zip(name, values, type_):  #zip all three if type is 'div' for one - continue (as that will be a div as oppossed to a dcc)
            print(f"NAME: {n} - VALUE: {v}")
            if (t != 'div'):  #checklists that are not checked return empty list (if <empty_list> - returns False); other entryfields without entry will return None
                entry_name = "_".join(n.split('_')[1:])  ##first part of n is the category --> grab only relevant entry name like used in db
                to_db[entry_name] = True if (('check' in t) and v) else False if not v else v
                print(f"{entry_name} : {1 if (('check' in t) and v) else 0 if not v else v}")

            else:
                continue
                # print(f"Div: {n} - {v}")  ##uncomment for troubleshooting
        print(f">>>DATA: {to_db}")
        if len(to_db) > 0:
            insert_database(to_db, tab_to_db)
    return tab

# # get date information stored in database
# @app.callback(Output(None, 'None'),
#               [Input('startdate-input', 'value')])
#             #   ,State({'name': MATCH, 'type': 'div'}, 'style'))
# def get_date_info(date):
#     print(date)
#     return date

# get values from date picker
@app.callback(Output('picked_date', 'children'),
              [Input('startdate-input', 'date')])
def change_date(date):
    print(f'DATE PICKED: {date}')  ##status of last tab (the one to send data to db for) is returned and saved
    date_conv = datetime.strptime(date, '%Y-%m-%d')
    print(date_conv)
    test = db_transact.query_data_by_date_and_user(date_conv, user='gabri', end_date=None)
    if test != 2:
        return str(test)
    else:
        return "No data for this date yet!"

# @app.callback(Output('test', 'children'),
#               [Input({'name':'health_medication', 'type': 'check_toggle'}, 'value')])
# def testing(test):
#     print(f"CURRENT VALUE: {test}")
#     return test

if __name__ == '__main__':
    app.run_server(debug=True) 