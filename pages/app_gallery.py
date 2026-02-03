import streamlit as st
import pandas as pd
from PIL import Image
import requests
import io

from google.oauth2 import service_account
from google.cloud import bigquery
from utils.utils import return_national_flag

st.set_page_config(
    page_title="Coffee Farm Gallery",
    page_icon="🖼",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .gallery-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(120deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .farm-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 4px solid #38ef7d;
    }
    .farm-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class="gallery-header">
    <h1>🖼 Coffee Farm Gallery</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        地理学と文化人類学で見る、コーヒー農園の世界
    </p>
</div>
""", unsafe_allow_html=True)

# イントロダクション
st.markdown("""
### 🌍 地理学 × 🎨 文化人類学

このページでは、Cup of Excellenceに入賞した農園の写真を通じて、
コーヒー生産地の**地理的多様性**と**文化的豊かさ**を体験できます。

- **地理学の視点**: 各農園の立地、標高、気候、土壌がコーヒーの個性を生み出します
- **文化人類学の視点**: 生産者の暮らし、伝統的な栽培方法、地域コミュニティが見えてきます

それぞれの写真には、生産者の物語と土地の記憶が刻まれています。
""")

st.markdown("---")

# BigQueryクライアント設定
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# クエリID（リフレッシュ用）の初期化
if 'query_id' not in st.session_state:
    st.session_state.query_id = 0

@st.cache_data(ttl=600)
def run_query(query, query_id):
    """BigQueryからデータを取得
    query_id: キャッシュを制御するための引数（値が変わると再実行される）
    """
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

# ギャラリーオプション
st.sidebar.header("ギャラリー設定")
num_farms = st.sidebar.slider("表示する農園数", min_value=5, max_value=30, value=15)

# リフレッシュボタン
if st.sidebar.button("🔄 新しい農園を表示"):
    st.session_state.query_id += 1
    # st.rerun() # 必要であれば

# クエリ実行
rows = run_query(f"""
    SELECT
        res.country,
        res.year,
        res.url,
        img.image_url,
        farm.farm_cws
    FROM
        `coffee-research.coffee_house.fct_results` res
    LEFT JOIN
        `coffee-research.coffee_house.dim_farm_images` img
    ON
        res.result_key = img.result_key
    LEFT JOIN
        `coffee-research.coffee_house.dim_farm_info` farm
    ON
        res.result_key = farm.result_key
    WHERE
        img.image_url IS NOT NULL
    ORDER BY
        RAND()
    LIMIT
        {num_farms}
""", st.session_state.query_id)

# 農園数表示
st.header(f"🌱 発見された農園: {len(rows)}件")

# ギャラリー表示
for idx, row in enumerate(rows, 1):
    try:
        country = row['country'].replace("-", " ").title()
        year = str(row['year'])
        image_url = row['image_url']
        farm_url = row['url']
        farm_cws = row['farm_cws'].title() if row['farm_cws'] else "不明"
        
        # 農園カード
        st.markdown(f"""
        <div class="farm-card">
            <h3>🏆 農園 #{idx}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 情報表示
        col_info, col_img = st.columns([1, 2])
        
        with col_info:
            st.markdown(f"""
            <div class="farm-info">
                <p><strong>🌍 国:</strong> {country} {return_national_flag(country)}</p>
                <p><strong>📅 年:</strong> {year}</p>
                <p><strong>🌱 農園/精製所:</strong> {farm_cws}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"[🔗 詳細ページを見る]({farm_url})")
        
        with col_img:
            # 画像読み込みと表示
            try:
                if image_url:
                    response = requests.get(image_url, timeout=5)
                    if response.status_code == 200:
                        img = Image.open(io.BytesIO(response.content))
                        st.image(img, use_container_width=True, caption=f"{country} - {year}")
                    else:
                        st.warning(f"画像をロードできませんでした (Status: {response.status_code})")
                else:
                    st.info("No Image Available")
            except Exception as img_error:
                st.warning(f"画像読み込みエラー: {str(img_error)}")
        
        if image_url:
            st.caption(f"📷 画像URL: {image_url}")
        st.divider()
        
    except Exception as e:
        # st.warning(f"農園 #{idx} のデータ処理中にエラーが発生しました: {str(e)}")
        # st.divider()
        pass

# まとめ
st.markdown("---")
st.header("🌏 コーヒーが教えてくれる世界の多様性")

st.write("""
これらの写真は、単なる農園の風景ではありません。それぞれが：

- **地理的な物語**: 山岳地帯、火山性土壌、熱帯雨林...場所ごとに異なる自然環境
- **文化的な記憶**: 世代を超えて受け継がれる栽培技術と伝統
- **経済的な希望**: 品質向上による生産者の生活改善と地域の発展
- **人間的なつながり**: 遠く離れた土地の生産者と消費者を繋ぐ架け橋

1杯のコーヒーの背後には、豊かな地理と文化の物語があります。
""")