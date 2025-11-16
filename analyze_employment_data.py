"""
Employment Data Analysis Script
Comprehensive analysis of Business Data Collection employment data
"""

import pandas as pd
import numpy as np
import os
import json
from collections import Counter

# Create output directories
os.makedirs('./blackbox-analysis/visualization/', exist_ok=True)
os.makedirs('./blackbox-analysis/pdfs/', exist_ok=True)

print("=" * 80)
print("PHASE 1: LOADING AND UNDERSTANDING DATA STRUCTURE")
print("=" * 80)

# Load the complete dataset
df = pd.read_csv('/vercel/sandbox/uploads/employment-data.csv')

print(f"\n📊 Dataset Overview:")
print(f"   Total Rows: {len(df):,}")
print(f"   Total Columns: {len(df.columns)}")
print(f"   Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

print(f"\n📋 Column Names and Types:")
for col in df.columns:
    print(f"   - {col}: {df[col].dtype}")

print(f"\n🔍 Data Quality Check:")
print(f"   Missing Values per Column:")
for col in df.columns:
    missing = df[col].isna().sum()
    missing_pct = (missing / len(df)) * 100
    print(f"   - {col}: {missing:,} ({missing_pct:.2f}%)")

print(f"\n📅 Time Period Coverage:")
df['Period'] = pd.to_numeric(df['Period'], errors='coerce')
print(f"   Start Period: {df['Period'].min()}")
print(f"   End Period: {df['Period'].max()}")
print(f"   Unique Periods: {df['Period'].nunique()}")

# Convert Period to datetime for better analysis
df['Year'] = df['Period'].apply(lambda x: int(x) if pd.notna(x) else None)
df['Quarter'] = df['Period'].apply(lambda x: int((x % 1) * 100) if pd.notna(x) else None)

print(f"\n📊 Data Categories:")
print(f"   Unique Series References: {df['Series_reference'].nunique()}")
print(f"   Unique Groups: {df['Group'].nunique()}")
print(f"   Unique Series Title 1: {df['Series_title_1'].nunique()}")
print(f"   Unique Series Title 2: {df['Series_title_2'].nunique()}")
print(f"   Unique Series Title 3: {df['Series_title_3'].nunique()}")

# Save initial insights
initial_insights = {
    "total_rows": int(len(df)),
    "total_columns": int(len(df.columns)),
    "columns": list(df.columns),
    "period_range": {
        "start": float(df['Period'].min()) if pd.notna(df['Period'].min()) else None,
        "end": float(df['Period'].max()) if pd.notna(df['Period'].max()) else None
    },
    "unique_counts": {
        "series_references": int(df['Series_reference'].nunique()),
        "groups": int(df['Group'].nunique()),
        "periods": int(df['Period'].nunique())
    }
}

with open('/vercel/sandbox/employment_data_initial_insights.json', 'w') as f:
    json.dump(initial_insights, f, indent=2)

print("\n✅ Phase 1 Complete - Initial insights saved to employment_data_initial_insights.json")

print("\n" + "=" * 80)
print("PHASE 2: DEEP ANALYSIS - PATTERNS AND STATISTICS")
print("=" * 80)

# Analyze Groups
print("\n📊 Groups in Dataset:")
for group in df['Group'].unique():
    count = len(df[df['Group'] == group])
    print(f"   - {group}: {count:,} records ({count/len(df)*100:.1f}%)")

# Analyze Series Title 1 (Employment Variables)
print("\n📊 Employment Variables (Series_title_1):")
for title in df['Series_title_1'].unique():
    count = len(df[df['Series_title_1'] == title])
    print(f"   - {title}: {count:,} records ({count/len(df)*100:.1f}%)")

# Analyze Series Title 3 (Data Types)
print("\n📊 Data Types (Series_title_3):")
for title in df['Series_title_3'].unique():
    count = len(df[df['Series_title_3'] == title])
    print(f"   - {title}: {count:,} records ({count/len(df)*100:.1f}%)")

# Analyze STATUS field
print("\n📊 STATUS Field Distribution:")
status_counts = df['STATUS'].value_counts()
for status, count in status_counts.items():
    print(f"   - {status}: {count:,} records ({count/len(df)*100:.1f}%)")

# Analyze UNITS field
print("\n📊 UNITS Field Distribution:")
units_counts = df['UNITS'].value_counts()
for unit, count in units_counts.items():
    print(f"   - {unit}: {count:,} records ({count/len(df)*100:.1f}%)")

# Analyze Suppressed field
print("\n📊 Suppressed Data:")
suppressed_y = len(df[df['Suppressed'] == 'Y'])
suppressed_empty = len(df[df['Suppressed'] == ''])
print(f"   - Suppressed (Y): {suppressed_y:,} records ({suppressed_y/len(df)*100:.1f}%)")
print(f"   - Not Suppressed: {suppressed_empty:,} records ({suppressed_empty/len(df)*100:.1f}%)")

# Analyze Data_value statistics (for non-suppressed data)
print("\n📊 Data Value Statistics (Non-Suppressed):")
non_suppressed = df[df['Suppressed'] != 'Y']['Data_value'].dropna()
if len(non_suppressed) > 0:
    print(f"   Count: {len(non_suppressed):,}")
    print(f"   Mean: {non_suppressed.mean():,.2f}")
    print(f"   Median: {non_suppressed.median():,.2f}")
    print(f"   Std Dev: {non_suppressed.std():,.2f}")
    print(f"   Min: {non_suppressed.min():,.2f}")
    print(f"   Max: {non_suppressed.max():,.2f}")
    print(f"   25th Percentile: {non_suppressed.quantile(0.25):,.2f}")
    print(f"   75th Percentile: {non_suppressed.quantile(0.75):,.2f}")

print("\n✅ Phase 2 Complete")

print("\n" + "=" * 80)
print("PHASE 3: DETAILED CATEGORY ANALYSIS")
print("=" * 80)

# Analyze Industries (Series_title_2 for Industry group)
industry_data = df[df['Group'] == 'Industry by employment variable']
print(f"\n🏭 Industries Tracked ({industry_data['Series_title_2'].nunique()} unique):")
industry_counts = industry_data['Series_title_2'].value_counts()
for industry, count in industry_counts.head(20).items():
    print(f"   - {industry}: {count:,} records")

# Analyze Age Groups
age_data = df[df['Group'] == 'Age by employment variable']
print(f"\n👥 Age Groups Tracked ({age_data['Series_title_2'].nunique()} unique):")
age_counts = age_data['Series_title_2'].value_counts()
for age, count in age_counts.items():
    print(f"   - {age}: {count:,} records")

# Analyze Sex Categories
sex_data = df[df['Group'] == 'Sex by employment variable']
print(f"\n⚧ Sex Categories Tracked ({sex_data['Series_title_2'].nunique()} unique):")
sex_counts = sex_data['Series_title_2'].value_counts()
for sex, count in sex_counts.items():
    print(f"   - {sex}: {count:,} records")

# Analyze Regions
region_data = df[df['Group'] == 'Region by employment variable']
print(f"\n🗺️ Regions Tracked ({region_data['Series_title_2'].nunique()} unique):")
region_counts = region_data['Series_title_2'].value_counts()
for region, count in region_counts.items():
    print(f"   - {region}: {count:,} records")

# Analyze Territorial Authorities
ta_data = df[df['Group'] == 'Territorial authority by employment variable']
print(f"\n🏛️ Territorial Authorities Tracked: {ta_data['Series_title_2'].nunique()} unique")
print(f"   Total Records: {len(ta_data):,}")
print(f"   Top 10 Territorial Authorities:")
ta_counts = ta_data['Series_title_2'].value_counts()
for ta, count in ta_counts.head(10).items():
    print(f"   - {ta}: {count:,} records")

# Analyze time series patterns
print(f"\n📅 Time Series Analysis:")
print(f"   Years Covered: {df['Year'].min():.0f} to {df['Year'].max():.0f}")
print(f"   Quarters per Year: {df['Quarter'].nunique()}")
print(f"   Quarter Distribution:")
quarter_counts = df['Quarter'].value_counts().sort_index()
for quarter, count in quarter_counts.items():
    if pd.notna(quarter):
        print(f"   - Q{int(quarter/3)}: {count:,} records")

# Analyze Magnitude field
print(f"\n📏 Magnitude Field:")
magnitude_counts = df['Magnitude'].value_counts().sort_index()
for mag, count in magnitude_counts.items():
    print(f"   - Magnitude {mag}: {count:,} records ({count/len(df)*100:.1f}%)")

print("\n✅ Phase 3 Complete")

print("\n" + "=" * 80)
print("PHASE 4: COMPREHENSIVE INSIGHTS AND TRENDS")
print("=" * 80)

# Analyze trends over time for key metrics
print("\n📈 Employment Trends Analysis:")

# Filter for filled jobs data (actual values, not suppressed)
filled_jobs = df[(df['Series_title_1'] == 'Filled jobs') & 
                 (df['Suppressed'] != 'Y') & 
                 (df['Data_value'].notna())]

print(f"   Total Filled Jobs Records: {len(filled_jobs):,}")

# Analyze by industry over time
industry_jobs = filled_jobs[filled_jobs['Group'] == 'Industry by employment variable']
industry_actual = industry_jobs[industry_jobs['Series_title_3'] == 'Actual']

print(f"\n🏭 Industry Employment Trends:")
for industry in industry_actual['Series_title_2'].unique()[:10]:
    industry_subset = industry_actual[industry_actual['Series_title_2'] == industry]
    if len(industry_subset) > 0:
        avg_jobs = industry_subset['Data_value'].mean()
        min_jobs = industry_subset['Data_value'].min()
        max_jobs = industry_subset['Data_value'].max()
        growth = ((max_jobs - min_jobs) / min_jobs * 100) if min_jobs > 0 else 0
        print(f"   - {industry}:")
        print(f"     Avg: {avg_jobs:,.0f} | Min: {min_jobs:,.0f} | Max: {max_jobs:,.0f} | Range: {growth:.1f}%")

# Analyze earnings data
earnings_data = df[(df['Series_title_1'] == 'Total earnings') & 
                   (df['Suppressed'] != 'Y') & 
                   (df['Data_value'].notna())]

print(f"\n💰 Total Earnings Analysis:")
print(f"   Total Earnings Records: {len(earnings_data):,}")
print(f"   Average Earnings Value: ${earnings_data['Data_value'].mean():,.2f}")
print(f"   Median Earnings Value: ${earnings_data['Data_value'].median():,.2f}")

# Analyze by sex
sex_jobs = filled_jobs[filled_jobs['Group'] == 'Sex by employment variable']
sex_actual = sex_jobs[sex_jobs['Series_title_3'] == 'Actual']

print(f"\n⚧ Employment by Sex:")
for sex in sex_actual['Series_title_2'].unique():
    sex_subset = sex_actual[sex_actual['Series_title_2'] == sex]
    if len(sex_subset) > 0:
        avg_jobs = sex_subset['Data_value'].mean()
        latest = sex_subset.sort_values('Period', ascending=False).iloc[0]['Data_value']
        print(f"   - {sex}: Avg {avg_jobs:,.0f} jobs | Latest: {latest:,.0f} jobs")

# Analyze by age groups
age_jobs = filled_jobs[filled_jobs['Group'] == 'Age by employment variable']
age_actual = age_jobs[age_jobs['Series_title_3'] == 'Actual']

print(f"\n👥 Employment by Age Group:")
for age in sorted(age_actual['Series_title_2'].unique()):
    age_subset = age_actual[age_actual['Series_title_2'] == age]
    if len(age_subset) > 0:
        avg_jobs = age_subset['Data_value'].mean()
        latest = age_subset.sort_values('Period', ascending=False).iloc[0]['Data_value']
        print(f"   - {age}: Avg {avg_jobs:,.0f} jobs | Latest: {latest:,.0f} jobs")

# Save comprehensive insights
comprehensive_insights = {
    "dataset_summary": {
        "total_records": int(len(df)),
        "time_period": f"{df['Year'].min():.0f} - {df['Year'].max():.0f}",
        "quarters_covered": int(df['Period'].nunique())
    },
    "categories": {
        "groups": list(df['Group'].unique()),
        "employment_variables": list(df['Series_title_1'].unique()),
        "data_types": list(df['Series_title_3'].unique())
    },
    "industries": list(industry_actual['Series_title_2'].unique()) if len(industry_actual) > 0 else [],
    "age_groups": sorted(list(age_actual['Series_title_2'].unique())) if len(age_actual) > 0 else [],
    "sex_categories": list(sex_actual['Series_title_2'].unique()) if len(sex_actual) > 0 else [],
    "regions": list(region_data['Series_title_2'].unique()) if len(region_data) > 0 else [],
    "data_quality": {
        "suppressed_records": int(len(df[df['Suppressed'] == 'Y'])),
        "missing_data_values": int(df['Data_value'].isna().sum()),
        "complete_records": int(len(df[(df['Suppressed'] != 'Y') & (df['Data_value'].notna())]))
    }
}

with open('/vercel/sandbox/employment_data_comprehensive_insights.json', 'w') as f:
    json.dump(comprehensive_insights, f, indent=2)

print("\n✅ Phase 4 Complete - Comprehensive insights saved")
print("\n" + "=" * 80)
