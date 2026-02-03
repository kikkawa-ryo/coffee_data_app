import streamlit as st
import pandas as pd
import altair as alt

from utils.data_utils import query

st.set_page_config(
    page_title="Statistics - Coffee Data",
    page_icon="📊",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .stats-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# データ取得
df = query()

# ヘッダー
st.markdown("""
<div class="stats-header">
    <h1>📊 統計学で紐解くコーヒーの世界</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        データが語る品質、価格、そして時間の物語
    </p>
</div>
""", unsafe_allow_html=True)

# イントロダクション
st.markdown("""
### 統計学とコーヒー

統計学は、膨大なデータから意味のあるパターンを抽出し、未来を予測する学問です。
Cup of Excellenceのデータを統計的に分析することで、コーヒーの品質を決める要因や、
市場価値の変遷を理解できます。
""")

st.markdown("---")

# セクション1: 基本統計量
st.header("📈 データ概要")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{len(df):,}</h3>
        <p>総サンプル数</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if 'score' in df.columns:
        avg_score = df['score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{avg_score:.2f}</h3>
            <p>平均スコア</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if 'high_bid' in df.columns:
        avg_bid = df['high_bid'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>${avg_bid:.2f}</h3>
            <p>平均落札価格</p>
        </div>
        """, unsafe_allow_html=True)

with col4:
    years_span = df['year'].max() - df['year'].min() if 'year' in df.columns else 0
    st.markdown(f"""
    <div class="metric-card">
        <h3>{years_span}年</h3>
        <p>データ期間</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# セクション2: 時系列分析
st.header("📉 時系列分析：落札価格の推移")
st.write("時間とともに変化する落札価格のパターンを探る")

if 'year' in df.columns and 'high_bid' in df.columns and not df.empty:
    # 年次集計
    agg = df.groupby(["year"]).agg({"high_bid":['mean', 'min', 'max']})
    agg.columns = agg.columns.droplevel(0)
    agg = agg.add_suffix("").reset_index()

    # 長形式に変換
    agg_long = pd.melt(agg, id_vars=["year"], var_name="metric", value_name="high_bid")

    # レイヤーチャート
    line = alt.Chart(agg_long).mark_line(point=True).encode(
        x=alt.X('year:Q', title='年', scale=alt.Scale(domain=[1998, 2025])),
        y=alt.Y('high_bid:Q', title='落札価格 ($/lb)', scale=alt.Scale(domain=[0, 450])),
        color=alt.Color('metric:N', 
                    scale=alt.Scale(
                        domain=['mean', 'min', 'max'],
                        range=['#667eea', '#f093fb', '#f5576c']
                    ),
                    legend=alt.Legend(
                        title='統計量',
                        labelExpr="datum.label === 'mean' ? '平均' : datum.label === 'min' ? '最小' : '最大'"
                    )),
        tooltip=['year:Q', 'metric:N', alt.Tooltip('high_bid:Q', format='.2f')]
    ).properties(height=400)

    st.altair_chart(line, use_container_width=True)

    # インサイト
    max_year = agg.loc[agg['mean'].idxmax(), 'year']
    max_avg = agg['mean'].max()
    
    st.markdown(f"""
    <div class="insight-box">
        <h3>💡 インサイト</h3>
        <p>最も落札価格が高かった年は <strong>{int(max_year)}年</strong>で、
        平均 <strong>${max_avg:.2f}/lb</strong> を記録しました。</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("時系列分析に必要なデータが不足しています")

st.markdown("---")

# セクション3: 分布分析
st.header("📊 分布分析：品質スコアと価格")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("落札価格の分布")
    h1 = alt.Chart(df).mark_bar(color='#667eea').encode(
        x=alt.X('high_bid:Q', bin=alt.Bin(step=5, extent=[0, 500]), title='落札価格 ($/lb)'),
        y=alt.Y('count()', title='頻度'),
        tooltip=['count()']
    ).properties(height=350)
    st.altair_chart(h1, use_container_width=True)

with col_right:
    st.subheader("品質スコアの分布")
    h2 = alt.Chart(df).mark_bar(color='#f093fb').encode(
        x=alt.X('score:Q', bin=alt.Bin(step=0.5, extent=[70, 100]), title='スコア'),
        y=alt.Y('count()', title='頻度'),
        tooltip=['count()']
    ).properties(height=350)
    st.altair_chart(h2, use_container_width=True)

st.markdown("---")

# セクション4: 相関分析
st.header("🔗 相関分析：スコアと価格の関係")
st.write("品質スコアが高いほど、落札価格も高くなる傾向があるのか？")

scatter = alt.Chart(df).mark_circle(size=60, opacity=0.6).encode(
    x=alt.X('score:Q', scale=alt.Scale(domain=[80, 100]), title='スコア'),
    y=alt.Y('high_bid:Q', scale=alt.Scale(domain=[0, 500]), title='落札価格 ($/lb)'),
    color=alt.Color('year:Q', 
                   scale=alt.Scale(domain=[1998, 2025], scheme='turbo'),
                   legend=alt.Legend(title='年')),
    tooltip=['score:Q', alt.Tooltip('high_bid:Q', format='.2f'), 'year:Q', 'country:N']
).transform_filter(
    (alt.datum.award_category == "coe")
).properties(height=450).interactive()

st.altair_chart(scatter, use_container_width=True)

# 相関係数計算
if 'score' in df.columns and 'high_bid' in df.columns:
    correlation = df[['score', 'high_bid']].corr().iloc[0, 1]
    st.markdown(f"""
    <div class="insight-box">
        <h3>📐 統計的インサイト</h3>
        <p>スコアと落札価格の相関係数: <strong>{correlation:.3f}</strong></p>
        <p>{'正の相関が見られます。スコアが高いコーヒーほど、高値で取引される傾向があります。' if correlation > 0.5 else '相関は弱めですが、品質以外の要因（希少性、産地など）も価格に影響しています。'}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# セクション5: 箱ひげ図
st.header("📦 箱ひげ図：分布の可視化")

box_col1, box_col2 = st.columns(2)

with box_col1:
    st.subheader("年ごとのスコア分布")
    box1 = alt.Chart(df).mark_boxplot(extent='min-max', color='#667eea').encode(
        x=alt.X('year:O', title='年'),
        y=alt.Y('score:Q', scale=alt.Scale(domain=[80, 100]), title='スコア'),
        tooltip=['year:O']
    ).properties(height=350)
    st.altair_chart(box1, use_container_width=True)

with box_col2:
    st.subheader("国ごとの標高分布")
    box2 = alt.Chart(df).mark_boxplot(extent='min-max', color='#f093fb').encode(
        x=alt.X('country:N', title='国'),
        y=alt.Y('avg_altitude:Q', scale=alt.Scale(domain=[0, 3000]), title='平均標高 (m)'),
        tooltip=['country:N']
    ).properties(height=350)
    st.altair_chart(box2, use_container_width=True)

st.markdown("---")

# まとめ
st.header("📚 統計学が教えてくれること")
st.write("""
Cup of Excellenceのデータを統計的に分析することで、以下のことが明らかになりました：

- **品質と価格**: スコアと落札価格には正の相関があり、品質が市場価値に反映される
- **時系列トレンド**: 年によって落札価格は大きく変動し、市場の動向を反映
- **分布の特徴**: 多くのコーヒーは特定のスコア帯に集中し、高得点は希少
- **地理的多様性**: 国ごとに標高分布が異なり、テロワールの重要性を示唆

統計学を通じて、データに潜むストーリーを読み解くことができました。
""")