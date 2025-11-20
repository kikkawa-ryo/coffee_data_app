import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from altair import datum

from utils.data_utils import query

_="""
全ページ共通の処理
"""
# サイドバー
# with st.sidebar:
#     st.page_link("app.py", label="！ホーム", icon="🏠")
#     st.page_link("pages/viz_scatterplot.py", label="scatterplot", icon="📈")
#     st.page_link("pages/viz_lineplot.py", label="lineplot", icon="📈")
#     st.page_link("pages/viz_barplot.py", label="barplot", icon="📊")
#     st.page_link("pages/02_boxplot.py", label="boxplot", icon="📊")
#     st.page_link("pages/01_wordcloud.py", label="wordcloud", icon="🍷")
#     st.page_link("pages/gallery.py", label="gallery", icon="🖼")
# データの取得
df = query()

_="""
全ページ共通の処理
"""
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ページ設定
# st.set_page_config(layout="wide")

# --- 1. データ構造 ---
location_data = [
    {'name': 'STREAMER COFFEE COMPANY', 'lat': 35.66415, 'lon': 139.69831, 'type': 'shop', 'brand': 'STREAMER COFFEE', 'repr': True},
    {'name': 'ONIBUS COFFEE 中目黒', 'lat': 35.64453, 'lon': 139.70321, 'type': 'shop', 'brand': 'ONIBUS COFFEE', 'repr': True},
    {'name': 'ONIBUS COFFEE 八雲', 'lat': 35.6318, 'lon': 139.6703, 'type': 'shop', 'brand': 'ONIBUS COFFEE', 'repr': False},
    {'name': 'BLUE BOTTLE COFFEE 清澄白河', 'lat': 35.68339, 'lon': 139.79955, 'type': 'shop', 'brand': 'BLUE BOTTLE COFFEE', 'repr': True},
    {'name': 'Finca El Injerto', 'lat': 15.1707, 'lon': -91.9183, 'type': 'farm', 'brand': None, 'repr': False},
    {'name': 'Gesha Village Estate', 'lat': 6.6435, 'lon': 35.8594, 'type': 'farm', 'brand': None, 'repr': False},
    {'name': 'Daterra Estate', 'lat': -18.4831, 'lon': -47.3917, 'type': 'farm', 'brand': None, 'repr': False},
    {'name': 'La Palma y El Tucán', 'lat': 4.8647, 'lon': -74.0152, 'type': 'farm', 'brand': None, 'repr': False},
    {'name': 'Finca Santa Teresa', 'lat': 8.8667, 'lon': -82.5500, 'type': 'farm', 'brand': None, 'repr': False},
]
locations_df = pd.DataFrame(location_data)

relations_data = {
    'STREAMER COFFEE': ['Daterra Estate', 'La Palma y El Tucán'],
    'ONIBUS COFFEE': ['Finca El Injerto', 'Gesha Village Estate'],
    'BLUE BOTTLE COFFEE': ['Gesha Village Estate', 'Finca Santa Teresa', 'Daterra Estate']
}

# --- 2. StreamlitアプリのUI ---
st.title('☕ コーヒーソーシングマップ (Folium版)')
st.markdown("コーヒーブランドを選択すると、代表店舗から農園への調達ルートと、ブランドの全店舗が表示されます。")

brand_names = list(relations_data.keys())
selected_brand = st.selectbox('コーヒーブランドを選択してください', brand_names)

# --- 3. 描画データの準備 ---
repr_shop_info = locations_df[(locations_df['brand'] == selected_brand) & (locations_df['repr'] == True)]
all_brand_shops_info = locations_df[locations_df['brand'] == selected_brand]
related_farm_names = relations_data.get(selected_brand, [])
related_farms_info = locations_df[locations_df['name'].isin(related_farm_names)]

# --- 4. Foliumによる地図描画 ---
if not repr_shop_info.empty:
    map_center = [repr_shop_info['lat'].iloc[0], repr_shop_info['lon'].iloc[0]]
    m = folium.Map(location=map_center, zoom_start=2)

    points_to_plot = pd.concat([all_brand_shops_info, related_farms_info])

    for _, point in points_to_plot.iterrows():
        icon_color = 'blue'
        if point['type'] == 'shop':
            icon_color = 'red' if point.get('repr', False) else 'orange'
        
        folium.Marker(
            location=[point['lat'], point['lon']],
            popup=f"<b>{point['name']}</b><br>({point['type']})",
            tooltip=point['name'],
            icon=folium.Icon(color=icon_color, icon='info-sign')
        ).add_to(m)

    if not related_farms_info.empty:
        source_lat = repr_shop_info['lat'].iloc[0]
        source_lon = repr_shop_info['lon'].iloc[0]
        
        for _, farm in related_farms_info.iterrows():
            farm_lat = farm['lat']
            farm_lon = farm['lon']
            
            if abs(farm_lon - source_lon) > 180:
                adjusted_farm_lon = farm_lon + 360 if farm_lon < source_lon else farm_lon - 360
                folium.PolyLine(locations=[[source_lat, source_lon], [farm_lat, adjusted_farm_lon]], color='red', weight=2.5, opacity=0.8).add_to(m)
            else:
                folium.PolyLine(locations=[[source_lat, source_lon], [farm_lat, farm_lon]], color='red', weight=2.5, opacity=0.8).add_to(m)

    st_folium(m, width=725, height=500, returned_objects=[])

else:
    st.warning('選択されたブランドの店舗または農園データが見つかりませんでした。')