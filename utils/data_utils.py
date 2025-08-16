import streamlit as st

from google.oauth2 import service_account
from google.cloud import bigquery

from utils.utils import return_national_flag

@st.cache_resource
def query():
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
    # BigQueryからの取得
    df = client.query(sql).to_dataframe()
    # dataframeの加工
    df['country'] = df['country'].apply(lambda x: x.replace("-"," ").title()).apply(lambda x: x +return_national_flag(x))
    df = df.convert_dtypes()
    df[['score', 'high_bid', 'total_value', 'weight_lb', 'weight_kg', 'min_altitude', 'avg_altitude', 'max_altitude']] = df[['score', 'high_bid', 'total_value', 'weight_lb', 'weight_kg', 'min_altitude', 'avg_altitude', 'max_altitude']].astype(float)
    
    return df