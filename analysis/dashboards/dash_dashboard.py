import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd


# import data
df = pd.read_csv('test_df.csv', index_col= 0, parse_dates=True, header=[0, 1], skipinitialspace=True)
# sort df by index
df = df.sort_index()

# get sleep data for last 2 weeks
sleep14 = df.sleep.iloc[-14:]
hours_slept = sleep14.sleep.values
idx = sleep14.index
print(type(idx)) # check that idx is a datetime object


# initiate dash-object - similar to flask
app = dash.Dash()

np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

app.layout = html.Div([
    dcc.Graph(
        id='scatter3',
        figure={
            'data': [
                go.Scatter(
                    x = idx,
                    y = hours_slept,
                    mode = 'markers+lines',
                    marker = {
                                'size': 5,
                                'color': 'darkslategrey',
                                'symbol': 'star',
                                'line': dict(
                                            width=0.5, 
                                            color='grey'
                                            )
                        },
                    text=[f'Sleep score: {int(score)}' for score in sleep14['sleep score']]
                )
            ],
            'layout': go.Layout(
                title = 'Interactive Plot',
                xaxis = {'title': 'Date'},
                yaxis = {'title': 'Hours slept'},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server()