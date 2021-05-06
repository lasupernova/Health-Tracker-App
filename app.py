import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from entry import create_entry_fields
from assets.entry_information import * 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# create tabs
app.layout = html.Div([
    # html.H1('Dash Tabs component demo'),
    html.Div([
        dbc.Row([dcc.Tabs(className='row', id="tabs", value='tab-1-example', children=[
            dcc.Tab(id="mood",label='Mood', value='mood'),
            dcc.Tab(label='Health', value='health'),
            dcc.Tab(label='Food', value='food'),
            dcc.Tab(label='Fitness', value='fitness'),
            dcc.Tab(label='Period', value='period'),
            dcc.Tab(label='Sleep', value='sleep'),
            dcc.Tab(label='Longterm', value='longterm'),
        ],  vertical=False, parent_style={'float': 'left'})]),
        dbc.Col([html.Div(id='tabs-content-example')])
    ])
])

#  add tab content as tabs' children using call back
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'mood':
        checklist, sliders = create_entry_fields(mood_info)
        return dcc.Checklist(
                            options=checklist,
                            value=[]
                        )  
    elif tab == 'health':
        checklist, sliders = create_entry_fields(health_info)
        entry_fields = []
        if len(checklist) > 0:
            entry_fields.append(dcc.Checklist(options=checklist, value=[]))
        for slider in sliders:
            param = slider['label']
            min_ = slider['min']
            max_ = slider['max']
            step = slider['step']
            new_spinbox = dcc.Input(
                                    id=param, 
                                    type='number', 
                                    min=min_, 
                                    max=max_, 
                                    step=step)  
            new_div =    html.Div([
                                html.Div([html.P(param)],style={'margin-right': '5px', 'display': 'inline-block'}),
                                html.Div([new_spinbox],style={'display': 'inline-block'})
                                ])
            entry_fields.append(new_div)
        return entry_fields

# marks={i: 'Label {}'.format(i) for i in range(10)}, --> add based on min-max-increment info

if __name__ == '__main__':
    app.run_server(debug=True)