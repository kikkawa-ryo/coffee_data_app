import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests
import io

from google.oauth2 import service_account
from google.cloud import bigquery

from utils.utils import return_national_flag

# サイドバー
# with st.sidebar:
#     st.page_link("app.py", label="ホーム", icon="🏠")
#     st.page_link("pages/viz_scatterplot.py", label="scatterplot", icon="📈")
#     st.page_link("pages/viz_lineplot.py", label="lineplot", icon="📈")
#     st.page_link("pages/viz_barplot.py", label="barplot", icon="📊")
#     st.page_link("pages/02_boxplot.py", label="boxplot", icon="📊")
#     st.page_link("pages/01_wordcloud.py", label="wordcloud", icon="🍷")
#     st.page_link("pages/gallery.py", label="gallery", icon="🖼")

# body
st.title("Coffee Farm Gallery")
st.header("What's this page?")
st.write("このページでは、Cup of Excellenceに出品し入賞した農家さんがアップしている写真をランダムに見ることができます。")

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# @st.cache_data(ttl=200)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

# 画像表示コンテナ
with st.container(height=700):
    rows = run_query(
        """
        select
            res.country,
            res.year,
            res.url,
            img.image_url,
            farm.farm_cws,
        from
            `coffee-research.coffee_house.fct_results` res
        left join
            `coffee-research.coffee_house.dim_farm_images` img
        on
            res.result_key = img.result_key
        left join
            `coffee-research.coffee_house.dim_farm_info` farm
        on
            res.result_key = farm.result_key
        where
            img.image_url is not null
        order by
            RAND()
        limit
            15
        """
    )

    # Print results.]
    for row in rows:
        try:
            country = row['country'].replace("-"," ").title()
            year = str(row['year'])
            image_url = row['image_url']
            farm_url = row['url']
            farm_cws = row['farm_cws'].title()
            
            st.write("Country: " + country + return_national_flag(country))
            st.write("Year: " + year)
            st.write("Farm | Coffee Washing Station: " + farm_cws)
            st.write("Farm URL: " + farm_url)
            response = requests.get(image_url)
        
            img = Image.open(io.BytesIO(response.content))
            st.image(img)
        except Exception as e:
            print(e)
        st.write("✍️ " + image_url)
        st.divider()