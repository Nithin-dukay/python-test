import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')

# Load data
excel_file = '/vercel/sandbox/uploads/Data (1).xlsx'
orders_df = pd.read_excel(excel_file, sheet_name='Orders')
orders_df['Year'] = orders_df['Order Date'].dt.year

print("Creating Chart 8: Yearly Comparison...")

# Create a new figure with proper size
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# 8.1 Sales by Year
ax1 = fig.add_subplot(gs[0, 0])
yearly_sales = orders_df.groupby('Year')['Sales'].sum()
ax1.bar(yearly_sales.index.astype(str), yearly_sales.values, color=sns.color_palette('Blues', 4), alpha=0.8)
ax1.set_title('Total Sales by Year', fontsize=14, fontweight='bold')
ax1.set_ylabel('Sales ($)', fontsize=12)
ax1.set_xlabel('Year', fontsize=12)
for i, (year, v) in enumerate(yearly_sales.items()):
    ax1.text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

# 8.2 Profit by Year
ax2 = fig.add_subplot(gs[0, 1])
yearly_profit = orders_df.groupby('Year')['Profit'].sum()
ax2.bar(yearly_profit.index.astype(str), yearly_profit.values, color=sns.color_palette('Greens', 4), alpha=0.8)
ax2.set_title('Total Profit by Year', fontsize=14, fontweight='bold')
ax2.set_ylabel('Profit ($)', fontsize=12)
ax2.set_xlabel('Year', fontsize=12)
for i, (year, v) in enumerate(yearly_profit.items()):
    ax2.text(i, v, f'${v/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

# 8.3 Orders by Year
ax3 = fig.add_subplot(gs[1, 0])
yearly_orders = orders_df.groupby('Year')['Order ID'].count()
ax3.bar(yearly_orders.index.astype(str), yearly_orders.values, color=sns.color_palette('Oranges', 4), alpha=0.8)
ax3.set_title('Total Orders by Year', fontsize=14, fontweight='bold')
ax3.set_ylabel('Number of Orders', fontsize=12)
ax3.set_xlabel('Year', fontsize=12)
for i, (year, v) in enumerate(yearly_orders.items()):
    ax3.text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold')

# 8.4 Growth Rate
ax4 = fig.add_subplot(gs[1, 1])
growth_data = pd.DataFrame({
    'Sales_Growth': yearly_sales.pct_change() * 100,
    'Profit_Growth': yearly_profit.pct_change() * 100
}).dropna()

years = [str(y) for y in growth_data.index]
x_pos = list(range(len(years)))
width = 0.35

ax4.bar([i - width/2 for i in x_pos], growth_data['Sales_Growth'].values, width, label='Sales Growth', color='#3498DB', alpha=0.8)
ax4.bar([i + width/2 for i in x_pos], growth_data['Profit_Growth'].values, width, label='Profit Growth', color='#2ECC71', alpha=0.8)
ax4.set_title('Year-over-Year Growth Rate', fontsize=14, fontweight='bold')
ax4.set_ylabel('Growth Rate (%)', fontsize=12)
ax4.set_xlabel('Year', fontsize=12)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(years)
ax4.legend()
ax4.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax4.grid(True, alpha=0.3, axis='y')

fig.suptitle('Year-over-Year Performance Comparison', fontsize=20, fontweight='bold', y=0.995)

plt.savefig('./blackbox-analysis/visualization/08_yearly_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 08_yearly_comparison.png")
