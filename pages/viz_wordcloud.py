import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum


from utils.data_utils import query

_="""
全ページ共通の処理
"""
# データの取得
df = query()

_="""
メイン処理
"""
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




tab1, tab2, tab3 = st.tabs(["🍋 Acidity", "💐 Aroma / Flavor", "☕️ Overall"])

with tab1:
    tab1.subheader("Acidityに使われる言葉")
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

with tab2:
    tab2.subheader('Aroma / Flavorに使われる言葉')
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
    
with tab3:
    st.subheader('全体的な印象の表現に使われる言葉')
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
    

# import folium
# from streamlit_folium import st_folium
# from geopy.geocoders import Nominatim

# geolocator = Nominatim(user_agent="test") #名前はなんでもOK
# # df
# data = df[["country", "aroma_flavor_str_agg"]].dropna()
# data["aroma_flavor_str_agg"] = data["aroma_flavor_str_agg"].map(lambda x: set(x.split(",")))

# # 単語リストを展開して頻度を集計
# def aggregate_word_frequencies(df):
#     # words列を展開
#     data_exploded = data.explode("aroma_flavor_str_agg")
#     # 国ごと、単語ごとに頻度を集計
#     freq_df = data_exploded.groupby(["country", "aroma_flavor_str_agg"]).size().reset_index(name="frequency")
#     return freq_df

# # 集計実行
# data_agg = aggregate_word_frequencies(data).sort_values(['country', 'frequency'], ascending=[True, False])
# data_agg["aroma_flavor_agg"] = 1
# # data_agg

# new_df = pd.DataFrame({"country": list(set(data_agg['country']))})
# new_df["address"] = new_df.apply(lambda x : geolocator.geocode(x.country[:-1]).address, axis=1)
# new_df["latitude"] = new_df.apply(lambda x : geolocator.geocode(x.country[:-1]).latitude, axis=1)
# new_df["longitude"] = new_df.apply(lambda x : geolocator.geocode(x.country[:-1]).longitude, axis=1)
# # for c in new_df['country']:
# #     location = geolocator.geocode(c[:-1])
# #     new_df["address"] = location.address
# #     new_df["latitude"] = location.latitude
# #     new_df["longitude"] = location.longitude
# new_df
# # countries = 


# st.write(location.address)       #住所
# st.write(location.latitude)      #緯度
# st.write(location.longitude)     #経度
# # df
# m = folium.Map(location=[20, 0], zoom_start=2)
# for country, lat, lon, values in data.itertuples(index=False):
#     labels = ['Category1', 'Category2', 'Category3']
#     img_str = create_pie_chart(values, labels)
#     icon = folium.features.CustomIcon(
#         icon_image=f'data:image/png;base64,{img_str}',
#         icon_size=(50, 50)
#     )
#     folium.Marker(
#         location=[lat, lon],
#         icon=icon
#     ).add_to(m)
# st_folium(m, width=700, height=500)