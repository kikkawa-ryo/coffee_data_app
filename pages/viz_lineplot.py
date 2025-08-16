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
# 時系列折れ線
st.subheader("Line Plot")
st.text('最大/平均/最小落札額の時系列グラフ')
agg = df.groupby(["year"]).agg({"high_bid":['mean', 'min', 'max']})
agg.columns = agg.columns.droplevel(0)
agg = agg.add_suffix("").reset_index()
line = (
    alt.Chart()
    .mark_line()
    .encode(
        x=alt.X('year:Q', scale=alt.Scale(domain=[1998, 2025])),
        y=alt.Y('high_bid:Q', scale=alt.Scale(domain=[0, 450]), title="high_bid"),
        color="metric",
    )
)
band = (
    alt.Chart()
    .mark_errorband(extent="ci")
    .encode(
        x=alt.X('year:Q', scale=alt.Scale(domain=[1998, 2025])),
        y=alt.Y('high_bid:Q', scale=alt.Scale(domain=[0, 450]), title="high_bid"),
        color="metric",
        )
)
chart = alt.layer(
    line,
    band,
    data=pd.melt(agg, id_vars=["year"], var_name="metric", value_name="high_bid")
)
st.altair_chart(
    chart,
    theme="streamlit",
    use_container_width=True
)

st.text('国別の最大/平均/最小落札額の時系列グラフ')
agg_avg = df[["country", "year", "high_bid"]].dropna().groupby(["country", "year"]).mean().reset_index()
agg_min = df[["country", "year", "high_bid"]].dropna().groupby(["country", "year"]).min().reset_index()
agg_max = df[["country", "year", "high_bid"]].dropna().groupby(["country", "year"]).max().reset_index()
avg_chart = alt.Chart(agg_avg).mark_line().encode(
    x=alt.X('year:Q', scale=alt.Scale(domain=[1998, 2025])),
    y=alt.Y('high_bid:Q', scale=alt.Scale(domain=[0, 50])).title("Avg. high_bid"),
    color=alt.Color('country')
).interactive()
min_chart = alt.Chart(agg_min).mark_line().encode(
    x=alt.X('year:Q', scale=alt.Scale(domain=[1998, 2025])),
    y=alt.Y('high_bid:Q', scale=alt.Scale(domain=[0, 20])).title("Min. high_bid"),
    color=alt.Color('country')
).interactive()
max_chart = alt.Chart(agg_max).mark_line().encode(
    x=alt.X('year:Q', scale=alt.Scale(domain=[1998, 2025])),
    y=alt.Y('high_bid:Q', scale=alt.Scale(domain=[0, 450])).title("Max. high_bid"),
    color=alt.Color('country')
).interactive()
chart = alt.VConcatChart(
        vconcat=(avg_chart, min_chart, max_chart)
    )
st.altair_chart(
    chart,
    theme="streamlit",
    use_container_width=True
)