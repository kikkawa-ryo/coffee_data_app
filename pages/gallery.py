import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests
import io


from google.oauth2 import service_account
from google.cloud import bigquery

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

rows = run_query(
    """
    SELECT
        image_url
    FROM
        `coffee-research.coffee_house.dim_farm_images`
    ORDER BY 
        rand()
    LIMIT
        10
    """
)

# Print results.]
for row in rows:
    response = requests.get(row['image_url'])
    st.write("✍️ " + row['image_url'])
    try:
        img = Image.open(io.BytesIO(response.content))
        st.image(img)
    except Exception as e:
        print(e)