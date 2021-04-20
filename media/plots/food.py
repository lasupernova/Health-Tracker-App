from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def create_cloud(dict):
    def custom_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
        return(f"hsl(322, {np.random.randint(15,100)}%, {np.random.randint(0,50)}%)")

    wc = WordCloud(background_color="white",
                   width=1500,
                   height=1000, 
                   max_words=100,
                   prefer_horizontal=0.8,
                   normalize_plurals=False).generate_from_frequencies(fruits_prod_count)

    # show
    plt.figure(figsize=[50,30])
    plt.imshow(wc.recolor(color_func = custom_color_func), interpolation="sinc")
    plt.axis("off")
    plt.show()