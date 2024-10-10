import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum

from google.oauth2 import service_account
from google.cloud import bigquery

# サイドバー
with st.sidebar:
    st.page_link("app.py", label="ホーム", icon="🏠")
    st.page_link("pages/viz_scatterplot.py", label="scatterplot", icon="📈")
    st.page_link("pages/viz_lineplot.py", label="lineplot", icon="📈")
    st.page_link("pages/viz_barplot.py", label="barplot", icon="📊")
    st.page_link("pages/02_boxplot.py", label="boxplot", icon="📊")
    st.page_link("pages/01_wordcloud.py", label="wordcloud", icon="🍷")
    st.page_link("pages/gallery.py", label="gallery", icon="🖼")

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
        year desc, country
"""
df = client.query(sql).to_dataframe()
st.dataframe(df)

# 棒グラフ
# st.subheader("Bar Plot")
# st.text('年ごとのスコアの分布')
# chart = alt.Chart(df).mark_boxplot(extent='min-max').encode(
#         x=alt.X('year:O'),
#         y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100])),
#     ).interactive()
# st.altair_chart(chart, theme="streamlit", use_container_width=True)

# box1, box2 = st.columns(2)
# with box1:
#     st.text('年ごとのスコアの分布')
#     chart = alt.Chart(df).mark_boxplot(extent='min-max').encode(
#             x=alt.X('year:O'),
#             y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100])),
#         ).interactive()
#     st.altair_chart(chart, theme="streamlit", use_container_width=True)
# with box2:
#     st.text('国ごとの標高の分布')
#     chart = alt.Chart(df).mark_boxplot(extent='min-max').encode(
#             x=alt.X('country'),
#             y=alt.Y('avg_altitude:Q', scale=alt.Scale(domain=[0, 3000])),
#         ).interactive()
#     st.altair_chart(chart, theme="streamlit", use_container_width=True)