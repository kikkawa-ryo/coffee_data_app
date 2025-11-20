import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum

from utils.data_utils import query

_="""
全ページ共通の処理
"""
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