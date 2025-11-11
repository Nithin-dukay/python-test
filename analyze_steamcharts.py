import pandas as pd
import json
import numpy as np
from datetime import datetime

# Read the CSV file
df = pd.read_csv('steamcharts.csv')

# Convert month to datetime for proper sorting
def parse_month(month_str):
    return datetime.strptime(month_str, '%b-%y')

df['month_date'] = df['month'].apply(parse_month)
df = df.sort_values(['steam_appid', 'month_date'])

print("=== Phase 2: Deep Analysis ===")

# Unique values analysis
print(f"\nNumber of unique games: {df['steam_appid'].nunique()}")
print(f"Number of unique game names: {df['name'].nunique()}")
print(f"Number of unique months: {df['month'].nunique()}")
print(f"Unique months: {sorted(df['month'].unique())}")

# Top games by average players
print("\n=== Top 20 Games by Average Players (Latest Month) ===")
latest_month = df['month'].iloc[0]
latest_data = df[df['month'] == latest_month].sort_values('avg_players', ascending=False)
print(latest_data[['name', 'avg_players', 'peak_players', 'gain_percent']].head(20))

# Games with highest peak players
print("\n=== Top 20 Games by Peak Players (All Time) ===")
top_peak = df.groupby('name')['peak_players'].max().sort_values(ascending=False).head(20)
print(top_peak)

# Games with highest growth
print("\n=== Top 20 Games by Growth Percentage (Latest Month) ===")
top_growth = latest_data.sort_values('gain_percent', ascending=False)
print(top_growth[['name', 'avg_players', 'gain_percent']].head(20))

# Games with biggest decline
print("\n=== Top 20 Games by Decline (Latest Month) ===")
top_decline = latest_data.sort_values('gain_percent', ascending=True)
print(top_decline[['name', 'avg_players', 'gain_percent']].head(20))

# Time series analysis for top games
print("\n=== Time Series Data Available ===")
top_5_games = latest_data.nlargest(5, 'avg_players')['steam_appid'].tolist()
for appid in top_5_games:
    game_data = df[df['steam_appid'] == appid]
    game_name = game_data['name'].iloc[0]
    print(f"\n{game_name} (AppID: {appid})")
    print(f"  Data points: {len(game_data)}")
    print(f"  Date range: {game_data['month'].iloc[-1]} to {game_data['month'].iloc[0]}")
    print(f"  Avg players range: {game_data['avg_players'].min():.2f} to {game_data['avg_players'].max():.2f}")

# Category analysis
print("\n=== Player Count Categories ===")
bins = [0, 10, 100, 1000, 10000, 100000, float('inf')]
labels = ['0-10', '10-100', '100-1K', '1K-10K', '10K-100K', '100K+']
df['player_category'] = pd.cut(df['avg_players'], bins=bins, labels=labels)
print(df['player_category'].value_counts().sort_index())
