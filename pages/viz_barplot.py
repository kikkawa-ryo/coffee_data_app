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
# 棒グラフ
st.subheader("Bar Plot")
st.text('')


h1 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        alt.X(
            "high_bid:Q",
            bin=alt.Bin(step=5, extent=[0, 500]),
            # bin=True,
            axis=alt.Axis(
                title="落札価格の分布"
            ),
        ),
        alt.Y(
            "count()",
        ),
    )
    .interactive()
)
st.altair_chart(
    h1,
    theme="streamlit",
    use_container_width=True,
)



histgram = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        alt.X(
            "score:Q",
            bin=alt.Bin(step=0.5, extent=[70, 100]),
            # bin=True,
            axis=alt.Axis(
                title="落札価格の分布"
            ),
        ),
        alt.Y(
            "count()",
        ),
    )
    .interactive()
)
st.altair_chart(
    histgram,
    theme="streamlit",
    use_container_width=True,
)
