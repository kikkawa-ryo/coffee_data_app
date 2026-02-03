import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import numpy as np

from utils.data_utils import query

# ページ設定
st.title("💰 Economic Analysis: Coffee C Price & COE")
st.write("国際コーヒー市場の価格動向とCup of Excellence落札価格の経済的分析")

# データ読み込み
@st.cache_data
def load_coffee_price():
    """Coffee C priceデータの読み込み"""
    df = pd.read_csv('data/coffee_c_price_full.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    return df

@st.cache_data  
def load_coe_data():
    """COEデータの読み込み"""
    return query()

df_price = load_coffee_price()
df_coe = load_coe_data()

# サイドバーでフィルター設定
st.sidebar.header("フィルター設定")

# 年範囲選択
min_year = int(df_price['year'].min())
max_year = int(df_price['year'].max())
selected_years = st.sidebar.slider(
    "分析期間",
    min_value=min_year,
    max_value=max_year,
    value=(2015, max_year)
)

# データフィルタリング
df_price_filtered = df_price[
    (df_price['year'] >= selected_years[0]) & 
    (df_price['year'] <= selected_years[1])
]

st.markdown("---")

# セクション1: Coffee C Price 概要
st.header("📈 Coffee C Price トレンド")
st.write("""
Coffee C Priceは、ニューヨーク商品取引所（ICE）で取引されるアラビカコーヒーの先物価格です。
世界中のコーヒー取引の指標となり、生産者・消費者双方に大きな影響を与えます。
""")

# メトリクス表示
col1, col2, col3, col4 = st.columns(4)

with col1:
    current_price = df_price_filtered['price_usd_lb'].iloc[-1]
    st.metric("現在価格", f"${current_price:.2f}/lb")

with col2:
    max_price = df_price_filtered['price_usd_lb'].max()
    max_date = df_price_filtered.loc[df_price_filtered['price_usd_lb'].idxmax(), 'Date']
    st.metric(
        "期間内最高価格", 
        f"${max_price:.2f}/lb",
        delta=f"{max_date.strftime('%Y/%m/%d')}"
    )

with col3:
    min_price = df_price_filtered['price_usd_lb'].min()
    min_date = df_price_filtered.loc[df_price_filtered['price_usd_lb'].idxmin(), 'Date']
    st.metric(
        "期間内最低価格",
        f"${min_price:.2f}/lb",
        delta=f"{min_date.strftime('%Y/%m/%d')}"
    )

with col4:
    volatility = df_price_filtered['price_usd_lb'].std()
    st.metric("価格変動性", f"${volatility:.2f}")

# 価格推移グラフ
st.subheader("💹 価格推移")

# 移動平均の計算
df_price_filtered_copy = df_price_filtered.copy()
df_price_filtered_copy['MA_30'] = df_price_filtered_copy['price_usd_lb'].rolling(window=30).mean()
df_price_filtered_copy['MA_90'] = df_price_filtered_copy['price_usd_lb'].rolling(window=90).mean()

# メインの価格チャート
base = alt.Chart(df_price_filtered_copy).encode(
    x=alt.X('Date:T', title='日付')
)

line_price = base.mark_line(color='#6B4423', strokeWidth=2).encode(
    y=alt.Y('price_usd_lb:Q', title='価格 ($/lb)'),
    tooltip=['Date:T', alt.Tooltip('price_usd_lb:Q', format='.2f', title='価格')]
)

line_ma30 = base.mark_line(color='#FFA500', strokeWidth=1.5, strokeDash=[5, 5]).encode(
    y='MA_30:Q',
    tooltip=['Date:T', alt.Tooltip('MA_30:Q', format='.2f', title='30日移動平均')]
)

line_ma90 = base.mark_line(color='#FF6347', strokeWidth=1.5, strokeDash=[3, 3]).encode(
    y='MA_90:Q',
    tooltip=['Date:T', alt.Tooltip('MA_90:Q', format='.2f', title='90日移動平均')]
)

price_chart = (line_price + line_ma30 + line_ma90).properties(
    height=400,
    title='Coffee C Price 推移（30日・90日移動平均含む）'
).interactive()

st.altair_chart(price_chart, use_container_width=True)

st.markdown("---")

# セクション2: COEとの比較
st.header("🏆 COE落札価格との比較")
st.write("""
Cup of Excellenceで落札される高品質コーヒーの価格と、
一般的なコーヒー市場価格（Coffee C Price）を比較します。
""")

# COEデータの年次集計
if 'year' in df_coe.columns and 'high_bid' in df_coe.columns:
    df_coe_yearly = df_coe.groupby('year').agg({
        'high_bid': ['mean', 'max', 'min', 'count']
    }).reset_index()
    df_coe_yearly.columns = ['year', 'avg_bid', 'max_bid', 'min_bid', 'count']
    
    # Coffee C Priceの年次平均
    df_price_yearly = df_price.groupby('year').agg({
        'price_usd_lb': 'mean'
    }).reset_index()
    df_price_yearly.columns = ['year', 'avg_price']
    
    # マージ
    df_comparison = pd.merge(df_coe_yearly, df_price_yearly, on='year', how='inner')
    df_comparison = df_comparison[
        (df_comparison['year'] >= selected_years[0]) &
        (df_comparison['year'] <= selected_years[1])
    ]
    
    # プレミアム計算
    df_comparison['premium_ratio'] = (df_comparison['avg_bid'] / df_comparison['avg_price']) - 1
    
    # 比較グラフ
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 年次平均価格比較")
        
        # データを縦持ちに変換
        df_plot = pd.DataFrame({
            'year': list(df_comparison['year']) + list(df_comparison['year']),
            'price': list(df_comparison['avg_price']) + list(df_comparison['avg_bid']),
            'type': ['Coffee C Price'] * len(df_comparison) + ['COE平均落札価格'] * len(df_comparison)
        })
        
        comparison_chart = alt.Chart(df_plot).mark_line(point=True).encode(
            x=alt.X('year:O', title='年'),
            y=alt.Y('price:Q', title='価格 ($/lb)'),
            color=alt.Color('type:N', 
                          scale=alt.Scale(
                              domain=['Coffee C Price', 'COE平均落札価格'],
                              range=['#6B4423', '#C68642']
                          ),
                          legend=alt.Legend(title='価格タイプ')),
            tooltip=['year:O', 'type:N', alt.Tooltip('price:Q', format='.2f')]
        ).properties(height=350)
        
        st.altair_chart(comparison_chart, use_container_width=True)
    
    with col_right:
        st.subheader("💎 プレミアム率推移")
        st.write("COE落札価格 ÷ Coffee C Price - 1")
        
        premium_chart = alt.Chart(df_comparison).mark_bar(color='#FFD700').encode(
            x=alt.X('year:O', title='年'),
            y=alt.Y('premium_ratio:Q', 
                   title='プレミアム率',
                   axis=alt.Axis(format='%')),
            tooltip=[
                'year:O', 
                alt.Tooltip('premium_ratio:Q', format='.1%', title='プレミアム率'),
                alt.Tooltip('avg_bid:Q', format='.2f', title='COE平均'),
                alt.Tooltip('avg_price:Q', format='.2f', title='C Price平均')
            ]
        ).properties(height=350)
        
        st.altair_chart(premium_chart, use_container_width=True)
    
    # インサイト
    st.subheader("🔍 インサイト")
    
    avg_premium = df_comparison['premium_ratio'].mean()
    max_premium_year = df_comparison.loc[df_comparison['premium_ratio'].idxmax(), 'year']
    max_premium_value = df_comparison['premium_ratio'].max()
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        st.info(f"""
        **平均プレミアム率**  
        COE落札価格は一般市場価格の  
        **{(avg_premium + 1):.1f}倍**  
        （{avg_premium:.1%}のプレミアム）
        """)
    
    with insight_col2:
        st.success(f"""
        **最高プレミアム年**  
        {int(max_premium_year)}年  
        **{(max_premium_value + 1):.1f}倍**  
        の価格差を記録
        """)
    
    with insight_col3:
        recent_premium = df_comparison['premium_ratio'].iloc[-1] if len(df_comparison) > 0 else 0
        st.warning(f"""
        **直近のプレミアム**  
        {(recent_premium + 1):.1f}倍  
        高品質コーヒーの価値は  
        依然として高い
        """)

else:
    st.info("COEデータに必要なカラム（year, high_bid）が見つかりません")

st.markdown("---")

# セクション3: 経済的考察
st.header("💡 経済的考察")

st.write("""
### コーヒー市場の特徴

1. **価格変動性**: Coffee C Priceは気候変動、政治情勢、為替レート、需給バランスなど、
   多様な要因によって大きく変動します。

2. **品質プレミアム**: Cup of Excellenceのような高品質コーヒーは、一般市場価格の
   数倍から数十倍で取引され、生産者に大きなインセンティブを提供します。

3. **バリューチェーン**: 生産者から消費者まで、コーヒーは複雑なグローバル流通を経て
   届けられます。適正な価格形成が持続可能性の鍵となります。

4. **市場トレンド**: 近年、スペシャルティコーヒーへの需要が高まり、
   品質重視の市場が拡大しています。
""")

# データテーブル表示
with st.expander("📋 詳細データを見る"):
    st.subheader("Coffee C Price データ（最近30日）")
    st.dataframe(df_price_filtered.tail(30)[['Date', 'Open', 'High', 'Low', 'Close', 'price_usd_lb']], use_container_width=True)
    
    if 'year' in df_coe.columns:
        st.subheader("COE年次統計")
        st.dataframe(df_comparison, use_container_width=True)
