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

def plot_cycle(): 
    df = pd.read_csv(f"frames{os.sep}analysis{os.sep}test_df.csv", index_col= 0, header=[0, 1], skipinitialspace=True)
    df = df[['vaginal','health','mood']].copy()
    df.index = pd.to_datetime(df.index, format = '%Y-%m-%d')

    #find local maxima
    locMax = df[('vaginal','cycle day')][(df[('vaginal','cycle day')].shift(1) < df[('vaginal','cycle day')]) & (df[('vaginal','cycle day')].shift(-1) < df[('vaginal','cycle day')])]
    #get local maxima mean
    cycleLengthMean = locMax.mean()
    cycleLengthMedian = locMax.median()

    # cycle length based on ONLY the last 4 periods
    cycleLengthCurrent = locMax[-4:].mean()

    # ----- calculate fertile window based ONLY on last 4 periods -----

    # ovulation - occurs 14 days before period start
    ovulation = math.ceil(cycleLengthCurrent - 14)
    # the fertile window starts 5- 6 days before ovulation
    fertile_start = ovulation - 5
    # the most fertile window start 2- 3 days before ovulation
    fertile_high = ovulation - 3
    # fertilization can occur up to 24 after ovulation
    fertile_trail = ovulation + 1

    fig = Figure(figsize=(2,2))
    ax = fig.add_subplot(111)
    # x = [1,2,3,4,5,6,7,8]
    # y= [2,4,6,8,10,12,14,100]

    # ax.scatter(x,y, c='red')
    df[('vaginal','cycle day')].plot(kind='bar',ax=ax)
    mean = df[('vaginal','cycle day')].mean()
    plt.axhline(y=cycleLengthMedian,xmin=0,xmax=1,color='red')
    plt.axhline(y=cycleLengthMean,xmin=0,xmax=1,color='pink')
    plt.xticks([],[])
    # print(df.index)
    return fig
    quit()