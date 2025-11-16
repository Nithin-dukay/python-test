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
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['font.size'] = 10

# Create directories
os.makedirs('./blackbox-analysis/visualization/', exist_ok=True)
os.makedirs('./blackbox-analysis/pdfs/', exist_ok=True)

print("=" * 80)
print("CREATING COMPREHENSIVE VISUALIZATIONS")
print("=" * 80)

# Load data
excel_file = '/vercel/sandbox/uploads/Data (1).xlsx'
orders_df = pd.read_excel(excel_file, sheet_name='Orders')
returns_df = pd.read_excel(excel_file, sheet_name='Returns')

# Merge returns
orders_df = orders_df.merge(returns_df, on='Order ID', how='left')
orders_df['Returned'] = orders_df['Returned'].fillna('No')
orders_df['Year'] = orders_df['Order Date'].dt.year
orders_df['Month'] = orders_df['Order Date'].dt.month
orders_df['YearMonth'] = orders_df['Order Date'].dt.to_period('M').astype(str)

print("\n✓ Data loaded and prepared")

# ============================================================================
# CHART 1: Sales and Profit Overview Dashboard
# ============================================================================
print("\n📊 Creating Chart 1: Sales and Profit Overview...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Sales and Profit Overview Dashboard', fontsize=20, fontweight='bold', y=0.995)

# 1.1 Sales by Category
category_data = orders_df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values('Sales', ascending=False)
axes[0, 0].bar(category_data.index, category_data['Sales'], color=['#2E86AB', '#A23B72', '#F18F01'], alpha=0.8)
axes[0, 0].set_title('Total Sales by Category', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Sales ($)', fontsize=12)
axes[0, 0].tick_params(axis='x', rotation=0)
for i, v in enumerate(category_data['Sales']):
    axes[0, 0].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

# 1.2 Profit by Category
axes[0, 1].bar(category_data.index, category_data['Profit'], color=['#06A77D', '#D4AF37', '#C73E1D'], alpha=0.8)
axes[0, 1].set_title('Total Profit by Category', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Profit ($)', fontsize=12)
axes[0, 1].tick_params(axis='x', rotation=0)
for i, v in enumerate(category_data['Profit']):
    axes[0, 1].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

# 1.3 Sales by Region
region_data = orders_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
colors_region = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
axes[1, 0].barh(region_data.index, region_data.values, color=colors_region, alpha=0.8)
axes[1, 0].set_title('Total Sales by Region', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Sales ($)', fontsize=12)
for i, v in enumerate(region_data.values):
    axes[1, 0].text(v, i, f'  ${v/1000:.0f}K', va='center', fontweight='bold')

# 1.4 Sales by Segment
segment_data = orders_df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
colors_segment = ['#9B59B6', '#3498DB', '#E74C3C']
axes[1, 1].barh(segment_data.index, segment_data.values, color=colors_segment, alpha=0.8)
axes[1, 1].set_title('Total Sales by Segment', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Sales ($)', fontsize=12)
for i, v in enumerate(segment_data.values):
    axes[1, 1].text(v, i, f'  ${v/1000:.0f}K', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/01_sales_profit_overview.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 01_sales_profit_overview.png")

# ============================================================================
# CHART 2: Time Series Analysis
# ============================================================================
print("\n📈 Creating Chart 2: Time Series Analysis...")

fig, axes = plt.subplots(2, 1, figsize=(16, 10))
fig.suptitle('Sales and Profit Trends Over Time', fontsize=20, fontweight='bold')

# 2.1 Monthly Sales Trend
monthly_data = orders_df.groupby('YearMonth').agg({'Sales': 'sum', 'Profit': 'sum'})
axes[0].plot(range(len(monthly_data)), monthly_data['Sales'], marker='o', linewidth=2, color='#2E86AB', label='Sales')
axes[0].fill_between(range(len(monthly_data)), monthly_data['Sales'], alpha=0.3, color='#2E86AB')
axes[0].set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Sales ($)', fontsize=12)
axes[0].set_xlabel('Time Period', fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].legend()

# 2.2 Monthly Profit Trend
axes[1].plot(range(len(monthly_data)), monthly_data['Profit'], marker='o', linewidth=2, color='#06A77D', label='Profit')
axes[1].fill_between(range(len(monthly_data)), monthly_data['Profit'], alpha=0.3, color='#06A77D')
axes[1].set_title('Monthly Profit Trend', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Profit ($)', fontsize=12)
axes[1].set_xlabel('Time Period', fontsize=12)
axes[1].grid(True, alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/02_time_series_trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 02_time_series_trends.png")

# ============================================================================
# CHART 3: Product Performance
# ============================================================================
print("\n📦 Creating Chart 3: Product Performance...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Product Performance Analysis', fontsize=20, fontweight='bold', y=0.995)

# 3.1 Top 10 Sub-Categories by Sales
subcat_sales = orders_df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
axes[0, 0].barh(subcat_sales.index, subcat_sales.values, color=sns.color_palette('viridis', 10), alpha=0.8)
axes[0, 0].set_title('Top 10 Sub-Categories by Sales', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Sales ($)', fontsize=12)
axes[0, 0].invert_yaxis()

# 3.2 Top 10 Products by Sales
top_products = orders_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
product_names_short = [name[:30] + '...' if len(name) > 30 else name for name in top_products.index]
axes[0, 1].barh(product_names_short, top_products.values, color=sns.color_palette('plasma', 10), alpha=0.8)
axes[0, 1].set_title('Top 10 Products by Sales', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Sales ($)', fontsize=12)
axes[0, 1].invert_yaxis()

# 3.3 Profit by Sub-Category
subcat_profit = orders_df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False).head(10)
colors = ['green' if x > 0 else 'red' for x in subcat_profit.values]
axes[1, 0].barh(subcat_profit.index, subcat_profit.values, color=colors, alpha=0.7)
axes[1, 0].set_title('Top 10 Sub-Categories by Profit', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Profit ($)', fontsize=12)
axes[1, 0].axvline(x=0, color='black', linestyle='--', linewidth=1)
axes[1, 0].invert_yaxis()

# 3.4 Quantity Sold by Category
quantity_data = orders_df.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
axes[1, 1].bar(quantity_data.index, quantity_data.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
axes[1, 1].set_title('Total Quantity Sold by Category', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('Quantity', fontsize=12)
for i, v in enumerate(quantity_data.values):
    axes[1, 1].text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/03_product_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 03_product_performance.png")

# ============================================================================
# CHART 4: Discount Impact Analysis
# ============================================================================
print("\n💸 Creating Chart 4: Discount Impact Analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Discount Impact on Sales and Profitability', fontsize=20, fontweight='bold', y=0.995)

# 4.1 Discount Distribution
axes[0, 0].hist(orders_df['Discount'], bins=20, color='#3498DB', alpha=0.7, edgecolor='black')
axes[0, 0].set_title('Distribution of Discounts', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Discount Rate', fontsize=12)
axes[0, 0].set_ylabel('Frequency', fontsize=12)

# 4.2 Sales vs Discount
discount_bins = [0, 0.1, 0.2, 0.3, 0.5, 1.0]
discount_labels = ['0-10%', '10-20%', '20-30%', '30-50%', '50%+']
orders_df['Discount_Range'] = pd.cut(orders_df['Discount'], bins=discount_bins, labels=discount_labels, include_lowest=True)
discount_sales = orders_df.groupby('Discount_Range', observed=True)['Sales'].sum()
axes[0, 1].bar(discount_sales.index, discount_sales.values, color=sns.color_palette('RdYlGn_r', 5), alpha=0.8)
axes[0, 1].set_title('Sales by Discount Range', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Sales ($)', fontsize=12)
axes[0, 1].tick_params(axis='x', rotation=45)

# 4.3 Profit vs Discount
discount_profit = orders_df.groupby('Discount_Range', observed=True)['Profit'].sum()
colors = ['green' if x > 0 else 'red' for x in discount_profit.values]
axes[1, 0].bar(discount_profit.index, discount_profit.values, color=colors, alpha=0.7)
axes[1, 0].set_title('Profit by Discount Range', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Profit ($)', fontsize=12)
axes[1, 0].axhline(y=0, color='black', linestyle='--', linewidth=1)
axes[1, 0].tick_params(axis='x', rotation=45)

# 4.4 Profit Margin by Discount
discount_analysis = orders_df.groupby('Discount_Range', observed=True).agg({'Sales': 'sum', 'Profit': 'sum'})
discount_analysis['Profit_Margin'] = (discount_analysis['Profit'] / discount_analysis['Sales'] * 100)
axes[1, 1].plot(discount_analysis.index, discount_analysis['Profit_Margin'], marker='o', linewidth=2, markersize=10, color='#E74C3C')
axes[1, 1].set_title('Profit Margin by Discount Range', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('Profit Margin (%)', fontsize=12)
axes[1, 1].axhline(y=0, color='black', linestyle='--', linewidth=1)
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/04_discount_impact.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 04_discount_impact.png")

# ============================================================================
# CHART 5: Customer and Geographic Analysis
# ============================================================================
print("\n🌍 Creating Chart 5: Customer and Geographic Analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Customer and Geographic Analysis', fontsize=20, fontweight='bold', y=0.995)

# 5.1 Top 10 States by Sales
state_sales = orders_df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10)
axes[0, 0].barh(state_sales.index, state_sales.values, color=sns.color_palette('coolwarm', 10), alpha=0.8)
axes[0, 0].set_title('Top 10 States by Sales', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Sales ($)', fontsize=12)
axes[0, 0].invert_yaxis()

# 5.2 Top 10 Cities by Sales
city_sales = orders_df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10)
axes[0, 1].barh(city_sales.index, city_sales.values, color=sns.color_palette('viridis', 10), alpha=0.8)
axes[0, 1].set_title('Top 10 Cities by Sales', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Sales ($)', fontsize=12)
axes[0, 1].invert_yaxis()

# 5.3 Top 10 Customers by Sales
customer_sales = orders_df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)
axes[1, 0].barh(customer_sales.index, customer_sales.values, color=sns.color_palette('plasma', 10), alpha=0.8)
axes[1, 0].set_title('Top 10 Customers by Sales', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Sales ($)', fontsize=12)
axes[1, 0].invert_yaxis()

# 5.4 Segment Distribution
segment_counts = orders_df['Segment'].value_counts()
colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1']
axes[1, 1].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%', 
               colors=colors_pie, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[1, 1].set_title('Customer Segment Distribution', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/05_customer_geographic.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 05_customer_geographic.png")

# ============================================================================
# CHART 6: Shipping and Returns Analysis
# ============================================================================
print("\n🚚 Creating Chart 6: Shipping and Returns Analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Shipping and Returns Analysis', fontsize=20, fontweight='bold', y=0.995)

# 6.1 Shipping Mode Distribution
ship_mode_data = orders_df.groupby('Ship Mode').agg({'Sales': 'sum', 'Order ID': 'count'})
axes[0, 0].bar(ship_mode_data.index, ship_mode_data['Order ID'], color=['#2E86AB', '#A23B72', '#F18F01', '#06A77D'], alpha=0.8)
axes[0, 0].set_title('Orders by Shipping Mode', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Number of Orders', fontsize=12)
axes[0, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(ship_mode_data['Order ID']):
    axes[0, 0].text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold')

# 6.2 Sales by Shipping Mode
axes[0, 1].bar(ship_mode_data.index, ship_mode_data['Sales'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'], alpha=0.8)
axes[0, 1].set_title('Sales by Shipping Mode', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Sales ($)', fontsize=12)
axes[0, 1].tick_params(axis='x', rotation=45)

# 6.3 Return Rate by Category
returns_by_cat = orders_df[orders_df['Returned'] == 'Yes'].groupby('Category').size()
total_by_cat = orders_df.groupby('Category').size()
return_rate_cat = (returns_by_cat / total_by_cat * 100).sort_values(ascending=False)
axes[1, 0].bar(return_rate_cat.index, return_rate_cat.values, color=['#E74C3C', '#F39C12', '#27AE60'], alpha=0.8)
axes[1, 0].set_title('Return Rate by Category', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Return Rate (%)', fontsize=12)
for i, v in enumerate(return_rate_cat.values):
    axes[1, 0].text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')

# 6.4 Return Rate by Region
returns_by_region = orders_df[orders_df['Returned'] == 'Yes'].groupby('Region').size()
total_by_region = orders_df.groupby('Region').size()
return_rate_region = (returns_by_region / total_by_region * 100).sort_values(ascending=False)
axes[1, 1].barh(return_rate_region.index, return_rate_region.values, color=sns.color_palette('Reds_r', 4), alpha=0.8)
axes[1, 1].set_title('Return Rate by Region', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Return Rate (%)', fontsize=12)
axes[1, 1].invert_yaxis()
for i, v in enumerate(return_rate_region.values):
    axes[1, 1].text(v, i, f'  {v:.1f}%', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/06_shipping_returns.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 06_shipping_returns.png")

# ============================================================================
# CHART 7: Profitability Analysis
# ============================================================================
print("\n💰 Creating Chart 7: Profitability Analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Profitability Analysis', fontsize=20, fontweight='bold', y=0.995)

# 7.1 Profit Margin by Category
category_analysis = orders_df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'})
category_analysis['Profit_Margin'] = (category_analysis['Profit'] / category_analysis['Sales'] * 100)
axes[0, 0].bar(category_analysis.index, category_analysis['Profit_Margin'], 
               color=['#06A77D', '#F18F01', '#2E86AB'], alpha=0.8)
axes[0, 0].set_title('Profit Margin by Category', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Profit Margin (%)', fontsize=12)
for i, v in enumerate(category_analysis['Profit_Margin']):
    axes[0, 0].text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')

# 7.2 Profit Distribution
profitable = (orders_df['Profit'] > 0).sum()
unprofitable = (orders_df['Profit'] < 0).sum()
breakeven = (orders_df['Profit'] == 0).sum()
profit_dist = pd.Series([profitable, unprofitable, breakeven], index=['Profitable', 'Unprofitable', 'Break-even'])
colors_profit = ['#27AE60', '#E74C3C', '#95A5A6']
axes[0, 1].pie(profit_dist.values, labels=profit_dist.index, autopct='%1.1f%%', 
               colors=colors_profit, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[0, 1].set_title('Order Profitability Distribution', fontsize=14, fontweight='bold')

# 7.3 Top 10 Most Profitable Products
product_profit = orders_df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
product_names_short = [name[:30] + '...' if len(name) > 30 else name for name in product_profit.index]
axes[1, 0].barh(product_names_short, product_profit.values, color=sns.color_palette('Greens', 10), alpha=0.8)
axes[1, 0].set_title('Top 10 Most Profitable Products', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Profit ($)', fontsize=12)
axes[1, 0].invert_yaxis()

# 7.4 Top 10 Loss-Making Products
loss_products = orders_df.groupby('Product Name')['Profit'].sum().sort_values().head(10)
loss_names_short = [name[:30] + '...' if len(name) > 30 else name for name in loss_products.index]
axes[1, 1].barh(loss_names_short, loss_products.values, color=sns.color_palette('Reds', 10), alpha=0.8)
axes[1, 1].set_title('Top 10 Loss-Making Products', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Loss ($)', fontsize=12)
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/07_profitability_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 07_profitability_analysis.png")

# ============================================================================
# CHART 8: Yearly Comparison
# ============================================================================
print("\n📅 Creating Chart 8: Yearly Comparison...")

plt.close('all')  # Close any existing figures
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Year-over-Year Performance Comparison', fontsize=20, fontweight='bold', y=0.995)

# 8.1 Sales by Year
yearly_sales = orders_df.groupby('Year')['Sales'].sum()
axes[0, 0].bar(yearly_sales.index, yearly_sales.values, color=sns.color_palette('Blues', 4), alpha=0.8)
axes[0, 0].set_title('Total Sales by Year', fontsize=14, fontweight='bold')
axes[0, 0].set_ylabel('Sales ($)', fontsize=12)
axes[0, 0].set_xlabel('Year', fontsize=12)
for i, v in enumerate(yearly_sales.values):
    axes[0, 0].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

# 8.2 Profit by Year
yearly_profit = orders_df.groupby('Year')['Profit'].sum()
axes[0, 1].bar(yearly_profit.index, yearly_profit.values, color=sns.color_palette('Greens', 4), alpha=0.8)
axes[0, 1].set_title('Total Profit by Year', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Profit ($)', fontsize=12)
axes[0, 1].set_xlabel('Year', fontsize=12)
for i, v in enumerate(yearly_profit.values):
    axes[0, 1].text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

# 8.3 Orders by Year
yearly_orders = orders_df.groupby('Year')['Order ID'].count()
axes[1, 0].bar(yearly_orders.index, yearly_orders.values, color=sns.color_palette('Oranges', 4), alpha=0.8)
axes[1, 0].set_title('Total Orders by Year', fontsize=14, fontweight='bold')
axes[1, 0].set_ylabel('Number of Orders', fontsize=12)
axes[1, 0].set_xlabel('Year', fontsize=12)
for i, v in enumerate(yearly_orders.values):
    axes[1, 0].text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold')

# 8.4 Growth Rate
growth_data = pd.DataFrame({
    'Sales_Growth': yearly_sales.pct_change() * 100,
    'Profit_Growth': yearly_profit.pct_change() * 100
}).dropna()
x_pos = list(range(len(growth_data)))
width = 0.35
x1 = [i - width/2 for i in x_pos]
x2 = [i + width/2 for i in x_pos]
axes[1, 1].bar(x1, growth_data['Sales_Growth'], width, label='Sales Growth', color='#3498DB', alpha=0.8)
axes[1, 1].bar(x2, growth_data['Profit_Growth'], width, label='Profit Growth', color='#2ECC71', alpha=0.8)
axes[1, 1].set_title('Year-over-Year Growth Rate', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('Growth Rate (%)', fontsize=12)
axes[1, 1].set_xlabel('Year', fontsize=12)
axes[1, 1].set_xticks(x_pos)
axes[1, 1].set_xticklabels([str(year) for year in growth_data.index])
axes[1, 1].legend()
axes[1, 1].axhline(y=0, color='black', linestyle='--', linewidth=1)
axes[1, 1].grid(True, alpha=0.3, axis='y')

try:
    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/08_yearly_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Saved: 08_yearly_comparison.png")
except Exception as e:
    print(f"  ⚠ Error saving chart 8: {e}")
    plt.close()

print("\n" + "=" * 80)
print("✅ ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("=" * 80)
print(f"\n📁 Visualizations saved to: ./blackbox-analysis/visualization/")
print(f"   Total charts created: 8")
