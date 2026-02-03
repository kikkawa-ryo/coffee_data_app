import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum
import emoji

from utils.data_utils import query
    
_="""
ENDPOINTでの処理
"""
top = st.Page(
    page="pages/top.py", title="Home", icon="🏠", default=True)
economic = st.Page(
    page="pages/economic_coffee_price.py", title="Economic Analysis", icon="💰")
stats = st.Page(
    page="pages/viz_stats.py", title="Cup of Excellence Stats", icon="📊")
gallery = st.Page(
    page="pages/app_gallery.py", title="Coffee Farm Gallery", icon="🖼")
flight = st.Page(
    page="pages/app_coffee_flight.py", title="Coffee Flight Map", icon="✈️")
flavor = st.Page(
    page="pages/viz_wordcloud.py", title="Flavor World", icon="🍷")


pg = st.navigation(
    [top, economic, stats, flavor, gallery, flight]
    )
pg.run()
# with st.sidebar:
#     st.page_link("app.py", label="！ホーム", icon="🏠")
#     st.page_link("pages/viz_scatterplot.py", label="scatterplot", icon="📈")
#     st.page_link("pages/viz_lineplot.py", label="lineplot", icon="📈")
#     st.page_link("pages/viz_barplot.py", label="barplot", icon="📊")
#     st.page_link("pages/02_boxplot.py", label="boxplot", icon="📊")
#     st.page_link("pages/01_wordcloud.py", label="wordcloud", icon="🍷")
#     st.page_link("pages/gallery.py", label="gallery", icon="🖼")
