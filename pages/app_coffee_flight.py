import streamlit as st
import pandas as pd
import pydeck as pdk
import math

st.set_page_config(
    page_title="Coffee Flight Map",
    page_icon="✈️",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
    .flight-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(120deg, #3494e6 0%, #ec6ead 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .geo-insight {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #2d3436;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stat-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #3494e6;
    }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class="flight-header">
    <h1>✈️ Coffee Flight Map</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        地理学で辿る、コーヒーの旅
    </p>
</div>
""", unsafe_allow_html=True)

# イントロダクション
st.markdown("""
### 🌍 地理学とコーヒー

地理学は、場所と空間の関係性を探る学問です。コーヒーの品質と味わいは、
**土地の記憶**が刻み込まれています：

- **緯度**: コーヒーベルト（赤道±25度）に集中する生産地
- **標高**: 高地ほど寒暖差が大きく、豊かなフレーバーが生まれる
- **土壌**: 火山性土壌、泥炭土など、terroir（テロワール）を形成
- **気候**: 降雨量、気温、日照時間が栽培を左右する

このマップは、あなたが飲んだコーヒーの「地理的な旅」を可視化します。
""")

st.markdown("---")

# データロード
HOME_LAT = 35.6895  # 東京
HOME_LON = 139.6917

@st.cache_data
def load_data():
    """CSVファイルを読み込み、前処理を行う"""
    df = pd.read_csv("data/flight_sample.csv")
    
    # カラム名の統一
    rename_map = {}
    if "latitude" in df.columns:
        rename_map["latitude"] = "lat"
    if "longitude" in df.columns:
        rename_map["longitude"] = "lon"
    
    if rename_map:
        df = df.rename(columns=rename_map)
    
    # 緯度経度がないデータを除外
    if "lat" in df.columns and "lon" in df.columns:
        df = df.dropna(subset=["lat", "lon"])
    else:
        st.error("CSVファイルに緯度経度情報がありません")
        st.stop()
    
    # 起点座標追加
    df["home_lat"] = HOME_LAT
    df["home_lon"] = HOME_LON
    
    return df

def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine formulaで2点間の距離を計算"""
    R = 6371  # 地球の半径 (km)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# データ読み込み
try:
    df = load_data()
except Exception as e:
    st.error(f"データ読み込みエラー: {e}")
    st.stop()

# 距離計算
if not df.empty:
    df["distance_km"] = df.apply(
        lambda x: calculate_distance(HOME_LAT, HOME_LON, x["lat"], x["lon"]), 
        axis=1
    )
else:
    st.warning("表示データがありません")
    st.stop()

# サイドバーフィルター
st.sidebar.header("🔍 フィルター")

if "year" in df.columns:
    available_years = sorted(df["year"].unique(), reverse=True)
    selected_years = st.sidebar.multiselect(
        "年で絞り込み",
        options=available_years,
        default=available_years
    )
    df = df[df["year"].isin(selected_years)] if selected_years else df

if "country" in df.columns:
    selected_countries = st.sidebar.multiselect(
        "国で絞り込み",
        options=df["country"].unique(),
        default=df["country"].unique()
    )
    filtered_df = df[df["country"].isin(selected_countries)] if selected_countries else df
else:
    filtered_df = df

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🗺️ マップの見方
- **青い点**: 東京（起点）
- **オレンジの点**: コーヒー生産地
- **アーク**: 地理的な距離を表現
""")

# 統計情報
st.header("📊 あなたのコーヒージャーニー統計")

total_cups = len(filtered_df)
total_distance = filtered_df["distance_km"].sum()
earth_circumference = 40075
orbit_count = total_distance / earth_circumference

if "country" in filtered_df.columns:
    total_countries = filtered_df["country"].nunique()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{total_cups}</h3>
            <p>コーヒー袋数</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{total_countries}</h3>
            <p>訪問国数</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{int(total_distance):,} km</h3>
            <p>総移動距離</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{orbit_count:.2f} 周</h3>
            <p>地球周回数</p>
        </div>
        """, unsafe_allow_html=True)

# 地理的インサイト
if "country" in filtered_df.columns and not filtered_df.empty:
    farthest = filtered_df.loc[filtered_df["distance_km"].idxmax()]
    nearest = filtered_df.loc[filtered_df["distance_km"].idxmin()]
    
    st.markdown(f"""
    <div class="geo-insight">
        <h3>🌏 地理的インサイト</h3>
        <p>🌟 <strong>最も遠い農園</strong>: {farthest.get('name', 'N/A')} ({farthest.get('country', 'N/A')}) - {farthest['distance_km']:.0f} km</p>
        <p>🏘️ <strong>最も近い農園</strong>: {nearest.get('name', 'N/A')} ({nearest.get('country', 'N/A')}) - {nearest['distance_km']:.0f} km</p>
        <p>🌍 コーヒーは地球を<strong>{orbit_count:.2f}周分</strong>旅してあなたの元へ届きました！</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# マップ可視化
st.header("🗺️ 世界コーヒーマップ")

if not filtered_df.empty:
    # Tooltip設定
    tooltip_html = "<b>{name}</b><br/>"
    if "country" in filtered_df.columns:
        tooltip_html += "📍 {location}, {country}<br/>"
    else:
        tooltip_html += "📍 {location}<br/>"
    tooltip_html += "📏 {distance_km:.0f} km from Tokyo"

    tooltip = {
        "html": tooltip_html,
        "style": {"backgroundColor": "#2d3436", "color": "white", "fontSize": "14px"}
    }

    # レイヤー定義
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=filtered_df,
        get_source_position=["home_lon", "home_lat"],
        get_target_position=["lon", "lat"],
        get_source_color=[52, 148, 230, 120],
        get_target_color=[236, 110, 173, 200],
        get_width=3,
        get_tilt=15,
        pickable=True,
        auto_highlight=True,
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_df,
        get_position=["lon", "lat"],
        get_color=[236, 110, 173, 220],
        get_radius=50000,
        pickable=True,
    )

    home_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame([{"lat": HOME_LAT, "lon": HOME_LON, "name": "Tokyo (Home)"}]),
        get_position=["lon", "lat"],
        get_color=[52, 148, 230, 255],
        get_radius=80000,
        pickable=True,
    )

    # マップ表示
    view_state = pdk.ViewState(
        latitude=20.0,
        longitude=10.0,
        zoom=1.2,
        pitch=35,
    )

    deck = pdk.Deck(
        map_style=pdk.map_styles.CARTO_LIGHT,
        initial_view_state=view_state,
        layers=[arc_layer, scatter_layer, home_layer],
        tooltip=tooltip
    )

    st.pydeck_chart(deck)
else:
    st.info("表示条件に一致するフライトデータがありません。フィルターを調整してください。")

st.markdown("---")

# データテーブル
st.header("📋 フライトマニフェスト")
st.write("旅の詳細記録")

if not filtered_df.empty:
    candidate_cols = [
        "url", "year", "month", "country", "name", "producer", 
        "farm", "washing_station", "elevation", "flavor_comment", 
        "location", "distance_km"
    ]
    display_cols = [c for c in candidate_cols if c in filtered_df.columns]

    col_config = {
        "distance_km": st.column_config.NumberColumn(
            "Distance (km)",
            format="%d km"
        ),
        "year": st.column_config.NumberColumn("Year", format="%d"),
        "url": st.column_config.LinkColumn("Store Page", display_text="View ☕")
    }

    st.dataframe(
        filtered_df[display_cols].sort_values(["year", "month"], ascending=False),
        use_container_width=True,
        column_config=col_config
    )
else:
    st.info("データがありません")

# まとめ
st.markdown("---")
st.header("🌍 地理が語る、コーヒーの物語")

st.write("""
このマップが示すのは、単なる距離ではなく、**場所と人のつながり**です。

### コーヒーベルトの奇跡

地球上でコーヒーが栽培できるのは、赤道を中心とした**南北回帰線の間**。
この限られたエリアに、驚くほど多様な風土が存在します：

- **中南米**: アンデス山脈の高地、豊かな火山性土壌  
- **アフリカ**: エチオピアの高原、ケニアの赤土  
- **アジア**: インドネシアの島々、ベトナムの高地  

それぞれの土地が、独自のフレーバーを生み出しています。

### Terroir（テロワール）

ワインの世界で使われる「テロワール」は、コーヒーにも当てはまります。
土壌、気候、標高、そして人の営みが、コーヒーの個性を形作ります。

あなたが飲む1杯のコーヒーは、遠く離れた土地の記憶を運んでくるのです。
""")