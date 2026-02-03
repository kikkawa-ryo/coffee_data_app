#!/usr/bin/env python3
"""Fun Facts用のデータ分析スクリプト"""
import pandas as pd

print('=== Fun Facts用データ分析 ===\n')

# Coffee C priceデータ分析
df_price = pd.read_csv('data/coffee_c_price_full.csv')
df_price['Date'] = pd.to_datetime(df_price['Date'])
df_price['year'] = df_price['Date'].dt.year

print('📈 Coffee C Price 分析:')
print(f'  - データ期間: {df_price["Date"].min().strftime("%Y年%m月")} ～ {df_price["Date"].max().strftime("%Y年%m月")}')
max_idx = df_price['price_usd_lb'].idxmax()
min_idx = df_price['price_usd_lb'].idxmin()
print(f'  - 最高価格: ${df_price["price_usd_lb"].max():.2f}/lb ({df_price.loc[max_idx, "Date"].strftime("%Y年%m月%d日")})')
print(f'  - 最低価格: ${df_price["price_usd_lb"].min():.2f}/lb ({df_price.loc[min_idx, "Date"].strftime("%Y年%m月%d日")})')
print(f'  - 価格変動率: {((df_price["price_usd_lb"].max() / df_price["price_usd_lb"].min() - 1) * 100):.1f}%')
print()

# 年次統計
yearly_stats = df_price.groupby('year')['price_usd_lb'].agg(['mean', 'max', 'min', 'std'])
print(f'  - 最も価格が高かった年: {yearly_stats["mean"].idxmax()}年 (平均${yearly_stats["mean"].max():.2f}/lb)')
print(f'  - 最も変動が大きかった年: {yearly_stats["std"].idxmax()}年 (標準偏差${yearly_stats["std"].max():.2f})')
print()

# フレーバーデータ分析
df_flavor = pd.read_csv('data/flavor_wheel_lexicon.csv')
print('🎨 Flavor Wheel 分析:')
print(f'  - カテゴリ1の数: {df_flavor["Category1"].nunique()}種類')
print(f'  - カテゴリ2の数: {df_flavor["Category2"].nunique()}種類')
print(f'  - カテゴリ3の数: {df_flavor["Category3"].nunique()}種類')
print(f'  - フレーバー総数: {len(df_flavor)}個')
print()

print('✅ データ分析完了')
