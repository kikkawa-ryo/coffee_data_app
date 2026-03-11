import streamlit as st
import pandas as pd

from google.oauth2 import service_account
from google.cloud import bigquery
from utils.utils import return_national_flag # このimportはローカルに必要

@st.cache_data
def query():
    """
    環境に応じたシークレットをロードし、BigQueryに接続してデータを取得・加工する。
    関数全体がキャッシュされるため、シークレットのロードとクライアント作成は一度しか実行されない。
    """

    # APIクライアントを作成
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
        
    client = bigquery.Client(credentials=credentials)
    
    # SQLの実行
    sql = """
        SELECT
            *
        FROM
            `coffee-research`.`coffee_house`.`t_lots`
        order by
            year desc, country_name, score desc
    """
    df = client.query(sql).to_dataframe()
    
    # DataFrameの加工
    # 古い rpt テーブルの構造に合わせるためリネーム
    rename_dict = {
        'country_name': 'country',
        'altitude_min': 'min_altitude',
        'altitude_avg': 'avg_altitude',
        'altitude_max': 'max_altitude'
    }
    df = df.rename(columns=rename_dict)
    
    # 欠損値等を埋めつつ文字列クレンジング、フラグ付与
    if 'country' in df.columns:
        df['country'] = df['country'].fillna("").apply(lambda x: x.replace("-"," ").title() if pd.notnull(x) else "")
        # emoji_flagがあればそれを使う、なければ自前関数
        if 'emoji_flag' in df.columns:
            df['country'] = df.apply(lambda row: row['country'] + (" " + row['emoji_flag'] if row['emoji_flag'] and pd.notnull(row['emoji_flag']) else return_national_flag(row['country'])), axis=1)
        else:
            df['country'] = df['country'].apply(lambda x: x + return_national_flag(x) if x else x)

    df = df.convert_dtypes()
    
    numeric_cols = ['score', 'high_bid', 'total_value', 'weight_lb', 'weight_kg', 'min_altitude', 'avg_altitude', 'max_altitude']
    existing_numeric_cols = [c for c in numeric_cols if c in df.columns]
    if existing_numeric_cols:
        df[existing_numeric_cols] = df[existing_numeric_cols].astype(float)
    
    return df