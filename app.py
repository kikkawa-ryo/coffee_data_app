import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
import emoji


st.title(emoji.emojize('Coffee Data App:hot_beverage:'))
st.header("What's this app?")
url = "https://allianceforcoffeeexcellence.org/competition-auction-results/"
st.write("[Cup of Excellence](%s) というコーヒーの品評会からデータを収集しています。" % url)
st.write("streamlitのテストを兼ねて作成しました。")

# ダミーデータの作成
st.subheader('Sample Data')
df = pd.read_csv('sample.csv').sort_values(['year', 'country', 'rank_no'], ascending=[False, True, True]).reset_index(drop=True)
st.dataframe(df)

# wordcloud
from collections import Counter
from wordcloud import WordCloud
st.subheader("Word Cloud")
st.text('風味表現に使われる言葉')
descriptions = pd.concat([df['acidity_str_agg'], df['aroma_flavor_str_agg'], df['other_str_agg'], df['overall_str_agg'], df['characteristics_str_agg']], ignore_index=True, axis=0).dropna()
descriptions_list = ",".join(descriptions).split(",")
c = Counter(descriptions_list)
d={t[0]: t[1] for t in c.most_common()}
wordcloud = WordCloud(width=800, height=400, background_color='white').fit_words(d)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)


# 箱ひげ
st.subheader("Box Plot")
st.text('年ごとのスコアの分布')
chart = alt.Chart(df[['year', "score", "country"]]).mark_boxplot(extent='min-max').encode(
        x=alt.X('year:O'),
        y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100])),
    )
st.altair_chart(chart, theme="streamlit", use_container_width=True)


# 散布図
st.subheader("Scatter Plot")
st.text('スコアとオークション価格の散布図')
chart = alt.Chart(df[["score", "total_value", "year"]]).mark_circle(size=60).encode(
    x=alt.X('score:Q', scale=alt.Scale(domain=[80, 100])),
    y=alt.Y('total_value:Q', scale=alt.Scale(domain=[0, 250000])),
    color=alt.Color('year:Q', scale=alt.Scale(domain=[1999, 2025], scheme='viridis'))
).interactive()
st.altair_chart(chart, theme="streamlit", use_container_width=True)


# 時系列折れ線
st.subheader("Line Plot")
st.text('時系列折れ線')
res3 = df[["country", "year", "total_value"]].dropna().groupby(["country", "year"]).mean().reset_index()
st.line_chart(
    data=res3,
    x="year", y="total_value",
    color="country",
    width=1, height=None,
    # use_container_width=True
)

# st.header("Result-3")
# res3 = df[["country", "year", "total_value"]].dropna().groupby(["country", "year"]).mean().reset_index()
# plot = sns.heatmap(df.corr(), annot=True)
# st.pyplot(plot.get_figure())


