import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum
import emoji

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
st.title(emoji.emojize('Coffee Data App:hot_beverage:'))
st.header("What's this app?")
url = "https://allianceforcoffeeexcellence.org/competition-auction-results/"
st.write("[Cup of Excellence](%s) というコーヒーの品評会からデータを収集しています。" % url)

# サンプルデータの作成
st.subheader('Sample Data')
# st.session_state['df'] = pd.read_csv('sample.csv').sort_values(['year', 'country', 'rank_no'], ascending=[False, True, True]).reset_index(drop=True)
# st.dataframe(st.session_state['df'])
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


