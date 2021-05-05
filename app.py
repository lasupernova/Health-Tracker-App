import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from entry import create_entry_fields
from assets.entry_information import * 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# create tabs
app.layout = html.Div([
    # html.H1('Dash Tabs component demo'),
    html.Div([
        dcc.Tabs(id="tabs", value='tab-1-example', children=[
            dcc.Tab(id="mood",label='Mood', value='mood'),
            dcc.Tab(label='Health', value='health'),
            dcc.Tab(label='Food', value='food'),
            dcc.Tab(label='Fitness', value='fitness'),
            dcc.Tab(label='Period', value='period'),
            dcc.Tab(label='Sleep', value='sleep'),
            dcc.Tab(label='Longterm', value='longterm'),
        ],  vertical=False, parent_style={'float': 'left'}),
        html.Div(id='tabs-content-example', style={'float': 'left', 'width': '1000'})
    ])
])

#  add tab content as tabs' children using call back
@app.callback(Output('mood', 'children'),
              [Input('tabs', 'value')])
def render_content(tab, mood_info=mood_info):
    if tab == 'mood':
        return dcc.Checklist(
                            options=create_entry_fields(mood_info),
                            value=[]
                        )  
    elif tab == 'health':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])



if __name__ == '__main__':
    app.run_server(debug=True)