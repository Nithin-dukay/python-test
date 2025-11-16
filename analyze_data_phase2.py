import pandas as pd
import numpy as np
import json

print("=" * 80)
print("PHASE 2: Deep Analysis - Patterns and Insights")
print("=" * 80)

# Load data
excel_file = '/vercel/sandbox/uploads/Data (1).xlsx'
orders_df = pd.read_excel(excel_file, sheet_name='Orders')
returns_df = pd.read_excel(excel_file, sheet_name='Returns')
people_df = pd.read_excel(excel_file, sheet_name='People')

# Merge returns with orders
orders_df = orders_df.merge(returns_df, on='Order ID', how='left')
orders_df['Returned'] = orders_df['Returned'].fillna('No')

print("\n✓ Merged returns data with orders")

# Extract time features
orders_df['Year'] = orders_df['Order Date'].dt.year
orders_df['Month'] = orders_df['Order Date'].dt.month
orders_df['Quarter'] = orders_df['Order Date'].dt.quarter
orders_df['DayOfWeek'] = orders_df['Order Date'].dt.day_name()
orders_df['Shipping_Days'] = (orders_df['Ship Date'] - orders_df['Order Date']).dt.days

print("\n" + "=" * 80)
print("CATEGORICAL ANALYSIS")
print("=" * 80)

# Unique values in categorical columns
categorical_cols = ['Ship Mode', 'Segment', 'Region', 'Category', 'Sub-Category']
unique_counts = {}

for col in categorical_cols:
    unique_vals = orders_df[col].value_counts()
    unique_counts[col] = unique_vals.to_dict()
    print(f"\n{col}:")
    for val, count in unique_vals.items():
        print(f"  • {val}: {count:,} ({count/len(orders_df)*100:.1f}%)")

print("\n" + "=" * 80)
print("SALES AND PROFIT ANALYSIS")
print("=" * 80)

# Total metrics
total_sales = orders_df['Sales'].sum()
total_profit = orders_df['Profit'].sum()
total_orders = orders_df['Order ID'].nunique()
total_customers = orders_df['Customer ID'].nunique()
avg_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

print(f"\n📊 Key Metrics:")
print(f"  • Total Sales: ${total_sales:,.2f}")
print(f"  • Total Profit: ${total_profit:,.2f}")
print(f"  • Profit Margin: {profit_margin:.2f}%")
print(f"  • Total Orders: {total_orders:,}")
print(f"  • Total Customers: {total_customers:,}")
print(f"  • Average Order Value: ${avg_order_value:.2f}")

# Sales by Category
print("\n💰 Sales by Category:")
category_sales = orders_df.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).round(2)
category_sales['Profit_Margin_%'] = (category_sales['Profit'] / category_sales['Sales'] * 100).round(2)
category_sales = category_sales.sort_values('Sales', ascending=False)
print(category_sales)

# Sales by Region
print("\n🌎 Sales by Region:")
region_sales = orders_df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).round(2)
region_sales['Profit_Margin_%'] = (region_sales['Profit'] / region_sales['Sales'] * 100).round(2)
region_sales = region_sales.sort_values('Sales', ascending=False)
print(region_sales)

# Sales by Segment
print("\n👥 Sales by Segment:")
segment_sales = orders_df.groupby('Segment').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).round(2)
segment_sales['Profit_Margin_%'] = (segment_sales['Profit'] / segment_sales['Sales'] * 100).round(2)
segment_sales = segment_sales.sort_values('Sales', ascending=False)
print(segment_sales)

print("\n" + "=" * 80)
print("TIME-BASED ANALYSIS")
print("=" * 80)

# Yearly trends
print("\n📅 Sales by Year:")
yearly_sales = orders_df.groupby('Year').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).round(2)
print(yearly_sales)

# Monthly trends
print("\n📆 Top 5 Months by Sales:")
monthly_sales = orders_df.groupby(['Year', 'Month']).agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).round(2).sort_values('Sales', ascending=False).head()
print(monthly_sales)

print("\n" + "=" * 80)
print("PRODUCT ANALYSIS")
print("=" * 80)

# Top products by sales
print("\n🏆 Top 10 Products by Sales:")
top_products = orders_df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2).sort_values('Sales', ascending=False).head(10)
print(top_products)

# Top sub-categories
print("\n📦 Top Sub-Categories by Sales:")
subcat_sales = orders_df.groupby('Sub-Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).round(2).sort_values('Sales', ascending=False).head(10)
print(subcat_sales)

print("\n" + "=" * 80)
print("DISCOUNT ANALYSIS")
print("=" * 80)

# Discount impact
discount_bins = [0, 0.1, 0.2, 0.3, 0.5, 1.0]
discount_labels = ['0-10%', '10-20%', '20-30%', '30-50%', '50%+']
orders_df['Discount_Range'] = pd.cut(orders_df['Discount'], bins=discount_bins, labels=discount_labels, include_lowest=True)

print("\n💸 Impact of Discounts on Profit:")
discount_analysis = orders_df.groupby('Discount_Range').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).round(2)
discount_analysis['Profit_Margin_%'] = (discount_analysis['Profit'] / discount_analysis['Sales'] * 100).round(2)
print(discount_analysis)

print("\n" + "=" * 80)
print("RETURNS ANALYSIS")
print("=" * 80)

# Return rate
return_rate = (orders_df['Returned'] == 'Yes').sum() / len(orders_df) * 100
print(f"\n📦 Return Rate: {return_rate:.2f}%")

# Returns by category
print("\n🔄 Returns by Category:")
returns_by_cat = orders_df[orders_df['Returned'] == 'Yes'].groupby('Category').size().sort_values(ascending=False)
print(returns_by_cat)

# Returns by region
print("\n🔄 Returns by Region:")
returns_by_region = orders_df[orders_df['Returned'] == 'Yes'].groupby('Region').size().sort_values(ascending=False)
print(returns_by_region)

print("\n" + "=" * 80)
print("CUSTOMER ANALYSIS")
print("=" * 80)

# Top customers
print("\n👑 Top 10 Customers by Sales:")
top_customers = orders_df.groupby('Customer Name').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).round(2).sort_values('Sales', ascending=False).head(10)
top_customers.columns = ['Total_Sales', 'Total_Profit', 'Order_Count']
print(top_customers)

# Customer segments
print("\n📊 Customer Segment Performance:")
customer_segment = orders_df.groupby(['Segment', 'Region']).agg({
    'Sales': 'sum',
    'Profit': 'sum'
}).round(2).sort_values('Sales', ascending=False).head(10)
print(customer_segment)

print("\n" + "=" * 80)
print("SHIPPING ANALYSIS")
print("=" * 80)

# Shipping mode analysis
print("\n🚚 Shipping Mode Performance:")
shipping_analysis = orders_df.groupby('Ship Mode').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Shipping_Days': 'mean',
    'Order ID': 'count'
}).round(2)
shipping_analysis.columns = ['Total_Sales', 'Total_Profit', 'Avg_Shipping_Days', 'Order_Count']
print(shipping_analysis)

# Average shipping time
avg_shipping = orders_df['Shipping_Days'].mean()
print(f"\n⏱️ Average Shipping Time: {avg_shipping:.1f} days")

print("\n" + "=" * 80)
print("PROFITABILITY INSIGHTS")
print("=" * 80)

# Profitable vs unprofitable orders
profitable_orders = (orders_df['Profit'] > 0).sum()
unprofitable_orders = (orders_df['Profit'] < 0).sum()
breakeven_orders = (orders_df['Profit'] == 0).sum()

print(f"\n💰 Profitability Breakdown:")
print(f"  • Profitable Orders: {profitable_orders:,} ({profitable_orders/len(orders_df)*100:.1f}%)")
print(f"  • Unprofitable Orders: {unprofitable_orders:,} ({unprofitable_orders/len(orders_df)*100:.1f}%)")
print(f"  • Break-even Orders: {breakeven_orders:,} ({breakeven_orders/len(orders_df)*100:.1f}%)")

# Loss-making products
print("\n⚠️ Top 10 Loss-Making Products:")
loss_products = orders_df.groupby('Product Name')['Profit'].sum().sort_values().head(10)
print(loss_products)

# Save comprehensive insights
insights = {
    "key_metrics": {
        "total_sales": float(total_sales),
        "total_profit": float(total_profit),
        "profit_margin_pct": float(profit_margin),
        "total_orders": int(total_orders),
        "total_customers": int(total_customers),
        "avg_order_value": float(avg_order_value),
        "return_rate_pct": float(return_rate)
    },
    "category_performance": category_sales.to_dict(),
    "region_performance": region_sales.to_dict(),
    "segment_performance": segment_sales.to_dict(),
    "profitability": {
        "profitable_orders": int(profitable_orders),
        "unprofitable_orders": int(unprofitable_orders),
        "breakeven_orders": int(breakeven_orders)
    },
    "shipping": {
        "avg_shipping_days": float(avg_shipping)
    }
}

with open('./data_insights_phase2.json', 'w') as f:
    json.dump(insights, f, indent=2)

print("\n✓ Phase 2 complete! Insights saved to data_insights_phase2.json")
