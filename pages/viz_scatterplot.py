import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum

from utils.data_utils import query

_="""
全ページ共通の処理
"""
# サイドバー
with st.sidebar:
    st.page_link("app.py", label="ホーム", icon="🏠")
    st.page_link("pages/viz_scatterplot.py", label="scatterplot", icon="📈")
    st.page_link("pages/viz_lineplot.py", label="lineplot", icon="📈")
    st.page_link("pages/viz_barplot.py", label="barplot", icon="📊")
    st.page_link("pages/02_boxplot.py", label="boxplot", icon="📊")
    st.page_link("pages/01_wordcloud.py", label="wordcloud", icon="🍷")
    st.page_link("pages/gallery.py", label="gallery", icon="🖼")
# データの取得
df = query()

_="""
メイン処理
"""
# 散布図
st.subheader("Scatter Plot")
st.text('スコアとオークション価格の散布図')
chart = alt.Chart(df).mark_circle(size=10).encode(
    x=alt.X('score:Q', scale=alt.Scale(domain=[80, 100])),
    y=alt.Y('high_bid:Q', scale=alt.Scale(domain=[0, 500])),
    color=alt.Color('year:Q', scale=alt.Scale(domain=[1998, 2025], scheme='turbo'))
).transform_filter(
    (alt.datum.award_category == "coe")
).interactive()
st.altair_chart(chart, theme="streamlit", use_container_width=True)

st.text('スコアとランクの散布図')
chart = alt.Chart(df).mark_circle(size=10).encode(
    x=alt.X('rank_no:Q', scale=alt.Scale(domain=[0, 50], reverse=True)),
    y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100])),
    color=alt.Color('year:Q', scale=alt.Scale(domain=[1998, 2025], scheme='turbo'))
).transform_filter(
    (alt.datum.award_category == "coe")
).interactive()
st.altair_chart(chart, theme="streamlit", use_container_width=True)

st.text('標高とスコアの散布図')
chart = alt.Chart(df).mark_circle(size=10).encode(
    x=alt.X('avg_altitude:Q', scale=alt.Scale(domain=[0, 3000])),
    y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100])),
).interactive()
st.altair_chart(chart, theme="streamlit", use_container_width=True)

chart = alt.Chart(df).mark_circle(size=10).encode(
    x=alt.X('avg_altitude:Q', scale=alt.Scale(domain=[0, 3000])),
    y=alt.Y('weight_kg:Q', scale=alt.Scale(domain=[0, 10000])),
).interactive()
st.altair_chart(chart, theme="streamlit", use_container_width=True)
