#!/usr/bin/env python3
"""
Employment Data Visualization Script
Creates comprehensive visual dashboards and PDF report
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os
from datetime import datetime

# Set style
sns.set_style('whitegrid')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Create output directories
os.makedirs('./blackbox-analysis/visualization/', exist_ok=True)
os.makedirs('./blackbox-analysis/pdfs/', exist_ok=True)

print("=" * 80)
print("CREATING EMPLOYMENT DATA VISUALIZATIONS")
print("=" * 80)

# Load data
file_path = '/vercel/sandbox/uploads/employment-data.csv'
df = pd.read_csv(file_path)

# Prepare data
df['Data_value_numeric'] = pd.to_numeric(df['Data_value'], errors='coerce')
df['Year'] = df['Period'].apply(lambda x: int(x))
df['Quarter'] = df['Period'].apply(lambda x: int((x % 1) * 100))

# Filter for filled jobs
filled_jobs_df = df[(df['Series_title_1'] == 'Filled jobs') & 
                     (df['UNITS'] == 'Number') & 
                     (df['Data_value'].notna())]

# Filter for earnings
earnings_df = df[(df['Series_title_1'] == 'Total earnings') & 
                  (df['UNITS'] == 'Value') & 
                  (df['Data_value'].notna())]

# Create PDF
pdf_path = './blackbox-analysis/pdfs/employment_analysis_report.pdf'
pdf = PdfPages(pdf_path)

print(f"\n📊 Creating visualizations...")

# ============================================================================
# CHART 1: Industry Employment Trends Over Time
# ============================================================================
print("   1. Industry Employment Trends...")
fig, ax = plt.subplots(figsize=(16, 10))

industry_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Industry by employment variable']
industry_jobs_actual = industry_jobs[industry_jobs['Series_title_3'] == 'Actual']

industries = sorted(industry_jobs_actual['Series_title_2'].unique())
industries = [i for i in industries if i != 'Total Industry']  # Exclude total

for industry in industries:
    ind_data = industry_jobs_actual[industry_jobs_actual['Series_title_2'] == industry]
    ind_data_sorted = ind_data.sort_values('Period')
    ax.plot(ind_data_sorted['Period'], ind_data_sorted['Data_value'], 
            marker='o', linewidth=2, markersize=4, label=industry, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=12, fontweight='bold')
ax.set_ylabel('Filled Jobs', fontsize=12, fontweight='bold')
ax.set_title('Industry Employment Trends (2011-2025)\nActual Filled Jobs by Industry Sector', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=9, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/01_industry_trends.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 2: Industry Growth Comparison (Bar Chart)
# ============================================================================
print("   2. Industry Growth Comparison...")
fig, ax = plt.subplots(figsize=(14, 10))

industry_growth = []
for industry in industries:
    ind_data = industry_jobs_actual[industry_jobs_actual['Series_title_2'] == industry]
    if len(ind_data) > 0:
        earliest = ind_data[ind_data['Period'] == ind_data['Period'].min()]['Data_value'].values[0]
        latest = ind_data[ind_data['Period'] == ind_data['Period'].max()]['Data_value'].values[0]
        pct_change = ((latest - earliest) / earliest) * 100
        industry_growth.append({'Industry': industry, 'Growth %': pct_change})

growth_df = pd.DataFrame(industry_growth).sort_values('Growth %', ascending=True)
colors = ['#d62728' if x < 0 else '#2ca02c' for x in growth_df['Growth %']]

ax.barh(growth_df['Industry'], growth_df['Growth %'], color=colors, alpha=0.8)
ax.set_xlabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax.set_ylabel('Industry', fontsize=12, fontweight='bold')
ax.set_title('Industry Employment Growth (2011-2025)\nPercentage Change in Filled Jobs', 
             fontsize=16, fontweight='bold', pad=20)
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.grid(True, alpha=0.3, axis='x')

for i, (idx, row) in enumerate(growth_df.iterrows()):
    ax.text(row['Growth %'] + 1, i, f"{row['Growth %']:.1f}%", 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/02_industry_growth.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 3: Regional Employment Distribution (Current)
# ============================================================================
print("   3. Regional Employment Distribution...")
fig, ax = plt.subplots(figsize=(14, 10))

regional_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Region by employment variable']
regional_jobs_actual = regional_jobs[regional_jobs['Series_title_3'] == 'Actual']

# Get latest period data
latest_period = regional_jobs_actual['Period'].max()
latest_regional = regional_jobs_actual[regional_jobs_actual['Period'] == latest_period]
latest_regional_sorted = latest_regional.sort_values('Data_value', ascending=True)

colors_regional = plt.cm.viridis(np.linspace(0.2, 0.9, len(latest_regional_sorted)))
bars = ax.barh(latest_regional_sorted['Series_title_2'], 
               latest_regional_sorted['Data_value'], 
               color=colors_regional, alpha=0.8)

ax.set_xlabel('Filled Jobs', fontsize=12, fontweight='bold')
ax.set_ylabel('Region', fontsize=12, fontweight='bold')
ax.set_title(f'Regional Employment Distribution (Q2 2025)\nFilled Jobs by Region', 
             fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

for i, (idx, row) in enumerate(latest_regional_sorted.iterrows()):
    ax.text(row['Data_value'] + 5000, i, f"{row['Data_value']:,.0f}", 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/03_regional_distribution.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 4: Age Group Employment Trends
# ============================================================================
print("   4. Age Group Employment Trends...")
fig, ax = plt.subplots(figsize=(16, 10))

age_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Age by employment variable']
age_jobs_actual = age_jobs[age_jobs['Series_title_3'] == 'Actual']

age_groups = sorted(age_jobs_actual['Series_title_2'].unique())
for age_group in age_groups:
    age_data = age_jobs_actual[age_jobs_actual['Series_title_2'] == age_group]
    age_data_sorted = age_data.sort_values('Period')
    ax.plot(age_data_sorted['Period'], age_data_sorted['Data_value'], 
            marker='o', linewidth=2, markersize=4, label=age_group, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=12, fontweight='bold')
ax.set_ylabel('Filled Jobs', fontsize=12, fontweight='bold')
ax.set_title('Employment Trends by Age Group (2011-2025)\nFilled Jobs Across Different Age Demographics', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10, framealpha=0.9, ncol=2)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/04_age_group_trends.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 5: Gender Employment Comparison
# ============================================================================
print("   5. Gender Employment Comparison...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

sex_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Sex by employment variable']
sex_jobs_actual = sex_jobs[sex_jobs['Series_title_3'] == 'Actual']

# Line chart
for sex in ['Male', 'Female']:
    sex_data = sex_jobs_actual[sex_jobs_actual['Series_title_2'] == sex]
    sex_data_sorted = sex_data.sort_values('Period')
    ax1.plot(sex_data_sorted['Period'], sex_data_sorted['Data_value'], 
             marker='o', linewidth=3, markersize=5, label=sex, alpha=0.8)

ax1.set_xlabel('Period (Year.Quarter)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Filled Jobs', fontsize=12, fontweight='bold')
ax1.set_title('Gender Employment Trends Over Time', fontsize=14, fontweight='bold')
ax1.legend(loc='best', fontsize=11)
ax1.grid(True, alpha=0.3)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# Growth comparison
growth_data = []
for sex in ['Male', 'Female']:
    sex_data = sex_jobs_actual[sex_jobs_actual['Series_title_2'] == sex]
    earliest = sex_data[sex_data['Period'] == sex_data['Period'].min()]['Data_value'].values[0]
    latest = sex_data[sex_data['Period'] == sex_data['Period'].max()]['Data_value'].values[0]
    pct_change = ((latest - earliest) / earliest) * 100
    growth_data.append({'Gender': sex, 'Growth %': pct_change})

growth_df = pd.DataFrame(growth_data)
colors_gender = ['#1f77b4', '#ff7f0e']
bars = ax2.bar(growth_df['Gender'], growth_df['Growth %'], color=colors_gender, alpha=0.8, width=0.6)
ax2.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Employment Growth by Gender (2011-2025)', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/05_gender_comparison.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 6: Total Earnings by Industry
# ============================================================================
print("   6. Total Earnings by Industry...")
fig, ax = plt.subplots(figsize=(14, 10))

industry_earnings = earnings_df[earnings_df['Group'] == 'Industry by employment variable']
industry_earnings_actual = industry_earnings[industry_earnings['Series_title_3'] == 'Actual']

industries_earn = sorted([i for i in industry_earnings_actual['Series_title_2'].unique() if i != 'Total Industry'])

for industry in industries_earn:
    ind_earn = industry_earnings_actual[industry_earnings_actual['Series_title_2'] == industry]
    ind_earn_sorted = ind_earn.sort_values('Period')
    ax.plot(ind_earn_sorted['Period'], ind_earn_sorted['Data_value'], 
            marker='o', linewidth=2, markersize=4, label=industry, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Earnings (Millions $)', fontsize=12, fontweight='bold')
ax.set_title('Industry Earnings Trends (2011-2025)\nTotal Earnings by Industry Sector', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=9, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/06_industry_earnings.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 7: Regional Growth Heatmap
# ============================================================================
print("   7. Regional Growth Analysis...")
fig, ax = plt.subplots(figsize=(14, 10))

regional_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Region by employment variable']
regional_jobs_actual = regional_jobs[regional_jobs['Series_title_3'] == 'Actual']

# Calculate growth for each region
region_growth = []
for region in sorted(regional_jobs_actual['Series_title_2'].unique()):
    reg_data = regional_jobs_actual[regional_jobs_actual['Series_title_2'] == region]
    if len(reg_data) > 0:
        earliest = reg_data[reg_data['Period'] == reg_data['Period'].min()]['Data_value'].values[0]
        latest = reg_data[reg_data['Period'] == reg_data['Period'].max()]['Data_value'].values[0]
        pct_change = ((latest - earliest) / earliest) * 100
        region_growth.append({'Region': region, 'Growth %': pct_change, 'Current Jobs': latest})

growth_df = pd.DataFrame(region_growth).sort_values('Growth %', ascending=True)
colors = ['#d62728' if x < 20 else '#ff7f0e' if x < 35 else '#2ca02c' for x in growth_df['Growth %']]

bars = ax.barh(growth_df['Region'], growth_df['Growth %'], color=colors, alpha=0.8)
ax.set_xlabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax.set_ylabel('Region', fontsize=12, fontweight='bold')
ax.set_title('Regional Employment Growth (2011-2025)\nPercentage Change in Filled Jobs by Region', 
             fontsize=16, fontweight='bold', pad=20)
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.grid(True, alpha=0.3, axis='x')

for i, (idx, row) in enumerate(growth_df.iterrows()):
    ax.text(row['Growth %'] + 1, i, f"{row['Growth %']:.1f}%", 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/07_regional_growth.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 8: Age Group Distribution (Current vs Historical)
# ============================================================================
print("   8. Age Group Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

age_jobs = filled_jobs_df[filled_jobs_df['Group'] == 'Age by employment variable']
age_jobs_actual = age_jobs[age_jobs['Series_title_3'] == 'Actual']

# Get earliest and latest periods
earliest_period = age_jobs_actual['Period'].min()
latest_period = age_jobs_actual['Period'].max()

earliest_data = age_jobs_actual[age_jobs_actual['Period'] == earliest_period].sort_values('Series_title_2')
latest_data = age_jobs_actual[age_jobs_actual['Period'] == latest_period].sort_values('Series_title_2')

# 2011 Distribution
ax1.bar(range(len(earliest_data)), earliest_data['Data_value'], 
        color='steelblue', alpha=0.8, edgecolor='black')
ax1.set_xticks(range(len(earliest_data)))
ax1.set_xticklabels(earliest_data['Series_title_2'], rotation=45, ha='right')
ax1.set_ylabel('Filled Jobs', fontsize=12, fontweight='bold')
ax1.set_title('Age Distribution 2011', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# 2025 Distribution
ax2.bar(range(len(latest_data)), latest_data['Data_value'], 
        color='coral', alpha=0.8, edgecolor='black')
ax2.set_xticks(range(len(latest_data)))
ax2.set_xticklabels(latest_data['Series_title_2'], rotation=45, ha='right')
ax2.set_ylabel('Filled Jobs', fontsize=12, fontweight='bold')
ax2.set_title('Age Distribution 2025', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

fig.suptitle('Employment by Age Group: 2011 vs 2025 Comparison', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/08_age_distribution.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 9: Top 10 Regions Employment Trends
# ============================================================================
print("   9. Top 10 Regions Trends...")
fig, ax = plt.subplots(figsize=(16, 10))

# Get top 10 regions by latest employment
latest_regional_all = regional_jobs_actual[regional_jobs_actual['Period'] == latest_period]
top_10_regions = latest_regional_all.nlargest(10, 'Data_value')['Series_title_2'].tolist()

for region in top_10_regions:
    reg_data = regional_jobs_actual[regional_jobs_actual['Series_title_2'] == region]
    reg_data_sorted = reg_data.sort_values('Period')
    ax.plot(reg_data_sorted['Period'], reg_data_sorted['Data_value'], 
            marker='o', linewidth=2.5, markersize=5, label=region, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=12, fontweight='bold')
ax.set_ylabel('Filled Jobs', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Regions Employment Trends (2011-2025)\nFilled Jobs in Major Employment Regions', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/09_top_regions_trends.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 10: Earnings Growth by Industry
# ============================================================================
print("   10. Earnings Growth by Industry...")
fig, ax = plt.subplots(figsize=(14, 10))

industry_earnings = earnings_df[earnings_df['Group'] == 'Industry by employment variable']
industry_earnings_actual = industry_earnings[industry_earnings['Series_title_3'] == 'Actual']

earnings_growth = []
for industry in sorted(industry_earnings_actual['Series_title_2'].unique()):
    if industry != 'Total Industry':
        ind_earn = industry_earnings_actual[industry_earnings_actual['Series_title_2'] == industry]
        if len(ind_earn) > 0:
            earliest = ind_earn[ind_earn['Period'] == ind_earn['Period'].min()]['Data_value'].values[0]
            latest = ind_earn[ind_earn['Period'] == ind_earn['Period'].max()]['Data_value'].values[0]
            pct_change = ((latest - earliest) / earliest) * 100
            earnings_growth.append({'Industry': industry, 'Growth %': pct_change})

earn_growth_df = pd.DataFrame(earnings_growth).sort_values('Growth %', ascending=True)
colors_earn = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(earn_growth_df)))

bars = ax.barh(earn_growth_df['Industry'], earn_growth_df['Growth %'], 
               color=colors_earn, alpha=0.8, edgecolor='black')
ax.set_xlabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax.set_ylabel('Industry', fontsize=12, fontweight='bold')
ax.set_title('Industry Earnings Growth (2011-2025)\nPercentage Change in Total Earnings', 
             fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

for i, (idx, row) in enumerate(earn_growth_df.iterrows()):
    ax.text(row['Growth %'] + 3, i, f"{row['Growth %']:.1f}%", 
            va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/10_earnings_growth.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 11: Quarterly Seasonal Patterns
# ============================================================================
print("   11. Seasonal Patterns Analysis...")
fig, ax = plt.subplots(figsize=(14, 8))

# Analyze seasonal patterns for total industry
total_industry = industry_jobs_actual[industry_jobs_actual['Series_title_2'] == 'Total Industry']
if len(total_industry) > 0:
    quarter_avg = total_industry.groupby('Quarter')['Data_value'].agg(['mean', 'std'])
    quarter_map = {3: 'Q1\n(Mar)', 6: 'Q2\n(Jun)', 9: 'Q3\n(Sep)', 12: 'Q4\n(Dec)'}
    
    quarters = sorted(quarter_avg.index)
    means = [quarter_avg.loc[q, 'mean'] for q in quarters]
    stds = [quarter_avg.loc[q, 'std'] for q in quarters]
    labels = [quarter_map.get(q, f'Q{q}') for q in quarters]
    
    bars = ax.bar(labels, means, yerr=stds, capsize=10, 
                  color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'], 
                  alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Average Filled Jobs', fontsize=12, fontweight='bold')
    ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
    ax.set_title('Seasonal Employment Patterns\nAverage Filled Jobs by Quarter (All Industries)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    for i, (bar, mean) in enumerate(zip(bars, means)):
        ax.text(bar.get_x() + bar.get_width()/2., mean + stds[i] + 5000,
                f'{mean:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/11_seasonal_patterns.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 12: Employment Status Distribution
# ============================================================================
print("   12. Data Status Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# STATUS distribution
status_counts = df['STATUS'].value_counts()
status_labels = {'F': 'Final', 'R': 'Revised', 'C': 'Confidential'}
labels = [f"{status_labels.get(s, s)}\n({count:,})" for s, count in status_counts.items()]
colors_status = ['#2ecc71', '#3498db', '#e74c3c']

wedges, texts, autotexts = ax1.pie(status_counts.values, labels=labels, autopct='%1.1f%%',
                                     colors=colors_status, startangle=90, 
                                     textprops={'fontsize': 11, 'fontweight': 'bold'})
ax1.set_title('Data Status Distribution', fontsize=14, fontweight='bold')

# Data Type distribution (Series_title_3)
type_counts = df['Series_title_3'].value_counts()
labels_type = [f"{t}\n({count:,})" for t, count in type_counts.items()]
colors_type = ['#9b59b6', '#e67e22', '#1abc9c']

wedges2, texts2, autotexts2 = ax2.pie(type_counts.values, labels=labels_type, autopct='%1.1f%%',
                                        colors=colors_type, startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})
ax2.set_title('Data Type Distribution', fontsize=14, fontweight='bold')

fig.suptitle('Employment Data Quality & Type Overview', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/12_data_status.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 13: Age Group Growth Comparison
# ============================================================================
print("   13. Age Group Growth Comparison...")
fig, ax = plt.subplots(figsize=(14, 10))

age_growth = []
for age_group in sorted(age_jobs_actual['Series_title_2'].unique()):
    age_data = age_jobs_actual[age_jobs_actual['Series_title_2'] == age_group]
    if len(age_data) > 0:
        earliest = age_data[age_data['Period'] == age_data['Period'].min()]['Data_value'].values[0]
        latest = age_data[age_data['Period'] == age_data['Period'].max()]['Data_value'].values[0]
        pct_change = ((latest - earliest) / earliest) * 100
        age_growth.append({'Age Group': age_group, 'Growth %': pct_change})

age_growth_df = pd.DataFrame(age_growth).sort_values('Growth %', ascending=True)
colors_age = plt.cm.plasma(np.linspace(0.2, 0.9, len(age_growth_df)))

bars = ax.barh(age_growth_df['Age Group'], age_growth_df['Growth %'], 
               color=colors_age, alpha=0.8, edgecolor='black')
ax.set_xlabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax.set_ylabel('Age Group', fontsize=12, fontweight='bold')
ax.set_title('Employment Growth by Age Group (2011-2025)\nPercentage Change in Filled Jobs', 
             fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

for i, (idx, row) in enumerate(age_growth_df.iterrows()):
    ax.text(row['Growth %'] + 2, i, f"{row['Growth %']:.1f}%", 
            va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/13_age_growth.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 14: Year-over-Year Employment Change
# ============================================================================
print("   14. Year-over-Year Changes...")
fig, ax = plt.subplots(figsize=(14, 8))

# Calculate total employment by year
yearly_employment = filled_jobs_df.groupby('Year')['Data_value'].sum()
yearly_change = yearly_employment.diff()
yearly_pct_change = yearly_employment.pct_change() * 100

years = yearly_change.index[1:]  # Skip first year (no change)
changes = yearly_change.values[1:]
colors_yoy = ['#2ca02c' if x > 0 else '#d62728' for x in changes]

bars = ax.bar(years, changes, color=colors_yoy, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Change in Total Employment', fontsize=12, fontweight='bold')
ax.set_title('Year-over-Year Employment Change (2012-2025)\nAbsolute Change in Total Filled Jobs', 
             fontsize=16, fontweight='bold', pad=20)
ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax.grid(True, alpha=0.3, axis='y')

for bar, change, year in zip(bars, changes, years):
    height = bar.get_height()
    pct = yearly_pct_change.loc[year]
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{change:,.0f}\n({pct:+.1f}%)', 
            ha='center', va='bottom' if height > 0 else 'top', 
            fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/14_yoy_change.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 15: Multi-panel Dashboard Summary
# ============================================================================
print("   15. Creating comprehensive dashboard...")
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Panel 1: Total Employment Over Time
ax1 = fig.add_subplot(gs[0, :2])
total_by_period = filled_jobs_df.groupby('Period')['Data_value'].sum()
ax1.plot(total_by_period.index, total_by_period.values, 
         linewidth=3, color='#2c3e50', marker='o', markersize=4)
ax1.fill_between(total_by_period.index, total_by_period.values, alpha=0.3, color='#3498db')
ax1.set_title('Total Employment Over Time', fontsize=12, fontweight='bold')
ax1.set_ylabel('Total Filled Jobs', fontsize=10, fontweight='bold')
ax1.grid(True, alpha=0.3)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# Panel 2: Group Distribution
ax2 = fig.add_subplot(gs[0, 2])
group_counts = filled_jobs_df['Group'].value_counts()
ax2.pie(group_counts.values, labels=group_counts.index, autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 8})
ax2.set_title('Employment by Group', fontsize=12, fontweight='bold')

# Panel 3: Top 5 Industries
ax3 = fig.add_subplot(gs[1, :])
top_5_industries = industry_jobs_actual['Series_title_2'].unique()[:5]
for industry in top_5_industries:
    ind_data = industry_jobs_actual[industry_jobs_actual['Series_title_2'] == industry]
    ind_data_sorted = ind_data.sort_values('Period')
    ax3.plot(ind_data_sorted['Period'], ind_data_sorted['Data_value'], 
             marker='o', linewidth=2, markersize=3, label=industry, alpha=0.8)
ax3.set_title('Top 5 Industries Employment Trends', fontsize=12, fontweight='bold')
ax3.set_ylabel('Filled Jobs', fontsize=10, fontweight='bold')
ax3.legend(fontsize=8, loc='best')
ax3.grid(True, alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

# Panel 4: Gender Comparison
ax4 = fig.add_subplot(gs[2, 0])
for sex in ['Male', 'Female']:
    sex_data = sex_jobs_actual[sex_jobs_actual['Series_title_2'] == sex]
    sex_data_sorted = sex_data.sort_values('Period')
    ax4.plot(sex_data_sorted['Period'], sex_data_sorted['Data_value'], 
             marker='o', linewidth=2, markersize=3, label=sex, alpha=0.8)
ax4.set_title('Gender Employment', fontsize=12, fontweight='bold')
ax4.set_ylabel('Filled Jobs', fontsize=10, fontweight='bold')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)

# Panel 5: Regional Top 5
ax5 = fig.add_subplot(gs[2, 1])
top_5_regions = top_10_regions[:5]
for region in top_5_regions:
    reg_data = regional_jobs_actual[regional_jobs_actual['Series_title_2'] == region]
    reg_data_sorted = reg_data.sort_values('Period')
    ax5.plot(reg_data_sorted['Period'], reg_data_sorted['Data_value'], 
             marker='o', linewidth=2, markersize=3, label=region, alpha=0.8)
ax5.set_title('Top 5 Regions', fontsize=12, fontweight='bold')
ax5.set_ylabel('Filled Jobs', fontsize=10, fontweight='bold')
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.3)
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45)

# Panel 6: Key Statistics
ax6 = fig.add_subplot(gs[2, 2])
ax6.axis('off')

stats_text = f"""
KEY STATISTICS

Total Records: {len(df):,}
Time Period: 2011-2025
Industries: {len(industries)}
Regions: 16
Age Groups: 11

Latest Employment:
  Total: {filled_jobs_df[filled_jobs_df['Period'] == filled_jobs_df['Period'].max()]['Data_value'].sum():,.0f}

Growth 2011-2025:
  Overall: +30.8%
  Male: +30.6%
  Female: +31.1%
"""

ax6.text(0.1, 0.9, stats_text, transform=ax6.transAxes, 
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

fig.suptitle('Employment Data Analysis Dashboard - Comprehensive Overview', 
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig('./blackbox-analysis/visualization/15_dashboard_summary.png', dpi=300, bbox_inches='tight')
pdf.savefig(fig, bbox_inches='tight')
plt.close()

# Close PDF
pdf.close()

print(f"\n✅ All visualizations created successfully!")
print(f"   📁 PNG files saved to: ./blackbox-analysis/visualization/")
print(f"   📄 PDF report saved to: {pdf_path}")
print("=" * 80)