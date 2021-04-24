from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np 
from database.connections import db_transact

def get_data(start_date=None, end_date=None):
    """
    Get data from database

    Parameters:
        start_date: start date to query from (default: None)
        end_date: end date to query to (default: None)

    Returns:
        data_values: a list containing the returned data from query
        date: a list containing the corresponding dates
    """

    user = 'gabri'
    columns=['unhealthy_food', 'date']
    table = 'food'
    # get data
    data = db_transact.query_data_between_dates_by_user(user, start_date=start_date, end_date=end_date, table=table, columns=columns)   #returns list of tuples

    if not data:
        return -1

    data_values = [tup[0:-1] for tup in data]   #extract values from each tuple
    date = [tup[-1] for tup in data] 

    return data_values, date

def get_counts_from_list(data):
    """
    Creates and returns a dict counting all items appearing in a pandas Series.
        - saves all series values into a list
        - iterates over list and saves values and value count in a dict
        - orders dict by value count
        - returns dict
        
    Parameters:
        data - pandas Series
    """
    # ----- clean data in initial list -----
    # clean data and save new cleaned items into list --> will be a list of lists with some items containing more than 1 string
    cleaned = [item.strip(" '[]").replace("'","").split(",") for day_data in data for item in day_data if item != None]

    temp_data = []
    for i in cleaned:  # add all individual strings in lists to temp_data
        temp_data.extend(i)

    # strip any whitespace
    data_list = [i.strip() for i in temp_data if i != ""]

    # ----- create counter_dict ------
    counter_dict = {}
    for food in data_list:
            if type(food) == list:
                print(food)
            else:
                if food == 'nan' or food == '' or food.isdigit():
                    continue
                elif food not in counter_dict.keys():
                    counter_dict[food] = 1
                else:
                    counter_dict[food] += 1
    
    ordered_dict = {k: v for k, v in sorted(counter_dict.items(), key=lambda item: item[1], reverse=True)}  #order dict by count
    print(ordered_dict)
    return ordered_dict

def create_cloud(feature_dict, feature_name):
    """
    Creates word cloud from data dict and saves the output to a .png file.

    Parameters:
        feature_dict: a dict - containing count information for each item captured in dict 
        feature_name: a string - name to save the dict as in .archive folder

    Returns:
        void function
    """
    def custom_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
        return(f"hsl(322, {np.random.randint(15,100)}%, {np.random.randint(0,50)}%)")

    wc = WordCloud(background_color="whitesmoke",
                   width=1500,
                   height=1000, 
                   max_words=100,
                   prefer_horizontal=0.8,
                   normalize_plurals=False).generate_from_frequencies(feature_dict)

    # show
    plt.figure(figsize=[50,30])
    plt.imshow(wc.recolor(color_func = custom_color_func), interpolation="sinc")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f'media\plots\.archive\{feature_name}.png')
    print(f">>>> Plots: {feature_name} Word Cloud finished")

if __name__=="__main__":
    data, dates = get_data()
    data_dict = get_counts_from_list(data)