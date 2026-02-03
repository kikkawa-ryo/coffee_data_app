import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt
import emoji

from utils.data_utils import query

# ページ設定
st.set_page_config(
    page_title="Coffee Data Explorer",
    page_icon="☕",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(120deg, #6B4423 0%, #C68642 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .category-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #DDD;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        background: white;
    }
    .category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-color: #C68642;
    }
    .fun-fact {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    .stat-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #C68642;
    }
</style>
""", unsafe_allow_html=True)

# データの取得
df = query()

# ヒーローセクション
st.markdown("""
<div class="main-header">
    <h1>☕ Coffee: A Lens to Understand Our Colorful World</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        一杯のコーヒーは、世界を知るための「レンズ」です。<br>
        経済、地理、化学、人間、文化...<br>
        世界を映し出す魅力的なレンズです。
    </p>
</div>
""", unsafe_allow_html=True)

# 学問マップセクション
st.header("🌟 コーヒーから見える世界の多様性")
st.write("""
コーヒーを深く知ることは、世界を多面的に理解することに繋がります。
産地の標高が100m変わるだけで、市場価格が1セント動くだけで、私たちのカップの中の物語は変化します。
ここでは、いくつかの側面からコーヒーという宇宙を探索します。
""")

# 6つのカテゴリカード
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="category-card">
        <h2>🌍</h2>
        <h3>地理学</h3>
        <p>コーヒーベルト、標高、気候、土壌が生み出す多様性</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="category-card">
        <h2>💰</h2>
        <h3>経済学</h3>
        <p>国際商品市場、価格変動、グローバルなバリューチェーン</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="category-card">
        <h2>🧪</h2>
        <h3>化学</h3>
        <p>フレーバー成分、ロースト反応、テロワールの科学</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="category-card">
        <h2>📊</h2>
        <h3>統計学</h3>
        <p>品質スコア分布、時系列分析、多変量解析</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="category-card">
        <h2>🌱</h2>
        <h3>農学</h3>
        <p>品種の多様性、栽培技術、サステナビリティ</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="category-card">
        <h2>🎨</h2>
        <h3>文化人類学</h3>
        <p>地域のコーヒー文化、儀式、社会的役割</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Fun Factsセクション
st.header("🎯 データで見る驚きのコーヒーワールド")

# Coffee C priceデータ読み込み
@st.cache_data
def load_coffee_price():
    df_price = pd.read_csv('data/coffee_c_price_full.csv')
    df_price['Date'] = pd.to_datetime(df_price['Date'])
    return df_price

df_price = load_coffee_price()

# フレーバーデータ読み込み
@st.cache_data
def load_flavor_data():
    return pd.read_csv('data/flavor_wheel_lexicon.csv')

df_flavor = load_flavor_data()

# Fun Facts表示
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="fun-fact">
        <h3>📈 価格の旅</h3>
        <p>過去26年間で、コーヒー価格は</p>
        <h2>${df_price['price_usd_lb'].min():.2f} → ${df_price['price_usd_lb'].max():.2f}/lb</h2>
        <p>なんと<strong>{((df_price['price_usd_lb'].max() / df_price['price_usd_lb'].min() - 1) * 100):.0f}%</strong>も変動しています！</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="fun-fact">
        <h3>🎨 フレーバーの宇宙</h3>
        <p>コーヒーが持つフレーバーの種類は</p>
        <h2>{len(df_flavor)}種類以上！</h2>
        <p>Fruity, Floral, Nutty, Spices...<br>無限の味わいが広がります</p>
    </div>
    """, unsafe_allow_html=True)

# COEデータの統計
col3, col4 = st.columns(2)

with col3:
    countries = df['country'].nunique()
    st.markdown(f"""
    <div class="fun-fact">
        <h3>🌍 世界を繋ぐ</h3>
        <p>Cup of Excellenceは</p>
        <h2>{countries}カ国</h2>
        <p>から優れたコーヒーを発掘<br>世界中の生産者と消費者を繋いでいます</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if 'max_altitude' in df.columns:
        max_alt = df['max_altitude'].max()
        st.markdown(f"""
        <div class="fun-fact">
            <h3>⛰️ 標高の極み</h3>
            <p>最も高い場所で栽培されたコーヒーは</p>
            <h2>{max_alt:,.0f}m</h2>
            <p>標高が高いほど、豊かで複雑な<br>フレーバーが生まれます</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="fun-fact">
            <h3>🏆 品質へのこだわり</h3>
            <p>Cup of Excellenceの審査は</p>
            <h2>超厳格！</h2>
            <p>世界中の専門家が<br>ブラインドテイスティングで評価</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ミニビジュアライゼーション
st.header("📊 データで見るコーヒーの世界")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("🌍 国別の入賞数")
    # 国別カウント
    country_chart = (
        alt.Chart(df.head(500))  # パフォーマンスのため制限
        .mark_bar()
        .encode(
            x=alt.X('count()', title='入賞数'),
            y=alt.Y('country:N', sort='-x', title='国'),
            color=alt.value('#C68642'),
            tooltip=['country', 'count()']
        )
        .properties(height=400)
    )
    st.altair_chart(country_chart, use_container_width=True)

with viz_col2:
    st.subheader("📈 Coffee C Price 推移")
    # 最近5年間の価格推移
    recent_price = df_price[df_price['Date'] >= '2020-01-01']
    price_chart = (
        alt.Chart(recent_price)
        .mark_line(color='#6B4423', strokeWidth=2)
        .encode(
            x=alt.X('Date:T', title='日付'),
            y=alt.Y('price_usd_lb:Q', title='価格 ($/lb)'),
            tooltip=['Date:T', 'price_usd_lb:Q']
        )
        .properties(height=400)
    )
    st.altair_chart(price_chart, use_container_width=True)

st.markdown("---")

# 統計サマリー
st.header("📈 COE データ統計サマリー")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown(f"""
    <div class="stat-box">
        <h3>{len(df):,}</h3>
        <p>総入賞数</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown(f"""
    <div class="stat-box">
        <h3>{df['country'].nunique()}</h3>
        <p>参加国数</p>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    if 'score' in df.columns:
        avg_score = df['score'].mean()
        st.markdown(f"""
        <div class="stat-box">
            <h3>{avg_score:.1f}</h3>
            <p>平均スコア</p>
        </div>
        """, unsafe_allow_html=True)

with stat_col4:
    if 'year' in df.columns:
        years = df['year'].max() - df['year'].min()
        st.markdown(f"""
        <div class="stat-box">
            <h3>{years}年</h3>
            <p>データ期間</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# データについて
st.header("📚 データについて")
url = "https://allianceforcoffeeexcellence.org/competition-auction-results/"
st.write(f"""
このアプリケーションは、[Cup of Excellence]({url})という世界的なコーヒー品評会から収集したデータと、
国際コーヒー市場の価格データ（Coffee C Price）を使用しています。

**Cup of Excellence**は、生産国ごとに開催される権威あるコーヒーコンペティションで、
厳格な審査を通過した最高品質のコーヒーのみが入賞します。このデータを通じて、
コーヒーの品質、産地、価格、フレーバーなど、多角的な分析が可能になります。

さあ、サイドバーから興味のあるページを選んで、コーヒーの世界を探検してみましょう！
""")

# データサンプル表示
with st.expander("📊 データサンプルを見る"):
    st.dataframe(df.head(100), use_container_width=True)