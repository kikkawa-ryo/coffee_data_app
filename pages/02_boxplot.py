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
# 箱ひげ
st.subheader("Box Plot")
box1, box2 = st.columns(2)
with box1:
    st.text('年ごとのスコアの分布')
    chart = alt.Chart(df).mark_boxplot(extent='min-max').encode(
            x=alt.X('year:O'),
            y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100])),
        ).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with box2:
    st.text('国ごとの標高の分布')
    chart = alt.Chart(df).mark_boxplot(extent='min-max').encode(
            x=alt.X('country'),
            y=alt.Y('avg_altitude:Q', scale=alt.Scale(domain=[0, 3000])),
        ).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)