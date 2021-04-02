import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
from pandas import Timestamp
from matplotlib import colors as mcolors
import matplotlib.ticker as mticker
import matplotlib
import datetime
import math
import os
import database.connections.db_transact as db_transact

# def set_BoxColors(bp):
#     setp(bp['boxes'][0], color='blue')
#     setp(bp['caps'][0], color='blue')
#     setp(bp['whiskers'][0], color='blue')
#     setp(bp['fliers'][0], color='blue')
#     setp(bp['medians'][0], color='blue')

BG_COLOR = "whitesmoke"

def plot_sleep(user, date): 
    '''
    Plots sleep information
    '''

    end_date = date - datetime.timedelta(weeks=13)
    start_date = end_date - datetime.timedelta(weeks=7)
    
    columns=['sleep', 'date']
    table = 'sleep'
    # get data
    data = db_transact.query_data_between_dates_by_user(user, start_date, end_date, table=table, columns=columns)   #returns list of tuples
    data_values = [tup[0:-1] for tup in data]   #extract values from each tuple
    date = [tup[-1] for tup in data] 

    # create dataframe from data
    df = pd.DataFrame(data=data_values, index=date, columns=columns[:-1])
    df['month'] = df.index.month
    df['weekday'] = df.index.strftime("%a")

    # create new df ordered by weekday
    cats = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df_by_weekday = df.copy()
    df_by_weekday['weekday'] = pd.Categorical(df['weekday'], categories=cats, ordered=True)
    df_by_weekday = df_by_weekday.sort_values('weekday')

    print(df_by_weekday)

    fig = Figure(figsize=(7,4))
    fig.patch.set_facecolor(BG_COLOR)

    # ----- ax1 -----
    ax = fig.add_subplot(121)

    for counter, month in enumerate(df.month.unique()):
        ax.boxplot(df.sleep[df.month == month], positions=[counter])
    ax.xaxis.set_ticklabels(df.month.unique())
    ax.set_facecolor(BG_COLOR)

    for axis in ax.spines:
        ax.spines[axis].set_visible(False)  #changed from: sns.despine(left=True, bottom = True)
    fig.tight_layout()

    # ------ ax2 ----- 
    ax2 = fig.add_subplot(122)

    for counter, weekday in enumerate(df_by_weekday.weekday.unique()):
        ax2.boxplot(df_by_weekday.sleep[df_by_weekday.weekday == weekday], positions=[counter])
    ax2.xaxis.set_ticklabels(df_by_weekday.weekday.unique())
    ax2.set_facecolor(BG_COLOR)

    for axis in ax2.spines:
        ax2.spines[axis].set_visible(False)  #changed from: sns.despine(left=True, bottom = True)
    fig.tight_layout()

    return fig




