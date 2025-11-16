"""
Employment Data Visualization Script
Creates comprehensive visualizations and PDF dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Create output directories
os.makedirs('./blackbox-analysis/visualization/', exist_ok=True)
os.makedirs('./blackbox-analysis/pdfs/', exist_ok=True)

print("=" * 80)
print("CREATING COMPREHENSIVE EMPLOYMENT DATA VISUALIZATIONS")
print("=" * 80)

# Load data
df = pd.read_csv('/vercel/sandbox/uploads/employment-data.csv')
df['Period'] = pd.to_numeric(df['Period'], errors='coerce')
df['Year'] = df['Period'].apply(lambda x: int(x) if pd.notna(x) else None)
df['Quarter'] = df['Period'].apply(lambda x: int((x % 1) * 100) if pd.notna(x) else None)

# Filter for non-suppressed data
df_clean = df[(df['Suppressed'] != 'Y') & (df['Data_value'].notna())].copy()

print(f"\n✅ Loaded {len(df):,} total records, {len(df_clean):,} non-suppressed records")

# List to store all chart paths for PDF
chart_paths = []

# ============================================================================
# CHART 1: Employment Trends by Industry Over Time
# ============================================================================
print("\n📊 Creating Chart 1: Employment Trends by Industry...")

industry_jobs = df_clean[(df_clean['Group'] == 'Industry by employment variable') & 
                         (df_clean['Series_title_1'] == 'Filled jobs') &
                         (df_clean['Series_title_3'] == 'Actual')]

# Get top industries
top_industries = industry_jobs.groupby('Series_title_2')['Data_value'].mean().nlargest(8).index

fig, ax = plt.subplots(figsize=(16, 10))
for industry in top_industries:
    industry_data = industry_jobs[industry_jobs['Series_title_2'] == industry].sort_values('Period')
    ax.plot(industry_data['Period'], industry_data['Data_value'], 
            marker='o', linewidth=2, markersize=4, label=industry, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Filled Jobs', fontsize=14, fontweight='bold')
ax.set_title('Employment Trends by Industry (2011-2025)', fontsize=18, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
chart1_path = './blackbox-analysis/visualization/01_industry_employment_trends.png'
plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
plt.close()
chart_paths.append(chart1_path)
print(f"   ✅ Saved: {chart1_path}")

# ============================================================================
# CHART 2: Employment by Age Group Distribution
# ============================================================================
print("\n📊 Creating Chart 2: Employment by Age Group...")

age_jobs = df_clean[(df_clean['Group'] == 'Age by employment variable') & 
                    (df_clean['Series_title_1'] == 'Filled jobs') &
                    (df_clean['Series_title_3'] == 'Actual')]

# Get latest data for each age group
latest_period = age_jobs['Period'].max()
age_latest = age_jobs[age_jobs['Period'] == latest_period].groupby('Series_title_2')['Data_value'].sum().sort_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Bar chart
colors = sns.color_palette('viridis', len(age_latest))
bars = ax1.bar(range(len(age_latest)), age_latest.values, color=colors, edgecolor='black', linewidth=1.5)
ax1.set_xticks(range(len(age_latest)))
ax1.set_xticklabels(age_latest.index, rotation=45, ha='right')
ax1.set_xlabel('Age Group', fontsize=14, fontweight='bold')
ax1.set_ylabel('Number of Filled Jobs', fontsize=14, fontweight='bold')
ax1.set_title(f'Employment Distribution by Age Group (Q{int(latest_period % 1 * 100/3)} {int(latest_period)})', 
              fontsize=16, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, age_latest.values)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(value):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Pie chart
colors_pie = sns.color_palette('Set3', len(age_latest))
wedges, texts, autotexts = ax2.pie(age_latest.values, labels=age_latest.index, autopct='%1.1f%%',
                                     colors=colors_pie, startangle=90, textprops={'fontsize': 10})
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
ax2.set_title('Age Group Distribution (%)', fontsize=16, fontweight='bold')

plt.tight_layout()
chart2_path = './blackbox-analysis/visualization/02_age_group_distribution.png'
plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
plt.close()
chart_paths.append(chart2_path)
print(f"   ✅ Saved: {chart2_path}")

# ============================================================================
# CHART 3: Employment by Sex Over Time
# ============================================================================
print("\n📊 Creating Chart 3: Employment by Sex Over Time...")

sex_jobs = df_clean[(df_clean['Group'] == 'Sex by employment variable') & 
                    (df_clean['Series_title_1'] == 'Filled jobs') &
                    (df_clean['Series_title_3'] == 'Actual')]

fig, ax = plt.subplots(figsize=(16, 9))
for sex in sex_jobs['Series_title_2'].unique():
    sex_data = sex_jobs[sex_jobs['Series_title_2'] == sex].sort_values('Period')
    ax.plot(sex_data['Period'], sex_data['Data_value'], 
            marker='o', linewidth=3, markersize=5, label=sex, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Filled Jobs', fontsize=14, fontweight='bold')
ax.set_title('Employment Trends by Sex (2011-2025)', fontsize=18, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=12, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
chart3_path = './blackbox-analysis/visualization/03_sex_employment_trends.png'
plt.savefig(chart3_path, dpi=300, bbox_inches='tight')
plt.close()
chart_paths.append(chart3_path)
print(f"   ✅ Saved: {chart3_path}")

# ============================================================================
# CHART 4: Regional Employment Distribution
# ============================================================================
print("\n📊 Creating Chart 4: Regional Employment Distribution...")

region_jobs = df_clean[(df_clean['Group'] == 'Region by employment variable') & 
                       (df_clean['Series_title_1'] == 'Filled jobs') &
                       (df_clean['Series_title_3'] == 'Actual')]

# Get latest data for each region
region_latest = region_jobs[region_jobs['Period'] == region_jobs['Period'].max()].groupby('Series_title_2')['Data_value'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(16, 10))
colors = sns.color_palette('coolwarm', len(region_latest))
bars = ax.barh(range(len(region_latest)), region_latest.values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_yticks(range(len(region_latest)))
ax.set_yticklabels(region_latest.index, fontsize=11)
ax.set_xlabel('Number of Filled Jobs', fontsize=14, fontweight='bold')
ax.set_ylabel('Region', fontsize=14, fontweight='bold')
ax.set_title(f'Employment by Region (Latest Period: Q{int(region_jobs["Period"].max() % 1 * 100/3)} {int(region_jobs["Period"].max())})', 
             fontsize=18, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, value) in enumerate(zip(bars, region_latest.values)):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f' {int(value):,}', ha='left', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
chart4_path = './blackbox-analysis/visualization/04_regional_employment.png'
plt.savefig(chart4_path, dpi=300, bbox_inches='tight')
plt.close()
chart_paths.append(chart4_path)
print(f"   ✅ Saved: {chart4_path}")

# ============================================================================
# CHART 5: Total Earnings by Industry
# ============================================================================
print("\n📊 Creating Chart 5: Total Earnings by Industry...")

earnings_industry = df_clean[(df_clean['Group'] == 'Industry by employment variable') & 
                             (df_clean['Series_title_1'] == 'Total earnings') &
                             (df_clean['Series_title_3'] == 'Actual')]

if len(earnings_industry) > 0:
    # Get average earnings by industry
    industry_earnings = earnings_industry.groupby('Series_title_2')['Data_value'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    colors = sns.color_palette('Spectral', len(industry_earnings))
    bars = ax.barh(range(len(industry_earnings)), industry_earnings.values, color=colors, edgecolor='black', linewidth=1.5)
    ax.set_yticks(range(len(industry_earnings)))
    ax.set_yticklabels(industry_earnings.index, fontsize=11)
    ax.set_xlabel('Average Total Earnings (Millions)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Industry', fontsize=14, fontweight='bold')
    ax.set_title('Average Total Earnings by Industry (2011-2025)', fontsize=18, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, industry_earnings.values)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f' ${value:,.0f}M', ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    chart5_path = './blackbox-analysis/visualization/05_industry_earnings.png'
    plt.savefig(chart5_path, dpi=300, bbox_inches='tight')
    plt.close()
    chart_paths.append(chart5_path)
    print(f"   ✅ Saved: {chart5_path}")

# ============================================================================
# CHART 6: Year-over-Year Employment Growth
# ============================================================================
print("\n📊 Creating Chart 6: Year-over-Year Employment Growth...")

# Calculate YoY growth for total industry
total_industry = industry_jobs[industry_jobs['Series_title_2'] == 'Total Industry'].sort_values('Period')

if len(total_industry) > 0:
    # Group by year and calculate average
    yearly_data = total_industry.groupby('Year')['Data_value'].mean()
    yoy_growth = yearly_data.pct_change() * 100
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
    
    # Absolute values
    ax1.plot(yearly_data.index, yearly_data.values, marker='o', linewidth=3, 
             markersize=8, color='steelblue', label='Average Filled Jobs')
    ax1.fill_between(yearly_data.index, yearly_data.values, alpha=0.3, color='steelblue')
    ax1.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Average Filled Jobs', fontsize=14, fontweight='bold')
    ax1.set_title('Total Industry Employment Over Time', fontsize=16, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=12)
    
    # YoY Growth Rate
    colors = ['green' if x > 0 else 'red' for x in yoy_growth.values]
    ax2.bar(yoy_growth.index, yoy_growth.values, color=colors, edgecolor='black', linewidth=1.5, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Year-over-Year Growth (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Year-over-Year Employment Growth Rate', fontsize=16, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, (year, value) in enumerate(zip(yoy_growth.index, yoy_growth.values)):
        if pd.notna(value):
            ax2.text(year, value, f'{value:.1f}%', ha='center', 
                    va='bottom' if value > 0 else 'top', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    chart6_path = './blackbox-analysis/visualization/06_yoy_growth.png'
    plt.savefig(chart6_path, dpi=300, bbox_inches='tight')
    plt.close()
    chart_paths.append(chart6_path)
    print(f"   ✅ Saved: {chart6_path}")

# ============================================================================
# CHART 7: Heatmap of Employment by Age Group Over Time
# ============================================================================
print("\n📊 Creating Chart 7: Employment Heatmap by Age Group...")

age_jobs = df_clean[(df_clean['Group'] == 'Age by employment variable') & 
                    (df_clean['Series_title_1'] == 'Filled jobs') &
                    (df_clean['Series_title_3'] == 'Actual')]

# Create pivot table
age_pivot = age_jobs.pivot_table(values='Data_value', index='Series_title_2', 
                                  columns='Year', aggfunc='mean')

fig, ax = plt.subplots(figsize=(16, 10))
sns.heatmap(age_pivot, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Filled Jobs'},
            linewidths=0.5, ax=ax, annot_kws={'fontsize': 8})
ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Age Group', fontsize=14, fontweight='bold')
ax.set_title('Employment Heatmap by Age Group Over Years', fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()
chart7_path = './blackbox-analysis/visualization/07_age_heatmap.png'
plt.savefig(chart7_path, dpi=300, bbox_inches='tight')
plt.close()
chart_paths.append(chart7_path)
print(f"   ✅ Saved: {chart7_path}")

# ============================================================================
# CHART 8: Quarterly Seasonality Pattern
# ============================================================================
print("\n📊 Creating Chart 8: Quarterly Seasonality Pattern...")

# Analyze seasonality across all industries
quarterly_pattern = industry_jobs.groupby('Quarter')['Data_value'].agg(['mean', 'std', 'count'])

fig, ax = plt.subplots(figsize=(14, 8))
quarters = ['Q1 (Mar)', 'Q2 (Jun)', 'Q3 (Sep)', 'Q4 (Dec)']
x_pos = [3, 6, 9, 12]

bars = ax.bar(x_pos, quarterly_pattern['mean'].values, 
              yerr=quarterly_pattern['std'].values,
              color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
              edgecolor='black', linewidth=2, alpha=0.8, capsize=10)

ax.set_xticks(x_pos)
ax.set_xticklabels(quarters, fontsize=12)
ax.set_xlabel('Quarter', fontsize=14, fontweight='bold')
ax.set_ylabel('Average Filled Jobs', fontsize=14, fontweight='bold')
ax.set_title('Quarterly Seasonality Pattern in Employment', fontsize=18, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for i, (bar, value) in enumerate(zip(bars, quarterly_pattern['mean'].values)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(value):,}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
chart8_path = './blackbox-analysis/visualization/08_quarterly_seasonality.png'
plt.savefig(chart8_path, dpi=300, bbox_inches='tight')
plt.close()
chart_paths.append(chart8_path)
print(f"   ✅ Saved: {chart8_path}")

# ============================================================================
# CHART 9: Top 10 Regions Employment Trends
# ============================================================================
print("\n📊 Creating Chart 9: Top Regions Employment Trends...")

region_jobs = df_clean[(df_clean['Group'] == 'Region by employment variable') & 
                       (df_clean['Series_title_1'] == 'Filled jobs') &
                       (df_clean['Series_title_3'] == 'Actual')]

# Get top 10 regions by average employment
top_regions = region_jobs.groupby('Series_title_2')['Data_value'].mean().nlargest(10).index

fig, ax = plt.subplots(figsize=(16, 10))
for region in top_regions:
    region_data = region_jobs[region_jobs['Series_title_2'] == region].sort_values('Period')
    ax.plot(region_data['Period'], region_data['Data_value'], 
            marker='o', linewidth=2, markersize=4, label=region, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Filled Jobs', fontsize=14, fontweight='bold')
ax.set_title('Employment Trends - Top 10 Regions (2011-2025)', fontsize=18, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10, framealpha=0.9, ncol=2)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
chart9_path = './blackbox-analysis/visualization/09_top_regions_trends.png'
plt.savefig(chart9_path, dpi=300, bbox_inches='tight')
plt.close()
chart_paths.append(chart9_path)
print(f"   ✅ Saved: {chart9_path}")

# ============================================================================
# CHART 10: Earnings vs Employment Correlation
# ============================================================================
print("\n📊 Creating Chart 10: Earnings vs Employment Analysis...")

# Get industry data for both metrics
industries_with_both = []
for industry in industry_jobs['Series_title_2'].unique():
    jobs_data = industry_jobs[industry_jobs['Series_title_2'] == industry]
    earnings_data = earnings_industry[earnings_industry['Series_title_2'] == industry]
    
    if len(jobs_data) > 0 and len(earnings_data) > 0:
        avg_jobs = jobs_data['Data_value'].mean()
        avg_earnings = earnings_data['Data_value'].mean()
        industries_with_both.append({
            'Industry': industry,
            'Avg_Jobs': avg_jobs,
            'Avg_Earnings': avg_earnings
        })

if len(industries_with_both) > 0:
    corr_df = pd.DataFrame(industries_with_both)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    scatter = ax.scatter(corr_df['Avg_Jobs'], corr_df['Avg_Earnings'], 
                        s=300, alpha=0.6, c=range(len(corr_df)), cmap='viridis',
                        edgecolors='black', linewidth=2)
    
    # Add labels for each point
    for idx, row in corr_df.iterrows():
        ax.annotate(row['Industry'], (row['Avg_Jobs'], row['Avg_Earnings']),
                   fontsize=9, ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel('Average Filled Jobs', fontsize=14, fontweight='bold')
    ax.set_ylabel('Average Total Earnings (Millions)', fontsize=14, fontweight='bold')
    ax.set_title('Employment vs Earnings by Industry', fontsize=18, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    chart10_path = './blackbox-analysis/visualization/10_earnings_vs_employment.png'
    plt.savefig(chart10_path, dpi=300, bbox_inches='tight')
    plt.close()
    chart_paths.append(chart10_path)
    print(f"   ✅ Saved: {chart10_path}")

print(f"\n✅ Created {len(chart_paths)} visualizations successfully!")
print("\n📊 Chart files saved in: ./blackbox-analysis/visualization/")