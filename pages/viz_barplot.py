import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum

from google.oauth2 import service_account
from google.cloud import bigquery

from utils.utils import return_national_flag

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
        year desc, country, score desc
"""
df = client.query(sql).to_dataframe()
st.dataframe(df)
df['country'] = df['country'].apply(lambda x: x.replace("-"," ").title()).apply(lambda x: return_national_flag(x) + x)
df = df.convert_dtypes()
df[['score', 'high_bid', 'total_value', 'weight_lb', 'weight_kg', 'min_altitude', 'avg_altitude', 'max_altitude']] = df[['score', 'high_bid', 'total_value', 'weight_lb', 'weight_kg', 'min_altitude', 'avg_altitude', 'max_altitude']].astype(float)

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
