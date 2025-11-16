import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Create output directories
os.makedirs('./blackbox-analysis/visualization/', exist_ok=True)
os.makedirs('./blackbox-analysis/pdfs/', exist_ok=True)

print("=" * 80)
print("CREATING COMPREHENSIVE VISUALIZATIONS")
print("=" * 80)

# Load processed data
df = pd.read_csv('/vercel/sandbox/processed_orders.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

print(f"\n✓ Loaded {len(df)} records")

# 1. Sales and Profit Over Time
print("\n📊 Creating time series visualizations...")
fig, axes = plt.subplots(2, 1, figsize=(16, 10))

# Monthly sales trend
monthly_sales = df.groupby(df['Order Date'].dt.to_period('M')).agg({
    'Sales': 'sum',
    'Profit': 'sum'
})
monthly_sales.index = monthly_sales.index.to_timestamp()

axes[0].plot(monthly_sales.index, monthly_sales['Sales'], marker='o', linewidth=2, color='#2E86AB', label='Sales')
axes[0].fill_between(monthly_sales.index, monthly_sales['Sales'], alpha=0.3, color='#2E86AB')
axes[0].set_title('Monthly Sales Trend (2014-2017)', fontsize=16, fontweight='bold', pad=20)
axes[0].set_xlabel('Month', fontsize=12)
axes[0].set_ylabel('Sales ($)', fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].legend(fontsize=11)

# Monthly profit trend
axes[1].plot(monthly_sales.index, monthly_sales['Profit'], marker='o', linewidth=2, color='#06A77D', label='Profit')
axes[1].fill_between(monthly_sales.index, monthly_sales['Profit'], alpha=0.3, color='#06A77D')
axes[1].set_title('Monthly Profit Trend (2014-2017)', fontsize=16, fontweight='bold', pad=20)
axes[1].set_xlabel('Month', fontsize=12)
axes[1].set_ylabel('Profit ($)', fontsize=12)
axes[1].grid(True, alpha=0.3)
axes[1].legend(fontsize=11)

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/01_time_series_trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Time series trends saved")

# 2. Category Performance
print("\n📦 Creating category performance charts...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Sales by category
category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
colors = ['#E63946', '#F1FAEE', '#A8DADC']
axes[0, 0].bar(category_sales.index, category_sales.values, color=colors)
axes[0, 0].set_title('Total Sales by Category', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Sales ($)', fontsize=11)
axes[0, 0].tick_params(axis='x', rotation=0)
for i, v in enumerate(category_sales.values):
    axes[0, 0].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontsize=10)

# Profit by category
category_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
axes[0, 1].bar(category_profit.index, category_profit.values, color=colors)
axes[0, 1].set_title('Total Profit by Category', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Profit ($)', fontsize=11)
axes[0, 1].tick_params(axis='x', rotation=0)
for i, v in enumerate(category_profit.values):
    axes[0, 1].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontsize=10)

# Top 10 sub-categories by sales
subcat_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
axes[1, 0].barh(subcat_sales.index, subcat_sales.values, color='#457B9D')
axes[1, 0].set_title('Top 10 Sub-Categories by Sales', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Sales ($)', fontsize=11)
axes[1, 0].invert_yaxis()
for i, v in enumerate(subcat_sales.values):
    axes[1, 0].text(v, i, f' ${v/1000:.0f}K', va='center', fontsize=9)

# Profit margin by category
category_margin = df.groupby('Category').apply(lambda x: (x['Profit'].sum() / x['Sales'].sum()) * 100)
axes[1, 1].bar(category_margin.index, category_margin.values, color=['#06A77D' if x > 0 else '#E63946' for x in category_margin.values])
axes[1, 1].set_title('Profit Margin by Category', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('Profit Margin (%)', fontsize=11)
axes[1, 1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
axes[1, 1].tick_params(axis='x', rotation=0)
for i, v in enumerate(category_margin.values):
    axes[1, 1].text(i, v, f'{v:.1f}%', ha='center', va='bottom' if v > 0 else 'top', fontsize=10)

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/02_category_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Category performance saved")

# 3. Regional Analysis
print("\n🌎 Creating regional analysis charts...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Sales by region
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
colors_region = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261']
axes[0, 0].bar(region_sales.index, region_sales.values, color=colors_region)
axes[0, 0].set_title('Sales by Region', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Sales ($)', fontsize=11)
for i, v in enumerate(region_sales.values):
    axes[0, 0].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontsize=10)

# Profit by region
region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)
axes[0, 1].bar(region_profit.index, region_profit.values, color=colors_region)
axes[0, 1].set_title('Profit by Region', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Profit ($)', fontsize=11)
for i, v in enumerate(region_profit.values):
    axes[0, 1].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontsize=10)

# Top 10 states by sales
state_sales = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
axes[1, 0].barh(state_sales.index, state_sales.values, color='#E76F51')
axes[1, 0].set_title('Top 10 States by Sales', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Sales ($)', fontsize=11)
axes[1, 0].invert_yaxis()
for i, v in enumerate(state_sales.values):
    axes[1, 0].text(v, i, f' ${v/1000:.0f}K', va='center', fontsize=9)

# Customer segment distribution
segment_sales = df.groupby('Segment')['Sales'].sum()
axes[1, 1].pie(segment_sales.values, labels=segment_sales.index, autopct='%1.1f%%', 
               colors=['#8ECAE6', '#219EBC', '#023047'], startangle=90)
axes[1, 1].set_title('Sales Distribution by Customer Segment', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/03_regional_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Regional analysis saved")

# 4. Discount Impact Analysis
print("\n💰 Creating discount impact analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Create discount brackets
df['Discount Bracket'] = pd.cut(df['Discount'], 
                                 bins=[-0.01, 0, 0.1, 0.2, 0.3, 1.0],
                                 labels=['No Discount', '0-10%', '10-20%', '20-30%', '30%+'])

# Sales by discount bracket
discount_sales = df.groupby('Discount Bracket', observed=True)['Sales'].sum()
axes[0, 0].bar(range(len(discount_sales)), discount_sales.values, color='#4361EE')
axes[0, 0].set_xticks(range(len(discount_sales)))
axes[0, 0].set_xticklabels(discount_sales.index, rotation=45, ha='right')
axes[0, 0].set_title('Sales by Discount Level', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Sales ($)', fontsize=11)
for i, v in enumerate(discount_sales.values):
    axes[0, 0].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontsize=9)

# Profit by discount bracket
discount_profit = df.groupby('Discount Bracket', observed=True)['Profit'].sum()
colors_profit = ['#06A77D' if x > 0 else '#E63946' for x in discount_profit.values]
axes[0, 1].bar(range(len(discount_profit)), discount_profit.values, color=colors_profit)
axes[0, 1].set_xticks(range(len(discount_profit)))
axes[0, 1].set_xticklabels(discount_profit.index, rotation=45, ha='right')
axes[0, 1].set_title('Profit by Discount Level', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Profit ($)', fontsize=11)
axes[0, 1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
for i, v in enumerate(discount_profit.values):
    axes[0, 1].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom' if v > 0 else 'top', fontsize=9)

# Profit margin by discount
discount_margin = df.groupby('Discount Bracket', observed=True).apply(lambda x: (x['Profit'].sum() / x['Sales'].sum()) * 100)
colors_margin = ['#06A77D' if x > 0 else '#E63946' for x in discount_margin.values]
axes[1, 0].bar(range(len(discount_margin)), discount_margin.values, color=colors_margin)
axes[1, 0].set_xticks(range(len(discount_margin)))
axes[1, 0].set_xticklabels(discount_margin.index, rotation=45, ha='right')
axes[1, 0].set_title('Profit Margin by Discount Level', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Profit Margin (%)', fontsize=11)
axes[1, 0].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
for i, v in enumerate(discount_margin.values):
    axes[1, 0].text(i, v, f'{v:.1f}%', ha='center', va='bottom' if v > 0 else 'top', fontsize=9)

# Order count by discount
discount_orders = df.groupby('Discount Bracket', observed=True)['Order ID'].count()
axes[1, 1].bar(range(len(discount_orders)), discount_orders.values, color='#7209B7')
axes[1, 1].set_xticks(range(len(discount_orders)))
axes[1, 1].set_xticklabels(discount_orders.index, rotation=45, ha='right')
axes[1, 1].set_title('Order Count by Discount Level', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('Number of Orders', fontsize=11)
for i, v in enumerate(discount_orders.values):
    axes[1, 1].text(i, v, f'{v:,}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/04_discount_impact.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Discount impact analysis saved")

# 5. Shipping Analysis
print("\n🚚 Creating shipping analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Sales by shipping mode
ship_sales = df.groupby('Ship Mode')['Sales'].sum().sort_values(ascending=False)
axes[0, 0].bar(range(len(ship_sales)), ship_sales.values, color='#FF6B6B')
axes[0, 0].set_xticks(range(len(ship_sales)))
axes[0, 0].set_xticklabels(ship_sales.index, rotation=45, ha='right')
axes[0, 0].set_title('Sales by Shipping Mode', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Sales ($)', fontsize=11)
for i, v in enumerate(ship_sales.values):
    axes[0, 0].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontsize=9)

# Average shipping days by mode
ship_days = df.groupby('Ship Mode')['Shipping Days'].mean().sort_values()
axes[0, 1].barh(ship_days.index, ship_days.values, color='#4ECDC4')
axes[0, 1].set_title('Average Shipping Days by Mode', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Days', fontsize=11)
for i, v in enumerate(ship_days.values):
    axes[0, 1].text(v, i, f' {v:.1f}', va='center', fontsize=10)

# Yearly comparison
yearly_sales = df.groupby('Year')['Sales'].sum()
yearly_profit = df.groupby('Year')['Profit'].sum()
x = range(len(yearly_sales))
width = 0.35
axes[1, 0].bar([i - width/2 for i in x], yearly_sales.values, width, label='Sales', color='#95E1D3')
axes[1, 0].bar([i + width/2 for i in x], yearly_profit.values, width, label='Profit', color='#F38181')
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(yearly_sales.index)
axes[1, 0].set_title('Yearly Sales vs Profit', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Amount ($)', fontsize=11)
axes[1, 0].legend()

# Return rate analysis
return_stats = df.groupby('Returned').agg({'Order ID': 'count', 'Sales': 'sum'})
axes[1, 1].pie(return_stats['Order ID'].values, labels=['Not Returned', 'Returned'], 
               autopct='%1.1f%%', colors=['#06A77D', '#E63946'], startangle=90)
axes[1, 1].set_title('Order Return Rate', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/05_shipping_yearly_returns.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Shipping and yearly analysis saved")

# 6. Product Performance Heatmap
print("\n🔥 Creating product performance heatmap...")
fig, ax = plt.subplots(figsize=(14, 10))

# Create pivot table for heatmap
heatmap_data = df.groupby(['Category', 'Sub-Category'])['Profit'].sum().reset_index()
heatmap_pivot = heatmap_data.pivot(index='Sub-Category', columns='Category', values='Profit')

sns.heatmap(heatmap_pivot, annot=True, fmt='.0f', cmap='RdYlGn', center=0, 
            cbar_kws={'label': 'Profit ($)'}, linewidths=0.5, ax=ax)
ax.set_title('Profit Heatmap: Sub-Category vs Category', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Category', fontsize=12)
ax.set_ylabel('Sub-Category', fontsize=12)

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/06_profit_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Profit heatmap saved")

# 7. Correlation Analysis
print("\n📊 Creating correlation analysis...")
fig, ax = plt.subplots(figsize=(10, 8))

# Select numeric columns for correlation
numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Days']
corr_matrix = df[numeric_cols].corr()

sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={'label': 'Correlation'}, ax=ax)
ax.set_title('Correlation Matrix: Key Metrics', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/07_correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Correlation matrix saved")

# 8. Distribution Analysis
print("\n📈 Creating distribution analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Sales distribution
axes[0, 0].hist(df['Sales'], bins=50, color='#3A86FF', edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Sales Distribution', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Sales ($)', fontsize=11)
axes[0, 0].set_ylabel('Frequency', fontsize=11)
axes[0, 0].axvline(df['Sales'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["Sales"].mean():.2f}')
axes[0, 0].legend()

# Profit distribution
axes[0, 1].hist(df['Profit'], bins=50, color='#06A77D', edgecolor='black', alpha=0.7)
axes[0, 1].set_title('Profit Distribution', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Profit ($)', fontsize=11)
axes[0, 1].set_ylabel('Frequency', fontsize=11)
axes[0, 1].axvline(df['Profit'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${df["Profit"].mean():.2f}')
axes[0, 1].legend()

# Quantity distribution
axes[1, 0].hist(df['Quantity'], bins=30, color='#FB5607', edgecolor='black', alpha=0.7)
axes[1, 0].set_title('Quantity Distribution', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Quantity', fontsize=11)
axes[1, 0].set_ylabel('Frequency', fontsize=11)
axes[1, 0].axvline(df['Quantity'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Quantity"].mean():.2f}')
axes[1, 0].legend()

# Discount distribution
axes[1, 1].hist(df['Discount'], bins=30, color='#8338EC', edgecolor='black', alpha=0.7)
axes[1, 1].set_title('Discount Distribution', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Discount', fontsize=11)
axes[1, 1].set_ylabel('Frequency', fontsize=11)
axes[1, 1].axvline(df['Discount'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Discount"].mean():.2f}')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/08_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Distribution analysis saved")

print("\n" + "=" * 80)
print("✅ ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("=" * 80)
print(f"\nVisualization files saved in: ./blackbox-analysis/visualization/")
print(f"Total charts created: 8")
