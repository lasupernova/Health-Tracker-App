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

external_stylesheets = [dbc.themes.LUX]

entry_info = {'mood':mood_info, 'health':health_info, 'food':food_info, 
              'fitness': fitness_info, 'period':period_info, 'sleep':sleep_info, 'longterm':longterm_info}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_ignore='.*css.*')

# create tabs
app.layout = html.Div([
    # html.H1('Dash Tabs component demo'),
    html.Div([
        dbc.Row([dcc.Tabs(className='row', id="tabs", value='tab-1-example', children=[
            dcc.Tab(id={"name":"mood", "type":"tab"},label='Mood', value='mood'),
            dcc.Tab(label='Health', value='health'),
            dcc.Tab(label='Food', value='food'),
            dcc.Tab(label='Fitness', value='fitness'),
            dcc.Tab(label='Period', value='period'),
            dcc.Tab(label='Sleep', value='sleep'),
            dcc.Tab(label='Longterm', value='longterm'),
        ],  vertical=False, parent_style={'float': 'left'})]),
        dbc.Col([html.Div(id='tabs-content-example')])
    ]),
    html.Div(id="values_to_db", children=['None'], style={'display':'none'})
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
              [Input({'name': MATCH, 'type': 'check_toggle'}, 'value')],
              State({'name': MATCH, 'type': 'div'}, 'style'))
def render_content(check_button, state):
    if len(check_button) > 0:
        # print('SELECTED')  ##uncomment for troubleshooting
        return {'display': 'inline-block', 'width':'30%'}
    else:
        return {'display': 'none', 'width':'30%'}

# get values for all entry fields in current tab --> to be passed on to db 
@app.callback(Output('values_to_db', 'children'),
              [Input('tabs', 'value')],
              [State({'name': ALL, 'type': ALL}, 'value'),
              State({'name': ALL, 'type': ALL}, 'id')])
def render_content(tab, values, names):
    name = [n['name'] for n in names]
    print(f"TAB: {tab}")
    for n, v in zip(name, values):
        print(f"{n}: {v}")

if __name__ == '__main__':
    app.run_server(debug=True)