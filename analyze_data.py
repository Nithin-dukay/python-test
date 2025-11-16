import pandas as pd
import numpy as np
import json
from datetime import datetime

# Phase 1: Load complete file and discover structure
print("=" * 80)
print("PHASE 1: Loading and Understanding Data Structure")
print("=" * 80)

# Load all sheets
excel_file = pd.ExcelFile('/vercel/sandbox/uploads/Data (1).xlsx')
print(f"\nSheets found: {excel_file.sheet_names}")

# Load Orders sheet (main data)
orders_df = pd.read_excel('/vercel/sandbox/uploads/Data (1).xlsx', sheet_name='Orders')
returns_df = pd.read_excel('/vercel/sandbox/uploads/Data (1).xlsx', sheet_name='Returns')
people_df = pd.read_excel('/vercel/sandbox/uploads/Data (1).xlsx', sheet_name='People')

print(f"\n✓ Orders: {len(orders_df)} rows, {len(orders_df.columns)} columns")
print(f"✓ Returns: {len(returns_df)} rows, {len(returns_df.columns)} columns")
print(f"✓ People: {len(people_df)} rows, {len(people_df.columns)} columns")

# Display column information
print("\n" + "=" * 80)
print("ORDERS DATASET STRUCTURE")
print("=" * 80)
print("\nColumns and Data Types:")
for col in orders_df.columns:
    dtype = orders_df[col].dtype
    null_count = orders_df[col].isnull().sum()
    print(f"  • {col:25s} | Type: {str(dtype):15s} | Nulls: {null_count}")

# Convert date columns
orders_df['Order Date'] = pd.to_datetime(orders_df['Order Date'])
orders_df['Ship Date'] = pd.to_datetime(orders_df['Ship Date'])

# Basic statistics
print("\n" + "=" * 80)
print("BASIC STATISTICS")
print("=" * 80)
print(f"\nDate Range: {orders_df['Order Date'].min().date()} to {orders_df['Order Date'].max().date()}")
print(f"Total Orders: {orders_df['Order ID'].nunique()}")
print(f"Total Customers: {orders_df['Customer ID'].nunique()}")
print(f"Total Products: {orders_df['Product ID'].nunique()}")

# Save Phase 1 insights
phase1_insights = {
    "total_rows": len(orders_df),
    "total_orders": int(orders_df['Order ID'].nunique()),
    "total_customers": int(orders_df['Customer ID'].nunique()),
    "total_products": int(orders_df['Product ID'].nunique()),
    "date_range": {
        "start": str(orders_df['Order Date'].min().date()),
        "end": str(orders_df['Order Date'].max().date())
    },
    "columns": list(orders_df.columns),
    "data_types": {col: str(dtype) for col, dtype in orders_df.dtypes.items()}
}

with open('/vercel/sandbox/phase1_insights.json', 'w') as f:
    json.dump(phase1_insights, f, indent=2)

print("\n✓ Phase 1 complete. Insights saved to phase1_insights.json")

# Phase 2: Deep Analysis
print("\n" + "=" * 80)
print("PHASE 2: Deep Analysis - Statistics and Patterns")
print("=" * 80)

# Merge returns data
orders_df = orders_df.merge(returns_df, on='Order ID', how='left')
orders_df['Returned'] = orders_df['Returned'].fillna('No')

# Calculate additional metrics
orders_df['Profit Margin'] = (orders_df['Profit'] / orders_df['Sales']) * 100
orders_df['Year'] = orders_df['Order Date'].dt.year
orders_df['Month'] = orders_df['Order Date'].dt.month
orders_df['Quarter'] = orders_df['Order Date'].dt.quarter
orders_df['Shipping Days'] = (orders_df['Ship Date'] - orders_df['Order Date']).dt.days

# Overall metrics
print("\n📊 OVERALL BUSINESS METRICS")
print("-" * 80)
total_sales = orders_df['Sales'].sum()
total_profit = orders_df['Profit'].sum()
avg_profit_margin = orders_df['Profit Margin'].mean()
total_quantity = orders_df['Quantity'].sum()
return_rate = (len(orders_df[orders_df['Returned'] == 'Yes']) / len(orders_df)) * 100

print(f"Total Sales:           ${total_sales:,.2f}")
print(f"Total Profit:          ${total_profit:,.2f}")
print(f"Average Profit Margin: {avg_profit_margin:.2f}%")
print(f"Total Quantity Sold:   {total_quantity:,}")
print(f"Return Rate:           {return_rate:.2f}%")
print(f"Average Order Value:   ${orders_df.groupby('Order ID')['Sales'].sum().mean():,.2f}")

# Category analysis
print("\n📦 CATEGORY PERFORMANCE")
print("-" * 80)
category_stats = orders_df.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Order ID': 'count'
}).round(2)
category_stats['Profit Margin %'] = (category_stats['Profit'] / category_stats['Sales'] * 100).round(2)
category_stats = category_stats.sort_values('Sales', ascending=False)
print(category_stats)

# Sub-category analysis
print("\n📋 TOP 10 SUB-CATEGORIES BY SALES")
print("-" * 80)
subcat_stats = orders_df.groupby('Sub-Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)
subcat_stats['Profit Margin %'] = (subcat_stats['Profit'] / subcat_stats['Sales'] * 100).round(2)
subcat_stats = subcat_stats.sort_values('Sales', ascending=False).head(10)
print(subcat_stats)

# Regional analysis
print("\n🌎 REGIONAL PERFORMANCE")
print("-" * 80)
region_stats = orders_df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Customer ID': 'nunique'
}).round(2)
region_stats['Profit Margin %'] = (region_stats['Profit'] / region_stats['Sales'] * 100).round(2)
region_stats = region_stats.sort_values('Sales', ascending=False)
print(region_stats)

# Customer segment analysis
print("\n👥 CUSTOMER SEGMENT ANALYSIS")
print("-" * 80)
segment_stats = orders_df.groupby('Segment').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Customer ID': 'nunique'
}).round(2)
segment_stats['Profit Margin %'] = (segment_stats['Profit'] / segment_stats['Sales'] * 100).round(2)
segment_stats = segment_stats.sort_values('Sales', ascending=False)
print(segment_stats)

# Shipping mode analysis
print("\n🚚 SHIPPING MODE ANALYSIS")
print("-" * 80)
ship_stats = orders_df.groupby('Ship Mode').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Shipping Days': 'mean',
    'Order ID': 'count'
}).round(2)
ship_stats = ship_stats.sort_values('Sales', ascending=False)
print(ship_stats)

# Discount analysis
print("\n💰 DISCOUNT IMPACT ANALYSIS")
print("-" * 80)
orders_df['Discount Bracket'] = pd.cut(orders_df['Discount'], 
                                        bins=[-0.01, 0, 0.1, 0.2, 0.3, 1.0],
                                        labels=['No Discount', '0-10%', '10-20%', '20-30%', '30%+'])
discount_stats = orders_df.groupby('Discount Bracket').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Order ID': 'count'
}).round(2)
discount_stats['Profit Margin %'] = (discount_stats['Profit'] / discount_stats['Sales'] * 100).round(2)
print(discount_stats)

# Save Phase 2 insights
phase2_insights = {
    "overall_metrics": {
        "total_sales": float(total_sales),
        "total_profit": float(total_profit),
        "avg_profit_margin": float(avg_profit_margin),
        "total_quantity": int(total_quantity),
        "return_rate": float(return_rate)
    },
    "category_performance": category_stats.to_dict(),
    "top_subcategories": subcat_stats.to_dict(),
    "regional_performance": region_stats.to_dict(),
    "segment_performance": segment_stats.to_dict(),
    "shipping_analysis": ship_stats.to_dict(),
    "discount_impact": discount_stats.to_dict()
}

with open('/vercel/sandbox/phase2_insights.json', 'w') as f:
    json.dump(phase2_insights, f, indent=2)

print("\n✓ Phase 2 complete. Insights saved to phase2_insights.json")

# Phase 3: Time Series and Trend Analysis
print("\n" + "=" * 80)
print("PHASE 3: Time Series and Trend Analysis")
print("=" * 80)

# Yearly trends
print("\n📈 YEARLY TRENDS")
print("-" * 80)
yearly_stats = orders_df.groupby('Year').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'Order ID': 'nunique'
}).round(2)
yearly_stats['Profit Margin %'] = (yearly_stats['Profit'] / yearly_stats['Sales'] * 100).round(2)
yearly_stats['YoY Sales Growth %'] = yearly_stats['Sales'].pct_change() * 100
print(yearly_stats)

# Monthly trends
monthly_stats = orders_df.groupby(['Year', 'Month']).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)

# Best and worst months
print("\n🏆 BEST PERFORMING MONTHS")
print("-" * 80)
best_months = monthly_stats.nlargest(5, 'Sales')
print(best_months)

print("\n⚠️ WORST PERFORMING MONTHS")
print("-" * 80)
worst_months = monthly_stats.nsmallest(5, 'Sales')
print(worst_months)

# Top customers
print("\n👑 TOP 10 CUSTOMERS BY SALES")
print("-" * 80)
customer_stats = orders_df.groupby(['Customer ID', 'Customer Name']).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique',
    'Quantity': 'sum'
}).round(2)
customer_stats = customer_stats.sort_values('Sales', ascending=False).head(10)
print(customer_stats)

# Top products
print("\n🌟 TOP 10 PRODUCTS BY SALES")
print("-" * 80)
product_stats = orders_df.groupby(['Product ID', 'Product Name']).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)
product_stats['Profit Margin %'] = (product_stats['Profit'] / product_stats['Sales'] * 100).round(2)
top_products = product_stats.sort_values('Sales', ascending=False).head(10)
print(top_products)

# Loss-making products
print("\n⚠️ TOP 10 LOSS-MAKING PRODUCTS")
print("-" * 80)
loss_products = product_stats[product_stats['Profit'] < 0].sort_values('Profit').head(10)
print(loss_products)

# State analysis
print("\n🗺️ TOP 10 STATES BY SALES")
print("-" * 80)
state_stats = orders_df.groupby('State').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Customer ID': 'nunique'
}).round(2)
state_stats['Profit Margin %'] = (state_stats['Profit'] / state_stats['Sales'] * 100).round(2)
top_states = state_stats.sort_values('Sales', ascending=False).head(10)
print(top_states)

# Save Phase 3 insights (convert to JSON-serializable format)
phase3_insights = {
    "yearly_trends": yearly_stats.reset_index().to_dict('records'),
    "best_months": best_months.reset_index().to_dict('records'),
    "worst_months": worst_months.reset_index().to_dict('records'),
    "top_customers": customer_stats.reset_index().to_dict('records'),
    "top_products": top_products.reset_index().to_dict('records'),
    "loss_making_products": loss_products.reset_index().to_dict('records'),
    "top_states": top_states.reset_index().to_dict('records')
}

with open('/vercel/sandbox/phase3_insights.json', 'w') as f:
    json.dump(phase3_insights, f, indent=2)

print("\n✓ Phase 3 complete. Insights saved to phase3_insights.json")

# Save the processed dataframe for visualization
print("\n💾 Saving processed data for visualization...")
orders_df.to_csv('/vercel/sandbox/processed_orders.csv', index=False)
print("✓ Processed data saved to processed_orders.csv")
