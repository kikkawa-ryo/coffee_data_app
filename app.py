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
st.dataframe(df)


# wordcloud
from collections import Counter
from wordcloud import WordCloud
st.subheader("Word Cloud")
st.text('風味表現に使われる言葉')
descriptions = pd.concat([df['acidity_str_agg'], df['aroma_flavor_str_agg'], df['other_str_agg'], df['overall_str_agg'], df['characteristics_str_agg']], ignore_index=True, axis=0).dropna()
descriptions_unique = descriptions.map(lambda l: ",".join(list(set(l.split(",")))) )
descriptions_list = ",".join(descriptions_unique).split(",")
c = Counter(descriptions_list)
d={t[0]: t[1] for t in c.most_common()}
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap="prism").fit_words(d)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)


# 箱ひげ
st.subheader("Box Plot")
st.text('年ごとのスコアの分布')
chart = alt.Chart(df).mark_boxplot(extent='min-max').encode(
        x=alt.X('year:O'),
        y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100])),
    ).interactive()
st.altair_chart(chart, theme="streamlit", use_container_width=True)


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


# 散布図
st.subheader("Scatter Plot")
st.text('スコアとランクの散布図')
chart = alt.Chart(df).mark_circle(size=10).encode(
    x=alt.X('rank_no:Q', scale=alt.Scale(domain=[0, 50], reverse=True)),
    y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100])),
    color=alt.Color('year:Q', scale=alt.Scale(domain=[1998, 2025], scheme='turbo'))
).transform_filter(
    (alt.datum.award_category == "coe")
).interactive()
st.altair_chart(chart, theme="streamlit", use_container_width=True)


# 時系列折れ線
st.subheader("Line Plot")
st.text('時系列折れ線')
agg = df.groupby(["year"]).agg({"high_bid":['mean', 'min', 'max']})
agg.columns = agg.columns.droplevel(0)
# agg = agg.add_suffix("_high_bid").reset_index()
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


# 時系列折れ線
st.subheader("Line Plot")
st.text('時系列折れ線')
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
