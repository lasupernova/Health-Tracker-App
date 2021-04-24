from PIL import Image
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
import numpy as np 
from database.connections import db_transact

def create_cloud(feature_dict, feature_name):

    end_date = None
    start_date = None
    user = 'gabri'
    columns=['unhealthy_food', 'date']
    table = 'food'
    # get data
    data = db_transact.query_data_between_dates_by_user(user, start_date=start_date, end_date=end_date, table=table, columns=columns)   #returns list of tuples

    if not data:
        return -1

    data_values = [tup[0:-1] for tup in data]   #extract values from each tuple
    date = [tup[-1] for tup in data] 

    print(data_values)
    # def custom_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    #     return(f"hsl(322, {np.random.randint(15,100)}%, {np.random.randint(0,50)}%)")

    # wc = WordCloud(background_color="whitesmoke",
    #                width=1500,
    #                height=1000, 
    #                max_words=100,
    #                prefer_horizontal=0.8,
    #                normalize_plurals=False).generate_from_frequencies(feature_dict)

    # # show
    # plt.figure(figsize=[50,30])
    # plt.imshow(wc.recolor(color_func = custom_color_func), interpolation="sinc")
    # plt.axis("off")
    # plt.savefig(f'media\plots\.archive\{feature_name}.png')
    # print(">>>> FINISHED!!!")

if __name__=="__main__":
    create_cloud('lala', "new2")