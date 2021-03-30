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
import database.connections.db_transact as db_transact

def plot_cycle(user, date): 
    '''
    Plots last 3 cycles
    '''

    end_date = date - datetime.timedelta(weeks=13)
    start_date = end_date - datetime.timedelta(weeks=6)
    
    columns=['cycle_day', 'date']
    table = 'period'
    # get data
    data = db_transact.query_data_between_dates_by_user(user, start_date, end_date, table=table, columns=columns)   #returns list of tuples
    data_values = [tup[0:-1] for tup in data]   #extract values from each tuple
    date = [tup[-1] for tup in data] 

    # create dataframe from data
    print(columns[:-1])
    df = pd.DataFrame(data=data_values, index=date, columns=columns[:-1])
    print(df)

    #find local maxima
    locMax = df['cycle_day'][(df['cycle_day'].shift(1) < df['cycle_day']) & (df['cycle_day'].shift(-1) < df['cycle_day'])]
    #get local maxima mean
    cycleLengthMean = locMax.mean()
    cycleLengthMedian = locMax.median()

    # # cycle length based on ONLY the last 4 periods ---> later for when more health tracker data is available
    # cycleLengthCurrent = locMax[-4:].mean()

    # ----- calculate fertile window based ONLY on last 4 periods ----- ---> later for when more health tracker data is available, NOW: only with available

    # ovulation - occurs 14 days before period start
    # ovulation = math.ceil(cycleLengthCurrent - 14)
    ovulation = math.ceil(cycleLengthMean - 14)
    # the fertile window starts 5- 6 days before ovulation
    fertile_start = ovulation - 5
    # the most fertile window start 2- 3 days before ovulation
    fertile_high = ovulation - 3
    # fertilization can occur up to 24 after ovulation
    fertile_trail = ovulation + 1

    fig = plt.figure(figsize=(8,3))
    ax = fig.add_subplot(111)
    # # x = [1,2,3,4,5,6,7,8]
    # # y= [2,4,6,8,10,12,14,100]

    # ax.scatter(df['cycle_day'], df.index, c='red')
    df['cycle_day'].plot(kind='bar',ax=ax, color='red')
    plt.axhline(y=cycleLengthMedian,xmin=0,xmax=1,color='red')
    plt.axhline(y=cycleLengthMean,xmin=0,xmax=1,color='pink')
    plt.xticks([],[])
    # # print(df.index)
    return fig
    # quit()