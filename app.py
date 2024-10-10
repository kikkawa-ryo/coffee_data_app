import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum
import emoji

# サイドバー
with st.sidebar:
    st.page_link("app.py", label="ホーム", icon="🏠")
    st.page_link("pages/viz_scatterplot.py", label="scatterplot", icon="📈")
    st.page_link("pages/viz_lineplot.py", label="lineplot", icon="📈")
    st.page_link("pages/viz_barplot.py", label="barplot", icon="📊")
    st.page_link("pages/02_boxplot.py", label="boxplot", icon="📊")
    st.page_link("pages/01_wordcloud.py", label="wordcloud", icon="🍷")
    st.page_link("pages/gallery.py", label="gallery", icon="🖼")

st.title(emoji.emojize('Coffee Data App:hot_beverage:'))
st.header("What's this app?")
url = "https://allianceforcoffeeexcellence.org/competition-auction-results/"
st.write("[Cup of Excellence](%s) というコーヒーの品評会からデータを収集しています。" % url)
# st.write("streamlitの勉強を兼ねて作成しました。")

# サンプルデータの作成
st.subheader('Sample Data')
df = pd.read_csv('data/sample.csv').sort_values(['year', 'country', 'rank_no'], ascending=[False, True, True]).reset_index(drop=True)
# st.session_state['df'] = pd.read_csv('sample.csv').sort_values(['year', 'country', 'rank_no'], ascending=[False, True, True]).reset_index(drop=True)
# st.dataframe(st.session_state['df'])
st.dataframe(df)





