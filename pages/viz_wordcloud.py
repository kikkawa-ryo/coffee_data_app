import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

from utils.data_utils import query
from utils.wordcloud_color_generator import SimpleGroupedColorFunc

st.set_page_config(
    page_title="Flavor Chemistry",
    page_icon="🧪",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .flavor-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(120deg, #fa709a 0%, #fee140 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chemistry-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        color: #2d3436;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .flavor-fact {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #fa709a;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# データ取得
df = query()

# ヘッダー
st.markdown("""
<div class="flavor-header">
    <h1>🧪 化学で解き明かす、フレーバーの宇宙</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        コーヒーの味と香りを生み出す、分子の世界
    </p>
</div>
""", unsafe_allow_html=True)

# イントロダクション
st.markdown("""
### 化学とコーヒー

コーヒーの複雑な味わいと香りは、**800種類以上の化学物質**が生み出しています。
ロースト過程でのメイラード反応やカラメル化により、糖とアミノ酸が反応し、
無数のフレーバー化合物が形成されます。

このページでは、COEのテイスティングノートから抽出されたフレーバー表現を分析し、
コーヒーの化学的多様性を可視化します。
""")

st.markdown("---")

# セクション1: Flavor Wheel
st.header("🎨 Coffee Flavor Wheel")
st.write("""
Flavor Wheelは、コーヒーのフレーバーを体系的に分類したもの。
中心から外側へ、より具体的なフレーバー表現に分かれています。
""")

st.image('images/flavor-wheel-en.png', 
         caption='Coffee Flavor Wheel - SCAが開発したコーヒーフレーバーの分類体系',
         use_container_width=True)

st.markdown("""
<div class="chemistry-box">
    <h3>🔬 化学的背景</h3>
    <p><strong>フルーティー（Fruity）</strong>: エステル類、アルデヒド類が生み出す甘い香り</p>
    <p><strong>フローラル（Floral）</strong>: リナロール、ゲラニオールなどのテルペン類</p>
    <p><strong>ナッツ（Nutty）</strong>: ピラジン類によるロースト香</p>
    <p><strong>チョコレート（Chocolate）</strong>: メイラード反応で生成されるアルデヒド類</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# セクション2: Word Cloud by Category
st.header("☁️ フレーバー表現の可視化")
st.write("実際のテイスティングノートで使われる言葉の頻度を分析")

# カラーマッピング設定
color_to_words = {
    '#CF5552': ["berry", "blackberry", "raspberry", "blueberry", "strawberry"],
    '#BC5245': ["dried fruit", "raisin", "prune"],
    '#E47050': ['coconut', 'cherry', 'pomegranate', 'pineapple', 'grape', 'apple', 'peach', 'pear'],
    '#F69114': ["citrus", "grapefruit", "orange", "lemon", "lime"],
    '#DABB0B': ["sour", "acetic", "butyric", "isovaleric", "citric", "malic"],
    '#A1881E': ["alcohol", "winey", "whiskey", "fermented", "overripe"],
    '#92A516': ['olive'],
    '#2C9640': ["green", "vegetative", "under ripe", "peapod", "fresh", "dark green", "hay", "herb"],
    '#BB7554': ["nutty", "peanut", "hazelnut", "almond"],
    '#AE6237': ["cocoa", "chocolate", "dark chocolate"],
    '#CA4344': ["brown sugar", "molasses", "maple syrup", "caramelized", "honey", "caramel"],
    '#F7856A': ["vanilla", "vanillin"],
    '#D3759B': ["floral", "chamomile", "rose", "jasmine"],
}
default_color = '#2d3436'
grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

# タブで分類
if df.empty:
    st.warning("データが取得できませんでした。")
else:
    tab1, tab2, tab3 = st.tabs(["🍋 Acidity（酸味）", "💐 Aroma / Flavor（香り・風味）", "☕️ Overall（全体印象）"])

    with tab1:
        st.subheader("Acidityに使われる言葉")
        st.write("酸味は、クエン酸、リンゴ酸、酒石酸などの有機酸によって生まれます")
        
        if 'acidity_str_agg' in df.columns:
            descriptions = pd.concat([df['acidity_str_agg']], ignore_index=True, axis=0).dropna()
            if not descriptions.empty:
                descriptions_unique = descriptions.map(lambda l: ",".join(list(set(l.split(",")))))
                descriptions_list = ",".join(descriptions_unique).split(",")
                c = Counter(descriptions_list)
                d = {t[0]: t[1] for t in c.most_common(50)}  # 上位50個
                
                if d:
                    wordcloud = WordCloud(
                        width=900, 
                        height=500, 
                        background_color='white', 
                        colormap="RdYlGn"
                    ).fit_words(d)
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                    
                    st.markdown(f"""
                    <div class="flavor-fact">
                        <p>💡 Acidityカテゴリで最も頻出する表現: <strong>{list(d.keys())[0]}</strong> ({list(d.values())[0]}回)</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("表示する単語データがありません")
            else:
                st.info("データが見つかりません")
        else:
            st.error("必要なデータカラム(acidity_str_agg)が見つかりません")

    with tab2:
        st.subheader('Aroma / Flavorに使われる言葉')
        st.write("香りと風味は、揮発性化合物の複雑な組み合わせで構成されます")
        
        if 'aroma_flavor_str_agg' in df.columns:
            descriptions = pd.concat([df['aroma_flavor_str_agg']], ignore_index=True, axis=0).dropna()
            if not descriptions.empty:
                descriptions_unique = descriptions.map(lambda l: ",".join(list(set(l.split(",")))))
                descriptions_list = ",".join(descriptions_unique).split(",")
                c = Counter(descriptions_list)
                d = {t[0]: t[1] for t in c.most_common(100)}  # 上位100個
                
                if d:
                    wordcloud = WordCloud(
                        width=900,
                        height=500,
                        background_color='white',
                        color_func=grouped_color_func
                    ).fit_words(d)
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                    
                    # Top 10表示
                    st.subheader("📊 Top 10 フレーバー表現")
                    top10 = pd.DataFrame(list(d.items())[:10], columns=['フレーバー', '頻度'])
                    st.dataframe(top10, use_container_width=True)
                else:
                    st.info("表示する単語データがありません")
            else:
                st.info("データが見つかりません")
        else:
            st.error("必要なデータカラム(aroma_flavor_str_agg)が見つかりません")

    with tab3:
        st.subheader('Overall（全体的な印象）に使われる言葉')
        st.write("全体的な印象は、酸味、甘味、苦味、ボディのバランスで決まります")
        
        # 必要なカラムの存在チェック
        target_cols = ['other_str_agg', 'overall_str_agg', 'characteristics_str_agg']
        existing_cols = [col for col in target_cols if col in df.columns]
        
        if existing_cols:
            descriptions = pd.concat([df[col] for col in existing_cols], ignore_index=True, axis=0).dropna()
            
            if not descriptions.empty:
                descriptions_unique = descriptions.map(lambda l: ",".join(list(set(l.split(",")))))
                descriptions_list = ",".join(descriptions_unique).split(",")
                c = Counter(descriptions_list)
                d = {t[0]: t[1] for t in c.most_common(50)}
                
                if d:
                    wordcloud = WordCloud(
                        width=900,
                        height=500,
                        background_color='white',
                        colormap="Set2"
                    ).fit_words(d)
                    
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                    
                    st.markdown(f"""
                    <div class="flavor-fact">
                        <p>💡 Overall評価で最も頻出する表現: <strong>{list(d.keys())[0]}</strong> ({list(d.values())[0]}回)</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("表示する単語データがありません")
            else:
                st.info("データが見つかりません")
        else:
             st.error("必要なデータカラムが見つかりません")

st.markdown("---")

# セクション3: まとめ
st.header("🔬 化学が明かす、味の複雑さ")

st.write("""
コーヒーのフレーバーは、単純な「苦い」「酸っぱい」だけでなく、
フルーティ、フローラル、ナッツ、チョコレートなど、**無限のバリエーション**があります。

### フレーバー形成のメカニズム

1. **生豆の段階**: 品種、土壌、標高が基本的な化学組成を決定
2. **ロースト**: 熱によってメイラード反応、カラメル化が進行
3. **抽出**: 水温、時間、圧力が最終的なフレーバーを調整

### 主要な化学物質群

- **有機酸**: クエン酸、リンゴ酸 → 酸味
- **糖類**: グルコース、フルクトース → 甘味
- **ピラジン類**: ナッツ、ロースト香
- **フラン類**: キャラメル、sweet aroma
- **テルペン類**: フローラル、fruitynotes

コーヒー1杯に潜む化学の世界は、驚くほど奥深いのです。
""")

# データ情報
with st.expander("📊 データ詳細"):
    st.write(f"分析対象サンプル数: {len(df):,}")
    st.write(f"Acidity表現のユニーク数: {df['acidity_str_agg'].dropna().nunique():,}")
    st.write(f"Aroma/Flavor表現のユニーク数: {df['aroma_flavor_str_agg'].dropna().nunique():,}")