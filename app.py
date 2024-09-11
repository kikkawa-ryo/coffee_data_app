import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum
import emoji


st.title(emoji.emojize('Coffee Data App:hot_beverage:'))
st.header("What's this app?")
url = "https://allianceforcoffeeexcellence.org/competition-auction-results/"
st.write("[Cup of Excellence](%s) というコーヒーの品評会からデータを収集しています。" % url)
st.write("streamlitの勉強を兼ねて作成しました。")

# サンプルデータの作成
st.subheader('Sample Data')
df = pd.read_csv('sample.csv').sort_values(['year', 'country', 'rank_no'], ascending=[False, True, True]).reset_index(drop=True)
# st.session_state['df'] = pd.read_csv('sample.csv').sort_values(['year', 'country', 'rank_no'], ascending=[False, True, True]).reset_index(drop=True)
# st.dataframe(st.session_state['df'])



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
