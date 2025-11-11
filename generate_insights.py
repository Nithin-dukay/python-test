import pandas as pd
import json
from datetime import datetime

# Read the CSV file
df = pd.read_csv('steamcharts.csv')

# Convert month to datetime for proper sorting
def parse_month(month_str):
    return datetime.strptime(month_str, '%b-%y')

df['month_date'] = df['month'].apply(parse_month)
df = df.sort_values(['steam_appid', 'month_date'])

print("=== Phase 3: Pattern Detection and Insights ===")

# Get latest month data
latest_month = df['month_date'].max()
latest_month_str = latest_month.strftime('%b-%y')
latest_data = df[df['month_date'] == latest_month].copy()

# Trend analysis - games with consistent growth
print("\n=== Games with Consistent Growth (Last 6 Months) ===")
six_months_ago = pd.Timestamp(latest_month) - pd.DateOffset(months=6)
recent_data = df[df['month_date'] >= six_months_ago].copy()

growth_consistency = []
for appid in recent_data['steam_appid'].unique():
    game_data = recent_data[recent_data['steam_appid'] == appid].sort_values('month_date')
    if len(game_data) >= 6:
        positive_months = (game_data['gain_percent'] > 0).sum()
        avg_growth = game_data['gain_percent'].mean()
        if positive_months >= 4 and avg_growth > 5:
            growth_consistency.append({
                'name': game_data['name'].iloc[0],
                'appid': appid,
                'positive_months': positive_months,
                'avg_growth': avg_growth,
                'current_players': game_data['avg_players'].iloc[-1]
            })

if growth_consistency:
    growth_df = pd.DataFrame(growth_consistency).sort_values('avg_growth', ascending=False).head(15)
    print(growth_df)
else:
    growth_df = pd.DataFrame()
    print("No games found with consistent growth pattern")

# Market segments analysis
print("\n=== Market Segment Analysis ===")
segments = {
    'AAA Blockbusters': latest_data[latest_data['avg_players'] >= 100000],
    'Popular Games': latest_data[(latest_data['avg_players'] >= 10000) & (latest_data['avg_players'] < 100000)],
    'Mid-tier Games': latest_data[(latest_data['avg_players'] >= 1000) & (latest_data['avg_players'] < 10000)],
    'Indie Games': latest_data[(latest_data['avg_players'] >= 100) & (latest_data['avg_players'] < 1000)],
    'Niche Games': latest_data[latest_data['avg_players'] < 100]
}

for segment_name, segment_data in segments.items():
    avg_growth = segment_data['gain_percent'].mean()
    median_players = segment_data['avg_players'].median()
    count = len(segment_data)
    print(f"\n{segment_name}:")
    print(f"  Count: {count}")
    print(f"  Median Players: {median_players:.2f}")
    print(f"  Average Growth: {avg_growth:.2f}%")

# Seasonal patterns
print("\n=== Seasonal Patterns Analysis ===")
df['month_name'] = df['month_date'].dt.month_name()
seasonal_growth = df.groupby('month_name')['gain_percent'].agg(['mean', 'median', 'count'])
seasonal_growth = seasonal_growth.reindex(['January', 'February', 'March', 'April', 'May', 'June', 
                                           'July', 'August', 'September', 'October', 'November', 'December'])
print(seasonal_growth)

# Volatility analysis - most stable vs most volatile games
print("\n=== Game Stability Analysis (Top 100 Games) ===")
top_100_appids = latest_data.nlargest(100, 'avg_players')['steam_appid'].tolist()
volatility_data = []

for appid in top_100_appids:
    game_data = df[df['steam_appid'] == appid].sort_values('month_date')
    if len(game_data) >= 12:
        volatility = game_data['gain_percent'].std()
        avg_players = game_data['avg_players'].mean()
        volatility_data.append({
            'name': game_data['name'].iloc[0],
            'volatility': volatility,
            'avg_players': avg_players
        })

volatility_df = pd.DataFrame(volatility_data)
print("\nMost Stable Games (Low Volatility):")
print(volatility_df.nsmallest(10, 'volatility')[['name', 'volatility', 'avg_players']])
print("\nMost Volatile Games (High Volatility):")
print(volatility_df.nlargest(10, 'volatility')[['name', 'volatility', 'avg_players']])

# Long-term trends
print("\n=== Long-term Trend Analysis ===")
for appid in latest_data.nlargest(5, 'avg_players')['steam_appid'].tolist():
    game_data = df[df['steam_appid'] == appid].sort_values('month_date')
    game_name = game_data['name'].iloc[0]
    
    # Calculate year-over-year growth
    one_year_ago = latest_month - pd.DateOffset(months=12)
    current_players = game_data[game_data['month_date'] == latest_month]['avg_players'].values
    past_players = game_data[game_data['month_date'] == one_year_ago]['avg_players'].values
    
    if len(current_players) > 0 and len(past_players) > 0:
        yoy_growth = ((current_players[0] - past_players[0]) / past_players[0]) * 100
        print(f"\n{game_name}:")
        print(f"  Current: {current_players[0]:,.2f} players")
        print(f"  1 Year Ago: {past_players[0]:,.2f} players")
        print(f"  YoY Growth: {yoy_growth:.2f}%")

print("\n=== Generating comprehensive insights JSON ===")

# Compile all insights
insights = {
    'dataset_overview': {
        'total_records': len(df),
        'unique_games': df['steam_appid'].nunique(),
        'date_range': {
            'start': df['month_date'].min().strftime('%Y-%m-%d'),
            'end': df['month_date'].max().strftime('%Y-%m-%d')
        },
        'months_covered': df['month'].nunique()
    },
    'latest_month': {
        'month': latest_month_str,
        'top_10_games': latest_data.nlargest(10, 'avg_players')[['name', 'avg_players', 'peak_players', 'gain_percent']].to_dict('records'),
        'fastest_growing': latest_data.nlargest(10, 'gain_percent')[['name', 'avg_players', 'gain_percent']].to_dict('records'),
        'biggest_declines': latest_data.nsmallest(10, 'gain_percent')[['name', 'avg_players', 'gain_percent']].to_dict('records')
    },
    'market_segments': {
        segment: {
            'count': len(data),
            'median_players': float(data['avg_players'].median()),
            'avg_growth_percent': float(data['gain_percent'].mean())
        }
        for segment, data in segments.items()
    },
    'consistent_growers': growth_df.to_dict('records') if not growth_df.empty else [],
    'all_time_peaks': df.groupby('name')['peak_players'].max().nlargest(20).to_dict()
}

# Save insights to JSON
with open('steamcharts_insights.json', 'w') as f:
    json.dump(insights, f, indent=2, default=str)

print("\n✓ Insights saved to steamcharts_insights.json")
print(f"\n=== Analysis Complete ===")
print(f"Total games analyzed: {df['steam_appid'].nunique():,}")
print(f"Total data points: {len(df):,}")
print(f"Time period: {df['month_date'].min().strftime('%B %Y')} to {df['month_date'].max().strftime('%B %Y')}")
