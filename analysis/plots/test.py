import pandas as pd
from matplotlib.figure import Figure

def make_plot():
    fig = Figure(figsize=(2,2))
    ax = fig.add_subplot(111)
    x = [1,2,3,4,5,6,7,8]
    y= [2,4,6,8,10,12,14,16]

    ax.scatter(x,y)
    return fig
    quit()