#!/usr/bin/env python3
"""
Employment Data Analysis Script
Comprehensive analysis of Business Data Collection employment data
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import os

# Create output directories
os.makedirs('./blackbox-analysis/visualization/', exist_ok=True)
os.makedirs('./blackbox-analysis/pdfs/', exist_ok=True)

print("=" * 80)
print("EMPLOYMENT DATA ANALYSIS - Phase 1: Data Discovery")
print("=" * 80)

# Load the complete dataset
file_path = '/vercel/sandbox/uploads/employment-data.csv'
df = pd.read_csv(file_path)

print(f"\n📊 Dataset Overview:")
print(f"   Total Records: {len(df):,}")
print(f"   Columns: {len(df.columns)}")
print(f"   File Size: {os.path.getsize(file_path) / (1024*1024):.2f} MB")

# Display column information
print(f"\n📋 Column Structure:")
for i, col in enumerate(df.columns, 1):
    dtype = df[col].dtype
    non_null = df[col].notna().sum()
    null_count = df[col].isna().sum()
    print(f"   {i:2d}. {col:20s} | Type: {str(dtype):10s} | Non-null: {non_null:6,} | Null: {null_count:6,}")

# Data types and basic statistics
print(f"\n🔍 Data Types:")
print(df.dtypes)

# Check for missing values
print(f"\n❓ Missing Values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Column': missing.index,
    'Missing Count': missing.values,
    'Percentage': missing_pct.values
})
print(missing_df[missing_df['Missing Count'] > 0].to_string(index=False))

# Unique values in key columns
print(f"\n🔑 Unique Values in Key Columns:")
key_columns = ['Series_reference', 'STATUS', 'UNITS', 'Subject', 'Group', 
               'Series_title_1', 'Series_title_2', 'Series_title_3']
for col in key_columns:
    if col in df.columns:
        unique_count = df[col].nunique()
        print(f"   {col:20s}: {unique_count:5,} unique values")

# Period analysis
print(f"\n📅 Time Period Analysis:")
df['Period'] = pd.to_numeric(df['Period'], errors='coerce')
print(f"   Earliest Period: {df['Period'].min()}")
print(f"   Latest Period: {df['Period'].max()}")
print(f"   Period Range: {df['Period'].max() - df['Period'].min():.2f} years")
print(f"   Unique Periods: {df['Period'].nunique()}")

# Data value analysis (convert to numeric)
print(f"\n💰 Data Value Analysis:")
df['Data_value_numeric'] = pd.to_numeric(df['Data_value'], errors='coerce')
non_suppressed = df[df['Suppressed'] != 'Y']['Data_value_numeric']
print(f"   Total Records with Values: {non_suppressed.notna().sum():,}")
print(f"   Suppressed Records: {(df['Suppressed'] == 'Y').sum():,}")
print(f"   Min Value: {non_suppressed.min():,.2f}")
print(f"   Max Value: {non_suppressed.max():,.2f}")
print(f"   Mean Value: {non_suppressed.mean():,.2f}")
print(f"   Median Value: {non_suppressed.median():,.2f}")

# STATUS field analysis
print(f"\n📊 STATUS Field Distribution:")
status_counts = df['STATUS'].value_counts()
for status, count in status_counts.items():
    pct = (count / len(df)) * 100
    print(f"   {status}: {count:6,} ({pct:5.2f}%)")

# UNITS analysis
print(f"\n📏 UNITS Distribution:")
units_counts = df['UNITS'].value_counts()
for unit, count in units_counts.items():
    pct = (count / len(df)) * 100
    print(f"   {unit}: {count:6,} ({pct:5.2f}%)")

# Group analysis
print(f"\n👥 Group Categories:")
group_counts = df['Group'].value_counts()
for group, count in group_counts.items():
    pct = (count / len(df)) * 100
    print(f"   {group}: {count:6,} ({pct:5.2f}%)")

# Series_title_1 analysis (Employment Variable)
print(f"\n📈 Employment Variables (Series_title_1):")
title1_counts = df['Series_title_1'].value_counts()
for title, count in title1_counts.items():
    pct = (count / len(df)) * 100
    print(f"   {title}: {count:6,} ({pct:5.2f}%)")

# Series_title_2 analysis (Categories)
print(f"\n🏢 Top 15 Categories (Series_title_2):")
title2_counts = df['Series_title_2'].value_counts().head(15)
for i, (title, count) in enumerate(title2_counts.items(), 1):
    pct = (count / len(df)) * 100
    print(f"   {i:2d}. {title:45s}: {count:5,} ({pct:5.2f}%)")

# Series_title_3 analysis (Data Type)
print(f"\n📊 Data Types (Series_title_3):")
title3_counts = df['Series_title_3'].value_counts()
for title, count in title3_counts.items():
    if pd.notna(title) and title != '':
        pct = (count / len(df)) * 100
        print(f"   {title}: {count:6,} ({pct:5.2f}%)")

# Save Phase 1 insights
insights = {
    "phase": "1 - Data Discovery",
    "timestamp": datetime.now().isoformat(),
    "dataset_info": {
        "total_records": int(len(df)),
        "columns": int(len(df.columns)),
        "file_size_mb": round(os.path.getsize(file_path) / (1024*1024), 2),
        "period_range": {
            "earliest": float(df['Period'].min()),
            "latest": float(df['Period'].max()),
            "span_years": round(float(df['Period'].max() - df['Period'].min()), 2),
            "unique_periods": int(df['Period'].nunique())
        }
    },
    "data_quality": {
        "suppressed_records": int((df['Suppressed'] == 'Y').sum()),
        "records_with_values": int(non_suppressed.notna().sum()),
        "missing_data_value": int(df['Data_value'].isna().sum())
    },
    "categories": {
        "groups": df['Group'].value_counts().to_dict(),
        "employment_variables": df['Series_title_1'].value_counts().to_dict(),
        "data_types": df['Series_title_3'].value_counts().to_dict(),
        "status_codes": df['STATUS'].value_counts().to_dict(),
        "units": df['UNITS'].value_counts().to_dict()
    },
    "top_categories": {
        "industries": df['Series_title_2'].value_counts().head(20).to_dict(),
        "series_references": df['Series_reference'].value_counts().head(20).to_dict()
    }
}

with open('employment_insights_phase1.json', 'w') as f:
    json.dump(insights, f, indent=2)

print(f"\n✅ Phase 1 Complete - Insights saved to employment_insights_phase1.json")
print("=" * 80)

# ============================================================================
# PHASE 2: DEEP ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("EMPLOYMENT DATA ANALYSIS - Phase 2: Deep Analysis")
print("=" * 80)

# Analyze by Group
print(f"\n🔬 Deep Dive by Group:")
for group in df['Group'].unique():
    group_df = df[df['Group'] == group]
    print(f"\n   📁 {group}:")
    print(f"      Records: {len(group_df):,}")
    print(f"      Unique Categories (Series_title_2): {group_df['Series_title_2'].nunique()}")
    print(f"      Employment Variables: {group_df['Series_title_1'].unique().tolist()}")
    
    # Show top categories for this group
    top_cats = group_df['Series_title_2'].value_counts().head(5)
    print(f"      Top 5 Categories:")
    for cat, count in top_cats.items():
        print(f"         - {cat}: {count:,} records")

# Analyze Industry by employment variable in detail
print(f"\n🏭 Industry Employment Analysis:")
industry_df = df[df['Group'] == 'Industry by employment variable']
industries = industry_df['Series_title_2'].unique()
print(f"   Total Industries: {len(industries)}")
print(f"   Industries List:")
for i, industry in enumerate(sorted(industries), 1):
    count = len(industry_df[industry_df['Series_title_2'] == industry])
    print(f"      {i:2d}. {industry:50s} ({count:3,} records)")

# Analyze Age groups
print(f"\n👶👴 Age Group Analysis:")
age_df = df[df['Group'] == 'Age by employment variable']
age_groups = age_df['Series_title_2'].unique()
print(f"   Total Age Groups: {len(age_groups)}")
print(f"   Age Groups:")
for age in sorted(age_groups):
    count = len(age_df[age_df['Series_title_2'] == age])
    print(f"      - {age:15s}: {count:,} records")

# Analyze Sex breakdown
print(f"\n⚧ Sex-based Analysis:")
sex_df = df[df['Group'] == 'Sex by employment variable']
sex_categories = sex_df['Series_title_2'].unique()
print(f"   Categories: {sex_categories.tolist()}")
for sex in sex_categories:
    count = len(sex_df[sex_df['Series_title_2'] == sex])
    print(f"      - {sex}: {count:,} records")

# Analyze Regional data
print(f"\n🗺️ Regional Analysis:")
region_df = df[df['Group'] == 'Region by employment variable']
regions = region_df['Series_title_2'].unique()
print(f"   Total Regions: {len(regions)}")
print(f"   Regions:")
for region in sorted(regions):
    count = len(region_df[region_df['Series_title_2'] == region])
    print(f"      - {region:30s}: {count:,} records")

# Analyze Territorial authorities
print(f"\n🏘️ Territorial Authority Analysis:")
ta_df = df[df['Group'] == 'Territorial authority by employment variable']
tas = ta_df['Series_title_2'].unique()
print(f"   Total Territorial Authorities: {len(tas)}")
print(f"   Top 20 Territorial Authorities by record count:")
ta_counts = ta_df['Series_title_2'].value_counts().head(20)
for i, (ta, count) in enumerate(ta_counts.items(), 1):
    print(f"      {i:2d}. {ta:40s}: {count:,} records")

# Time series analysis
print(f"\n⏰ Time Series Patterns:")
df['Year'] = df['Period'].apply(lambda x: int(x))
df['Quarter'] = df['Period'].apply(lambda x: int((x % 1) * 100))

year_counts = df['Year'].value_counts().sort_index()
print(f"   Records per Year:")
for year, count in year_counts.items():
    print(f"      {year}: {count:,} records")

quarter_counts = df['Quarter'].value_counts().sort_index()
print(f"\n   Records per Quarter:")
quarter_map = {3: 'Q1 (Mar)', 6: 'Q2 (Jun)', 9: 'Q3 (Sep)', 12: 'Q4 (Dec)'}
for quarter, count in quarter_counts.items():
    q_name = quarter_map.get(quarter, f'Q{quarter}')
    print(f"      {q_name}: {count:,} records")

# Magnitude analysis
print(f"\n📊 Magnitude Analysis:")
mag_counts = df['Magnitude'].value_counts().sort_index()
for mag, count in mag_counts.items():
    pct = (count / len(df)) * 100
    print(f"   Magnitude {mag}: {count:,} records ({pct:.2f}%)")

# Save Phase 2 insights
insights_phase2 = {
    "phase": "2 - Deep Analysis",
    "timestamp": datetime.now().isoformat(),
    "group_breakdown": {
        group: {
            "record_count": int(len(df[df['Group'] == group])),
            "unique_categories": int(df[df['Group'] == group]['Series_title_2'].nunique()),
            "employment_variables": df[df['Group'] == group]['Series_title_1'].unique().tolist()
        }
        for group in df['Group'].unique()
    },
    "industries": {
        "total": int(len(industries)),
        "list": sorted(industries.tolist())
    },
    "age_groups": sorted(age_groups.tolist()),
    "sex_categories": sex_categories.tolist(),
    "regions": {
        "total": int(len(regions)),
        "list": sorted(regions.tolist())
    },
    "territorial_authorities": {
        "total": int(len(tas)),
        "top_20": ta_counts.to_dict()
    },
    "time_series": {
        "years": year_counts.to_dict(),
        "quarters": {quarter_map.get(q, f'Q{q}'): int(c) for q, c in quarter_counts.items()}
    },
    "magnitude_distribution": mag_counts.to_dict()
}

with open('employment_insights_phase2.json', 'w') as f:
    json.dump(insights_phase2, f, indent=2)

print(f"\n✅ Phase 2 Complete - Insights saved to employment_insights_phase2.json")
print("=" * 80)

# ============================================================================
# PHASE 3: STATISTICAL ANALYSIS & TRENDS
# ============================================================================
print("\n" + "=" * 80)
print("EMPLOYMENT DATA ANALYSIS - Phase 3: Statistical Analysis & Trends")
print("=" * 80)

# Filter for actual filled jobs data (not suppressed)
filled_jobs_df = df[(df['Series_title_1'] == 'Filled jobs') & 
                     (df['UNITS'] == 'Number') & 
                     (df['Data_value'].notna())]

print(f"\n📊 Filled Jobs Analysis:")
print(f"   Total Records: {len(filled_jobs_df):,}")

# Industry trends over time
print(f"\n🏭 Industry Employment Trends (2011-2025):")
industry_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Industry by employment variable']
industry_jobs_actual = industry_jobs[industry_jobs['Series_title_3'] == 'Actual']

for industry in sorted(industry_jobs_actual['Series_title_2'].unique()):
    ind_data = industry_jobs_actual[industry_jobs_actual['Series_title_2'] == industry]
    if len(ind_data) > 0:
        earliest = ind_data[ind_data['Period'] == ind_data['Period'].min()]['Data_value'].values[0]
        latest = ind_data[ind_data['Period'] == ind_data['Period'].max()]['Data_value'].values[0]
        change = latest - earliest
        pct_change = (change / earliest) * 100 if earliest > 0 else 0
        avg_jobs = ind_data['Data_value'].mean()
        
        print(f"\n   {industry}:")
        print(f"      2011 Jobs: {earliest:>12,.0f}")
        print(f"      2025 Jobs: {latest:>12,.0f}")
        print(f"      Change:    {change:>12,.0f} ({pct_change:+.2f}%)")
        print(f"      Average:   {avg_jobs:>12,.0f}")

# Regional analysis
print(f"\n\n🗺️ Regional Employment Trends:")
regional_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Region by employment variable']
regional_jobs_actual = regional_jobs[regional_jobs['Series_title_3'] == 'Actual']

region_summary = []
for region in sorted(regional_jobs_actual['Series_title_2'].unique()):
    reg_data = regional_jobs_actual[regional_jobs_actual['Series_title_2'] == region]
    if len(reg_data) > 0:
        earliest = reg_data[reg_data['Period'] == reg_data['Period'].min()]['Data_value'].values[0]
        latest = reg_data[reg_data['Period'] == reg_data['Period'].max()]['Data_value'].values[0]
        change = latest - earliest
        pct_change = (change / earliest) * 100 if earliest > 0 else 0
        avg_jobs = reg_data['Data_value'].mean()
        
        region_summary.append({
            'region': region,
            'earliest': earliest,
            'latest': latest,
            'change': change,
            'pct_change': pct_change,
            'average': avg_jobs
        })

# Sort by latest jobs (descending)
region_summary_sorted = sorted(region_summary, key=lambda x: x['latest'], reverse=True)
print(f"\n   Top 10 Regions by Current Employment (2025):")
for i, reg in enumerate(region_summary_sorted[:10], 1):
    print(f"      {i:2d}. {reg['region']:30s}: {reg['latest']:>10,.0f} jobs ({reg['pct_change']:+6.2f}% change)")

print(f"\n   Fastest Growing Regions (by % change):")
region_growth_sorted = sorted(region_summary, key=lambda x: x['pct_change'], reverse=True)
for i, reg in enumerate(region_growth_sorted[:5], 1):
    print(f"      {i}. {reg['region']:30s}: {reg['pct_change']:+6.2f}% ({reg['change']:+,.0f} jobs)")

# Age group analysis
print(f"\n\n👥 Age Group Employment Trends:")
age_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Age by employment variable']
age_jobs_actual = age_jobs[age_jobs['Series_title_3'] == 'Actual']

age_summary = []
for age_group in sorted(age_jobs_actual['Series_title_2'].unique()):
    age_data = age_jobs_actual[age_jobs_actual['Series_title_2'] == age_group]
    if len(age_data) > 0:
        earliest = age_data[age_data['Period'] == age_data['Period'].min()]['Data_value'].values[0]
        latest = age_data[age_data['Period'] == age_data['Period'].max()]['Data_value'].values[0]
        change = latest - earliest
        pct_change = (change / earliest) * 100 if earliest > 0 else 0
        
        age_summary.append({
            'age_group': age_group,
            'earliest': earliest,
            'latest': latest,
            'change': change,
            'pct_change': pct_change
        })

for age in age_summary:
    print(f"   {age['age_group']:10s}: {age['earliest']:>10,.0f} → {age['latest']:>10,.0f} ({age['pct_change']:+6.2f}%)")

# Gender analysis
print(f"\n\n⚧ Gender Employment Analysis:")
sex_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Sex by employment variable']
sex_jobs_actual = sex_jobs[sex_jobs['Series_title_3'] == 'Actual']

for sex in ['Male', 'Female']:
    sex_data = sex_jobs_actual[sex_jobs_actual['Series_title_2'] == sex]
    if len(sex_data) > 0:
        earliest = sex_data[sex_data['Period'] == sex_data['Period'].min()]['Data_value'].values[0]
        latest = sex_data[sex_data['Period'] == sex_data['Period'].max()]['Data_value'].values[0]
        change = latest - earliest
        pct_change = (change / earliest) * 100 if earliest > 0 else 0
        avg_jobs = sex_data['Data_value'].mean()
        
        print(f"\n   {sex}:")
        print(f"      2011 Jobs: {earliest:>12,.0f}")
        print(f"      2025 Jobs: {latest:>12,.0f}")
        print(f"      Change:    {change:>12,.0f} ({pct_change:+.2f}%)")
        print(f"      Average:   {avg_jobs:>12,.0f}")

# Earnings analysis
print(f"\n\n💰 Total Earnings Analysis:")
earnings_df = df[(df['Series_title_1'] == 'Total earnings') & 
                  (df['UNITS'] == 'Value') & 
                  (df['Data_value'].notna())]

print(f"   Total Earnings Records: {len(earnings_df):,}")
print(f"   Magnitude 6 means values in millions")

# Industry earnings
industry_earnings = earnings_df[earnings_df['Group'] == 'Industry by employment variable']
industry_earnings_actual = industry_earnings[industry_earnings['Series_title_3'] == 'Actual']

print(f"\n   Industry Earnings Trends (in millions):")
for industry in sorted(industry_earnings_actual['Series_title_2'].unique()):
    ind_earn = industry_earnings_actual[industry_earnings_actual['Series_title_2'] == industry]
    if len(ind_earn) > 0:
        earliest = ind_earn[ind_earn['Period'] == ind_earn['Period'].min()]['Data_value'].values[0]
        latest = ind_earn[ind_earn['Period'] == ind_earn['Period'].max()]['Data_value'].values[0]
        change = latest - earliest
        pct_change = (change / earliest) * 100 if earliest > 0 else 0
        
        print(f"      {industry:45s}: ${earliest:>8,.2f}M → ${latest:>8,.2f}M ({pct_change:+6.2f}%)")

# Quarterly patterns
print(f"\n\n📅 Seasonal Patterns (Quarterly Averages):")
quarter_map = {3: 'Q1 (Mar)', 6: 'Q2 (Jun)', 9: 'Q3 (Sep)', 12: 'Q4 (Dec)'}
for quarter, q_name in quarter_map.items():
    q_data = filled_jobs_df[filled_jobs_df['Quarter'] == quarter]
    avg_jobs = q_data['Data_value'].mean()
    print(f"   {q_name}: {avg_jobs:>12,.0f} average jobs")

# Save Phase 3 insights
insights_phase3 = {
    "phase": "3 - Statistical Analysis",
    "timestamp": datetime.now().isoformat(),
    "industry_trends": [
        {
            "industry": industry,
            "start_jobs": float(ind_data[ind_data['Period'] == ind_data['Period'].min()]['Data_value'].values[0]),
            "end_jobs": float(ind_data[ind_data['Period'] == ind_data['Period'].max()]['Data_value'].values[0]),
            "change": float(ind_data[ind_data['Period'] == ind_data['Period'].max()]['Data_value'].values[0] - 
                          ind_data[ind_data['Period'] == ind_data['Period'].min()]['Data_value'].values[0]),
            "pct_change": float((ind_data[ind_data['Period'] == ind_data['Period'].max()]['Data_value'].values[0] - 
                               ind_data[ind_data['Period'] == ind_data['Period'].min()]['Data_value'].values[0]) / 
                              ind_data[ind_data['Period'] == ind_data['Period'].min()]['Data_value'].values[0] * 100)
        }
        for industry in sorted(industry_jobs_actual['Series_title_2'].unique())
        for ind_data in [industry_jobs_actual[industry_jobs_actual['Series_title_2'] == industry]]
        if len(ind_data) > 0
    ],
    "regional_summary": region_summary,
    "age_group_trends": age_summary,
    "gender_analysis": {
        sex: {
            "start_jobs": float(sex_data[sex_data['Period'] == sex_data['Period'].min()]['Data_value'].values[0]),
            "end_jobs": float(sex_data[sex_data['Period'] == sex_data['Period'].max()]['Data_value'].values[0]),
            "average": float(sex_data['Data_value'].mean())
        }
        for sex in ['Male', 'Female']
        for sex_data in [sex_jobs_actual[sex_jobs_actual['Series_title_2'] == sex]]
        if len(sex_data) > 0
    }
}

with open('employment_insights_phase3.json', 'w') as f:
    json.dump(insights_phase3, f, indent=2)

print(f"\n✅ Phase 3 Complete - Insights saved to employment_insights_phase3.json")
print("=" * 80)
