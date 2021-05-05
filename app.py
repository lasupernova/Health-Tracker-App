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
        # for slider in sliders:
        #     dcc.Slider(
        #             min=-5,
        #             max=10,
        #             step=0.5,
        #             value=-3
        #         )  
        return [
            dcc.Checklist(
                            options=checklist,
                            value=[]
                        ),
            dcc.Slider(
                    min=-5,
                    max=10,
                    step=0.5,
                    value=-3
                )  
        ]



if __name__ == '__main__':
    app.run_server(debug=True)