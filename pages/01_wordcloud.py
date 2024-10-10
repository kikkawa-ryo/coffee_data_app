import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum
import emoji

# サイドバー
with st.sidebar:
    st.page_link("app.py", label="ホーム", icon="🏠")
    st.page_link("pages/viz_scatterplot.py", label="scatterplot", icon="📈")
    st.page_link("pages/viz_lineplot.py", label="lineplot", icon="📈")
    st.page_link("pages/viz_barplot.py", label="barplot", icon="📊")
    st.page_link("pages/02_boxplot.py", label="boxplot", icon="📊")
    st.page_link("pages/01_wordcloud.py", label="wordcloud", icon="🍷")
    st.page_link("pages/gallery.py", label="gallery", icon="🖼")

df = pd.read_csv('data/sample.csv').sort_values(['year', 'country', 'rank_no'], ascending=[False, True, True]).reset_index(drop=True)


# Flavor Wheel
st.subheader('Coffee Flavor Wheel')
st.image('images/flavor-wheel-en.png', caption='Coffee Flavor Wheel')

# wordcloud
from collections import Counter
from wordcloud import WordCloud
st.subheader("Word Cloud")

#####
from utils.wordcloud_color_generator import SimpleGroupedColorFunc, GroupedColorFunc
color_to_words = {
        '#CF5552': ["berry",  'blackberry','raspberry','blueberry','strawberry'],
        '#BC5245': ["dried fruit",  'raisin','prune'],
        '#E47050': ['coconut','cherry','pemegranate','pineapple','grape','apple','peach','pear'],
        '#F69114': ["citrus",  'grapefruit','orange','lemon','lime'],
        '#DABB0B': ["sour",  'acetic','butyric','isovaleric','citric','malic'],
        '#A1881E': ["alcohol", 'winey','whiskey','fermented','overripe'],
        '#92A516': ['olive'],
        '#5C7921': ['flaw'],
        '#2C9640': ["green","vegetative",  'under ripe','peapod','fresh','dark green','hay','herb'],
        '#4C8B6C': ['beafy'],
        '#8BA3A9': ["papery","musty",  'stale','cardboard','papery','woody','moldy','damp','musty','dusty','earthy','animalic','meaty','brothy','phenolic'],
        '#62B3C0': ["chemical",  'bitter','salty','medicinal','petroleum','skunky','rubber'],
        '#BF954E': ["pipe tobacco","tobacco"],
        '#B1724E': ["burnt",  'acrid','ashy','smoky','brown','roast','grain','malt'],
        '#A13743': ["pungent","pepper","brown spice",  'anise','nutmeg','cinnamon','clove'],
        '#BB7554': ["nutty",  'peanut','hazelnut','almond'],
        '#AE6237': ["cocoa",  'chocolate','dark chocolate'],
        '#CA4344': ["brown sugar",  'molasses','mapple syrup','caramelized','honey'      ,'caramel'],
        '#F7856A': ["vanilla","vanillin"],
        '#854959': ["black tea"],
        '#D3759B': ["floral",'chamomile','rose','jasmin',  'jasmine'],
}
default_color = 'black'
grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)
# grouped_color_func = GroupedColorFunc(color_to_words, default_color)

# st.text('Aroma / Flavorに使われる言葉')
# descriptions = pd.concat([df['aroma_flavor_str_agg']], ignore_index=True, axis=0).dropna()
# descriptions_unique = descriptions.map(lambda l: ",".join(list(set(l.split(",")))) )
# descriptions_list = ",".join(descriptions_unique).split(",")
# c = Counter(descriptions_list)
# d={t[0]: t[1] for t in c.most_common()}
# wordcloud = WordCloud(width=1920, height=1080, background_color=None, mode="RGBA", color_func=grouped_color_func).fit_words(d)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# st.pyplot(plt)


st.text('Acidityに使われる言葉')
descriptions = pd.concat([df['acidity_str_agg']], ignore_index=True, axis=0).dropna()
descriptions_unique = descriptions.map(lambda l: ",".join(list(set(l.split(",")))) )
descriptions_list = ",".join(descriptions_unique).split(",")
c = Counter(descriptions_list)
d={t[0]: t[1] for t in c.most_common()}
wordcloud = WordCloud(width=600, height=400, background_color='white', colormap="prism").fit_words(d)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)

st.text('Aroma / Flavorに使われる言葉')
descriptions = pd.concat([df['aroma_flavor_str_agg']], ignore_index=True, axis=0).dropna()
descriptions_unique = descriptions.map(lambda l: ",".join(list(set(l.split(",")))) )
descriptions_list = ",".join(descriptions_unique).split(",")
c = Counter(descriptions_list)
d={t[0]: t[1] for t in c.most_common()}
wordcloud = WordCloud(width=600, height=400, background_color='white', colormap="prism").fit_words(d)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)






    
st.text('全体的な印象の表現に使われる言葉')
descriptions = pd.concat([df['other_str_agg'], df['overall_str_agg'], df['characteristics_str_agg']], ignore_index=True, axis=0).dropna()
descriptions_unique = descriptions.map(lambda l: ",".join(list(set(l.split(",")))) )
descriptions_list = ",".join(descriptions_unique).split(",")
c = Counter(descriptions_list)
d={t[0]: t[1] for t in c.most_common()}
wordcloud = WordCloud(width=600, height=400, background_color='white', colormap="prism").fit_words(d)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)