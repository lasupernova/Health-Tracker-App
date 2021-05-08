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

external_stylesheets = [dbc.themes.LUX]

entry_info = {'mood':mood_info, 'health':health_info, 'food':food_info, 
              'fitness': fitness_info, 'period':period_info, 'sleep':sleep_info, 'longterm':longterm_info}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_ignore='.*css.*')

# create tabs
app.layout = html.Div([
    # html.H1('Dash Tabs component demo'),
    html.Div([
        dbc.Row([dcc.Tabs(className='row', id="tabs", value='tab-1-example', children=[
            dcc.Tab(label='Mood', value='mood'),
            dcc.Tab(label='Health', value='health'),
            dcc.Tab(label='Food', value='food'),
            dcc.Tab(label='Fitness', value='fitness'),
            dcc.Tab(label='Period', value='period'),
            dcc.Tab(label='Sleep', value='sleep'),
            dcc.Tab(label='Longterm', value='longterm'),
        ],  vertical=False, parent_style={'float': 'left'})]),
        dbc.Col([html.Div(id='tabs-content-example')])
    ]),
    html.Div(id="values_to_db", children=['None'], style={'display':'block'})
])

#  add tab content as tabs' children using call back
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')],
              State('tabs-content-example', 'children'))
def render_content(tab, info):
    if info:
        for x in info['props']['children']:
            print(x.keys())
        print('\n')
    for k, v in entry_info.items():
        if tab == k:
            entry_options = return_full_entrytab(v)
            return entry_options

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


def insert_database(data, user='gabri', date=datetime.now().date()):
    '''
    Insert selection of current tab to database for specified date and logged in user
    '''

    # keep only values that have been entered in data-dict (--> exclude default values)
    for key, value in data.items():
        if self.value_entry_record == False:
            del data[key]

    print(f"Inserted into database: {data}")
    # append user and date to data
    data['date'] = date  #do not use today's date, in case Date Picker was used to change current health tracker date

    # insert into database
    db_transact.add_data(self.tab, data, user)


# get values for all entry fields in current tab --> to be passed on to db in dict form
@app.callback(Output('values_to_db', 'children'),
              [Input('tabs', 'value')],
              [State({'name': ALL, 'type': ALL}, 'value'),
              State({'name': ALL, 'type': ALL}, 'id')])
def send_to_db(tab, values, names):
    name = [n['name'] for n in names]
    type_ = [n['type'] for n in names]
    to_db = {}
    for n, v, t in zip(name, values, type_):  #zip all three if type is 'div' for one - continue (as that will be a div as oppossed to a dcc)
        if (t != 'div') and v:  #checklists that are not checked return empty list (if <empty_list> - returns False); other entryfields without entry will return None
            to_db[n] = 1 if 'check' in t else v
            print(f"{n} : {1 if 'check' in t else v}")

        else:
            continue
            # print(f"Div: {n} - {v}")  ##uncomment for troubleshooting

    return str(to_db)

if __name__ == '__main__':
    app.run_server(debug=True) 