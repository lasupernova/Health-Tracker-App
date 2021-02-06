import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
from pandas import Timestamp
from matplotlib import colors as mcolors
import matplotlib
import datetime
import math
import os

def plot_sleep(period=14): 
    # import data
    df = pd.read_csv(f"frames{os.sep}analysis{os.sep}test_df.csv", index_col= 0, parse_dates=True, header=[0, 1], skipinitialspace=True)

    # sort dates
    df.sort_index(inplace=True)

    # save data from last 7 days in separate dataframe
    average_sleep_period = df.sleep.sleep.to_frame().tail(period).copy()

    # get 3-lettter weekday abbreviation from index
    weekday_index = [ind.strftime('%a') for ind in average_sleep_period.index] 
    print(weekday_index)

    #create figure and add axis
    fig = Figure(figsize=(6,2))
    ax = fig.add_subplot(111)

    # create bar plots for sleepgin time of last 7 days
    df.sleep.sleep.to_frame().tail(period).plot(kind="bar", ax=ax)

    # aestetics
    plt.xticks(list(range(len(weekday_index))), weekday_index, rotation=0) #change xtick-labels to 3-letter weekday names and no rotation
    plt.tick_params(left=False, bottom=False,) #remove ticks
    plt.box(False) #remove box

    # return figure
    return fig
    quit()