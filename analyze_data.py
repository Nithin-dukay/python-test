import pandas as pd
import numpy as np
import json
import os

# Create output directory
os.makedirs('./data_insights', exist_ok=True)

print("=" * 80)
print("PHASE 1: Loading and Understanding Data Structure")
print("=" * 80)

# Load all sheets
excel_file = '/vercel/sandbox/uploads/Data (1).xlsx'
orders_df = pd.read_excel(excel_file, sheet_name='Orders')
returns_df = pd.read_excel(excel_file, sheet_name='Returns')
people_df = pd.read_excel(excel_file, sheet_name='People')

print(f"\n✓ Loaded Orders: {len(orders_df)} rows, {len(orders_df.columns)} columns")
print(f"✓ Loaded Returns: {len(returns_df)} rows, {len(returns_df.columns)} columns")
print(f"✓ Loaded People: {len(people_df)} rows, {len(people_df.columns)} columns")

# Display column information
print("\n" + "=" * 80)
print("ORDERS DATASET STRUCTURE")
print("=" * 80)
print("\nColumns and Data Types:")
for col in orders_df.columns:
    print(f"  • {col}: {orders_df[col].dtype}")

print("\n" + "=" * 80)
print("DATA QUALITY CHECK")
print("=" * 80)

# Check for missing values
print("\nMissing Values:")
missing = orders_df.isnull().sum()
if missing.sum() > 0:
    print(missing[missing > 0])
else:
    print("  ✓ No missing values found!")

# Check for duplicates
duplicates = orders_df.duplicated().sum()
print(f"\nDuplicate Rows: {duplicates}")

# Basic statistics
print("\n" + "=" * 80)
print("BASIC STATISTICS")
print("=" * 80)

print("\nNumerical Columns Summary:")
print(orders_df[['Sales', 'Quantity', 'Discount', 'Profit']].describe())

# Save initial insights
initial_insights = {
    "dataset_info": {
        "total_orders": len(orders_df),
        "total_returns": len(returns_df),
        "total_people": len(people_df),
        "date_range": {
            "start": str(orders_df['Order Date'].min()),
            "end": str(orders_df['Order Date'].max())
        },
        "columns": list(orders_df.columns)
    },
    "data_quality": {
        "missing_values": int(missing.sum()),
        "duplicate_rows": int(duplicates)
    }
}

with open('./data_insights_phase1.json', 'w') as f:
    json.dump(initial_insights, f, indent=2)

print("\n✓ Phase 1 complete! Insights saved to data_insights_phase1.json")
