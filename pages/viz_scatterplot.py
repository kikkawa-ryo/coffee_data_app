import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum

from google.oauth2 import service_account
from google.cloud import bigquery

from utils.utils import return_national_flag

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

if 'df' not in st.session_state:
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)
    sql = """
        SELECT
            *
        FROM
            `coffee-research`.`coffee_house`.`rpt_streamlit_sample_data`
        order by
            year desc, country, score desc
    """
    # dataframeの作成
    df = client.query(sql).to_dataframe()
    df['country'] = df['country'].apply(lambda x: x.replace("-"," ").title()).apply(lambda x: x +return_national_flag(x))
    df = df.convert_dtypes()
    df[['score', 'high_bid', 'total_value', 'weight_lb', 'weight_kg', 'min_altitude', 'avg_altitude', 'max_altitude']] = df[['score', 'high_bid', 'total_value', 'weight_lb', 'weight_kg', 'min_altitude', 'avg_altitude', 'max_altitude']].astype(float)
    # dataframeをセッションに保存
    st.session_state.df = df
df = st.session_state.df


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
