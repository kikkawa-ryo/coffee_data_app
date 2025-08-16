import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum
import emoji

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
st.title(emoji.emojize('Coffee Data App:hot_beverage:'))
st.header("What's this app?")
url = "https://allianceforcoffeeexcellence.org/competition-auction-results/"
main_sentence = """
[Cup of Excellence](%s) というコーヒーの品評会から収集したデータを使い、様々なデータ可視化をおこなっています。\n
""" % url
st.write(main_sentence)
with st.expander(label="魅力をまとめたスライドは👇", expanded=True):
    components.iframe("https://docs.google.com/presentation/d/e/2PACX-1vSlqWlnZ1adWSqcY-LGucbssCrCF2Vfs4ZCEM0iQ0mtq0gw13YmkueR8AAAm52BkkRyf5Vf3tfAKzuV/embed?start=false&loop=false&delayms=3000", height=480)
with st.expander(label="データはコチラ"):
    st.subheader('Sample Data')
    st.dataframe(df)


# 国別レコード数
st.header("国別出品数")
st.write("Cup of Excelenceでこれまでに入賞した国別のfarm数")

bars = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        alt.X(
            "country",
            sort='ascending',
        ),
        alt.Y(
            "count()",
        )
    )
    .interactive()
)
st.altair_chart(
    bars,
    theme=None,
    use_container_width=True
)


