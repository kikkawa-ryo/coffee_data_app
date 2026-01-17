import streamlit as st
import pandas as pd
import pydeck as pdk
import math

# -----------------------------------------------------------------------------
# 1. Config & Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="My Coffee Flight Log",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# スタイル調整（余白を減らし、没入感を高める）
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    div[data-testid="stMetricValue"] { font-size: 2rem; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading & Processing
# -----------------------------------------------------------------------------
# 日本（東京）の座標を旅の拠点とする
HOME_LAT = 35.6895
HOME_LON = 139.6917

@st.cache_data
def load_data():
    """
    CSVファイルを読み込み、必要な前処理を行う関数
    """
    # CSVの読み込み
    df = pd.read_csv("data/flight_sample.csv")

    # 緯度経度カラムのゆらぎ吸収（latitude -> lat, longitude -> lon）
    rename_map = {}
    if "latitude" in df.columns:
        rename_map["latitude"] = "lat"
    if "longitude" in df.columns:
        rename_map["longitude"] = "lon"
    
    if rename_map:
        df = df.rename(columns=rename_map)

    # 緯度経度がないデータ（特定できなかったデータ）を除外
    # ※ 地図描画でエラーになるのを防ぐため
    if "lat" in df.columns and "lon" in df.columns:
        df = df.dropna(subset=["lat", "lon"])
    else:
        st.error("CSVファイルに緯度経度情報（latitude/longitude）が見つかりません。")
        st.stop()

    # 旅の起点（東京）の座標を全行に追加（ArcLayer用）
    df["home_lat"] = HOME_LAT
    df["home_lon"] = HOME_LON
    
    return df

def calculate_distance(lat1, lon1, lat2, lon2):
    """2点間の距離(km)を計算する（Haversine formula簡易版）"""
    R = 6371  # 地球の半径 (km)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# データ読み込み実行
try:
    df = load_data()
except Exception as e:
    st.error(f"データの読み込みに失敗しました: {e}")
    st.stop()

# 距離計算 (データがある場合のみ)
if not df.empty:
    df["distance_km"] = df.apply(lambda x: calculate_distance(HOME_LAT, HOME_LON, x["lat"], x["lon"]), axis=1)
else:
    st.warning("表示できるデータがありません（緯度経度情報が含まれるデータが0件です）。")
    st.stop()

# -----------------------------------------------------------------------------
# 3. Sidebar Filters
# -----------------------------------------------------------------------------
st.sidebar.title("✈️ Flight Settings")
st.sidebar.markdown("あなたのコーヒージャーニーを振り返りましょう。")

# 年ごとのフィルタ
if "year" in df.columns:
    available_years = sorted(df["year"].unique(), reverse=True)
    selected_years = st.sidebar.multiselect(
        "Filter by Year",
        options=available_years,
        default=available_years
    )
    if selected_years:
        df = df[df["year"].isin(selected_years)]

# 国ごとのフィルタ (countryカラムがあるので利用)
if "country" in df.columns:
    selected_countries = st.sidebar.multiselect(
        "Filter by Country",
        options=df["country"].unique(),
        default=df["country"].unique()
    )
    if selected_countries:
        filtered_df = df[df["country"].isin(selected_countries)]
    else:
        filtered_df = df
else:
    filtered_df = df

# -----------------------------------------------------------------------------
# 4. KPI Metrics (The "Stats")
# -----------------------------------------------------------------------------
st.title("☕ My Coffee Flight Log")

# 統計情報の計算
total_cups = len(filtered_df)
total_distance = filtered_df["distance_km"].sum()
earth_circumference = 40075
orbit_count = total_distance / earth_circumference

# カラム構成
if "country" in filtered_df.columns:
    total_countries = filtered_df["country"].nunique()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Beans", f"{total_cups} Bags", delta="Flight Count")
    with col2:
        st.metric("Countries Visited", f"{total_countries} Countries")
    with col3:
        st.metric("Total Distance", f"{int(total_distance):,} km")
    with col4:
        st.metric("Earth Orbits", f"{orbit_count:.2f} laps", help="地球を何周分旅したか")
else:
    col1, col3, col4 = st.columns(3)
    with col1:
        st.metric("Total Beans", f"{total_cups} Bags", delta="Flight Count")
    with col3:
        st.metric("Total Distance", f"{int(total_distance):,} km")
    with col4:
        st.metric("Earth Orbits", f"{orbit_count:.2f} laps")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Map Visualization (PyDeck ArcLayer)
# -----------------------------------------------------------------------------
# Tooltipの設定
tooltip_html = "<b>{name}</b><br/>"
if "country" in filtered_df.columns:
    tooltip_html += "📍 {location}, {country}<br/>"
else:
    tooltip_html += "📍 {location}<br/>"
tooltip_html += "📏 {distance_km} km from Tokyo"

tooltip = {
    "html": tooltip_html,
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# 1. Arc Layer (フライトライン: 東京 -> 農園)
arc_layer = pdk.Layer(
    "ArcLayer",
    data=filtered_df,
    get_source_position=["home_lon", "home_lat"],
    get_target_position=["lon", "lat"],
    get_source_color=[0, 128, 200, 100],   # Tokyo側（青）
    get_target_color=[255, 165, 0, 200],   # 農園側（オレンジ）
    get_width=3,
    get_tilt=15,
    pickable=True,
    auto_highlight=True,
)

# 2. Scatter Layer (農園の場所)
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position=["lon", "lat"],
    get_color=[255, 165, 0, 200],
    get_radius=50000,  # 半径(メートル)
    pickable=True,
)

# 3. Home Base Layer (東京)
home_layer = pdk.Layer(
    "ScatterplotLayer",
    data=pd.DataFrame([{"lat": HOME_LAT, "lon": HOME_LON, "name": "Light Up Coffee (Tokyo)"}]),
    get_position=["lon", "lat"],
    get_color=[0, 128, 200, 255],
    get_radius=80000,
    pickable=True,
)

# マップの表示設定
view_state = pdk.ViewState(
    latitude=20.0,
    longitude=10.0,
    zoom=1.2,
    pitch=30,
)

deck = pdk.Deck(
    # APIキー不要のCARTOスタイル
    map_style=pdk.map_styles.CARTO_LIGHT, 
    initial_view_state=view_state,
    layers=[arc_layer, scatter_layer, home_layer],
    tooltip=tooltip
)

st.pydeck_chart(deck)

# -----------------------------------------------------------------------------
# 6. Detailed Data View (The "Passport Stamps")
# -----------------------------------------------------------------------------
st.subheader("📋 Flight Manifest")
st.markdown("旅の記録（詳細データ）")

# 表示したいカラム（データの状況に合わせて調整）
candidate_cols = ["url", "year", "month", "country", "name", "producer", "farm", "washing_station", "elevation", "flavor_comment", "location", "distance_km"]
display_cols = [c for c in candidate_cols if c in filtered_df.columns]

# データフレーム設定
col_config = {
    "distance_km": st.column_config.NumberColumn(
        "Distance (km)",
        format="%d km"
    ),
    "year": st.column_config.NumberColumn(
        "Year",
        format="%d"
    ),
    # URLカラムをリンクとして設定
    "url": st.column_config.LinkColumn(
        "Store Page",       # ヘッダー名
        display_text="View ☕"  # 実際のURLの代わりに表示するテキスト
    )
}

st.dataframe(
    filtered_df[display_cols].sort_values("distance_km", ascending=False),
    use_container_width=True,
    column_config=col_config
)