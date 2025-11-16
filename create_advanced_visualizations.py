"""
Advanced Visualizations for Employment Data
Creates additional sophisticated charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

print("=" * 80)
print("CREATING ADVANCED VISUALIZATIONS")
print("=" * 80)

# Load data
df = pd.read_csv('/vercel/sandbox/uploads/employment-data.csv')
df['Period'] = pd.to_numeric(df['Period'], errors='coerce')
df['Year'] = df['Period'].apply(lambda x: int(x) if pd.notna(x) else None)
df['Quarter'] = df['Period'].apply(lambda x: int((x % 1) * 100) if pd.notna(x) else None)
df_clean = df[(df['Suppressed'] != 'Y') & (df['Data_value'].notna())].copy()

# ============================================================================
# CHART 11: Industry Comparison - Box Plot
# ============================================================================
print("\n📊 Creating Chart 11: Industry Employment Distribution (Box Plot)...")

industry_jobs = df_clean[(df_clean['Group'] == 'Industry by employment variable') & 
                         (df_clean['Series_title_1'] == 'Filled jobs') &
                         (df_clean['Series_title_3'] == 'Actual')]

top_industries = industry_jobs.groupby('Series_title_2')['Data_value'].mean().nlargest(8).index
industry_subset = industry_jobs[industry_jobs['Series_title_2'].isin(top_industries)]

fig, ax = plt.subplots(figsize=(16, 10))
box_data = [industry_subset[industry_subset['Series_title_2'] == ind]['Data_value'].values 
            for ind in top_industries]

bp = ax.boxplot(box_data, labels=top_industries, patch_artist=True, 
                notch=True, showmeans=True)

# Color the boxes
colors = sns.color_palette('Set2', len(top_industries))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel('Industry', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Filled Jobs', fontsize=14, fontweight='bold')
ax.set_title('Employment Distribution by Industry (Box Plot)', fontsize=18, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/11_industry_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 11_industry_boxplot.png")

# ============================================================================
# CHART 12: Age Group Trends Over Time
# ============================================================================
print("\n📊 Creating Chart 12: Age Group Employment Trends...")

age_jobs = df_clean[(df_clean['Group'] == 'Age by employment variable') & 
                    (df_clean['Series_title_1'] == 'Filled jobs') &
                    (df_clean['Series_title_3'] == 'Actual')]

# Select key age groups
key_ages = ['20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54']
age_subset = age_jobs[age_jobs['Series_title_2'].isin(key_ages)]

fig, ax = plt.subplots(figsize=(16, 10))
for age in key_ages:
    age_data = age_subset[age_subset['Series_title_2'] == age].sort_values('Period')
    ax.plot(age_data['Period'], age_data['Data_value'], 
            marker='o', linewidth=2, markersize=4, label=age, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Filled Jobs', fontsize=14, fontweight='bold')
ax.set_title('Employment Trends by Age Group (2011-2025)', fontsize=18, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=11, framealpha=0.9, ncol=2)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/12_age_trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 12_age_trends.png")

# ============================================================================
# CHART 13: Data Type Comparison (Actual vs Seasonally Adjusted vs Trend)
# ============================================================================
print("\n📊 Creating Chart 13: Data Type Comparison...")

# Use total industry data
total_ind = industry_jobs[industry_jobs['Series_title_2'] == 'Total Industry']

fig, ax = plt.subplots(figsize=(16, 10))
for data_type in ['Actual', 'Seasonally adjusted', 'Trend']:
    type_data = total_ind[total_ind['Series_title_3'] == data_type].sort_values('Period')
    if len(type_data) > 0:
        ax.plot(type_data['Period'], type_data['Data_value'], 
                marker='o', linewidth=2.5, markersize=5, label=data_type, alpha=0.8)

ax.set_xlabel('Period (Year.Quarter)', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Filled Jobs', fontsize=14, fontweight='bold')
ax.set_title('Total Industry Employment: Actual vs Seasonally Adjusted vs Trend', 
             fontsize=18, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=12, framealpha=0.9)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/13_data_type_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 13_data_type_comparison.png")

# ============================================================================
# CHART 14: Employment Growth Rate by Industry
# ============================================================================
print("\n📊 Creating Chart 14: Employment Growth Rate by Industry...")

growth_data = []
for industry in industry_jobs['Series_title_2'].unique():
    ind_data = industry_jobs[(industry_jobs['Series_title_2'] == industry) & 
                             (industry_jobs['Series_title_3'] == 'Actual')].sort_values('Period')
    if len(ind_data) >= 2:
        first_val = ind_data.iloc[0]['Data_value']
        last_val = ind_data.iloc[-1]['Data_value']
        if first_val > 0:
            growth_rate = ((last_val - first_val) / first_val) * 100
            growth_data.append({
                'Industry': industry,
                'Growth_Rate': growth_rate,
                'First_Value': first_val,
                'Last_Value': last_val
            })

if len(growth_data) > 0:
    growth_df = pd.DataFrame(growth_data).sort_values('Growth_Rate', ascending=False)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    colors_list = ['green' if x > 0 else 'red' for x in growth_df['Growth_Rate']]
    bars = ax.barh(range(len(growth_df)), growth_df['Growth_Rate'].values, 
                   color=colors_list, edgecolor='black', linewidth=1.5, alpha=0.7)
    
    ax.set_yticks(range(len(growth_df)))
    ax.set_yticklabels(growth_df['Industry'].values, fontsize=11)
    ax.set_xlabel('Growth Rate (%)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Industry', fontsize=14, fontweight='bold')
    ax.set_title('Employment Growth Rate by Industry (2011-2025)', fontsize=18, fontweight='bold', pad=20)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=2)
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, growth_df['Growth_Rate'].values)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f' {value:.1f}%', ha='left' if value > 0 else 'right', 
                va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/14_industry_growth_rates.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 14_industry_growth_rates.png")

# ============================================================================
# CHART 15: Regional Employment Heatmap
# ============================================================================
print("\n📊 Creating Chart 15: Regional Employment Heatmap...")

region_jobs = df_clean[(df_clean['Group'] == 'Region by employment variable') & 
                       (df_clean['Series_title_1'] == 'Filled jobs') &
                       (df_clean['Series_title_3'] == 'Actual')]

# Create pivot table for regions over years
region_pivot = region_jobs.pivot_table(values='Data_value', index='Series_title_2', 
                                        columns='Year', aggfunc='mean')

fig, ax = plt.subplots(figsize=(16, 12))
sns.heatmap(region_pivot, annot=True, fmt='.0f', cmap='RdYlGn', cbar_kws={'label': 'Filled Jobs'},
            linewidths=0.5, ax=ax, annot_kws={'fontsize': 7})
ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Region', fontsize=14, fontweight='bold')
ax.set_title('Regional Employment Heatmap Over Years', fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/15_regional_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 15_regional_heatmap.png")

# ============================================================================
# CHART 16: Earnings Trends by Industry
# ============================================================================
print("\n📊 Creating Chart 16: Earnings Trends by Industry...")

earnings_industry = df_clean[(df_clean['Group'] == 'Industry by employment variable') & 
                             (df_clean['Series_title_1'] == 'Total earnings') &
                             (df_clean['Series_title_3'] == 'Actual')]

if len(earnings_industry) > 0:
    top_earning_industries = earnings_industry.groupby('Series_title_2')['Data_value'].mean().nlargest(6).index
    
    fig, ax = plt.subplots(figsize=(16, 10))
    for industry in top_earning_industries:
        ind_data = earnings_industry[earnings_industry['Series_title_2'] == industry].sort_values('Period')
        ax.plot(ind_data['Period'], ind_data['Data_value'], 
                marker='o', linewidth=2.5, markersize=5, label=industry, alpha=0.8)
    
    ax.set_xlabel('Period (Year.Quarter)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Total Earnings (Millions)', fontsize=14, fontweight='bold')
    ax.set_title('Total Earnings Trends by Industry (2011-2025)', fontsize=18, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/16_earnings_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 16_earnings_trends.png")

# ============================================================================
# CHART 17: Employment Composition by Group
# ============================================================================
print("\n📊 Creating Chart 17: Employment Composition by Group...")

group_composition = df_clean[df_clean['Series_title_1'] == 'Filled jobs'].groupby('Group')['Data_value'].sum()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Pie chart
colors = sns.color_palette('pastel', len(group_composition))
wedges, texts, autotexts = ax1.pie(group_composition.values, labels=group_composition.index, 
                                     autopct='%1.1f%%', colors=colors, startangle=90,
                                     textprops={'fontsize': 9})
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
ax1.set_title('Employment Data Composition by Group', fontsize=16, fontweight='bold')

# Bar chart
bars = ax2.bar(range(len(group_composition)), group_composition.values, 
               color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
ax2.set_xticks(range(len(group_composition)))
ax2.set_xticklabels([g.replace(' by employment variable', '') for g in group_composition.index], 
                     rotation=45, ha='right', fontsize=10)
ax2.set_ylabel('Total Filled Jobs', fontsize=14, fontweight='bold')
ax2.set_title('Total Employment by Group Category', fontsize=16, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, value in zip(bars, group_composition.values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(value):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/17_group_composition.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 17_group_composition.png")

# ============================================================================
# CHART 18: Territorial Authority Top 20
# ============================================================================
print("\n📊 Creating Chart 18: Top 20 Territorial Authorities...")

ta_jobs = df_clean[(df_clean['Group'] == 'Territorial authority by employment variable') & 
                   (df_clean['Series_title_1'] == 'Filled jobs') &
                   (df_clean['Series_title_3'] == 'Actual')]

# Get top 20 TAs by average employment
top_tas = ta_jobs.groupby('Series_title_2')['Data_value'].mean().nlargest(20).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(14, 12))
colors = sns.color_palette('rocket', len(top_tas))
bars = ax.barh(range(len(top_tas)), top_tas.values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_yticks(range(len(top_tas)))
ax.set_yticklabels(top_tas.index, fontsize=10)
ax.set_xlabel('Average Filled Jobs', fontsize=14, fontweight='bold')
ax.set_ylabel('Territorial Authority', fontsize=14, fontweight='bold')
ax.set_title('Top 20 Territorial Authorities by Average Employment', fontsize=18, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for bar, value in zip(bars, top_tas.values):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f' {int(value):,}', ha='left', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/18_top_territorial_authorities.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 18_top_territorial_authorities.png")

# ============================================================================
# CHART 19: Quarterly Patterns by Industry
# ============================================================================
print("\n📊 Creating Chart 19: Quarterly Patterns by Industry...")

# Analyze quarterly patterns for top 4 industries
top_4_industries = industry_jobs.groupby('Series_title_2')['Data_value'].mean().nlargest(4).index

fig, axes = plt.subplots(2, 2, figsize=(18, 14))
axes = axes.flatten()

for idx, industry in enumerate(top_4_industries):
    ind_data = industry_jobs[industry_jobs['Series_title_2'] == industry]
    quarterly_avg = ind_data.groupby('Quarter')['Data_value'].agg(['mean', 'std'])
    
    quarters = ['Q1 (Mar)', 'Q2 (Jun)', 'Q3 (Sep)', 'Q4 (Dec)']
    x_pos = [3, 6, 9, 12]
    
    bars = axes[idx].bar(x_pos, quarterly_avg['mean'].values, 
                         yerr=quarterly_avg['std'].values,
                         color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
                         edgecolor='black', linewidth=1.5, alpha=0.8, capsize=8)
    
    axes[idx].set_xticks(x_pos)
    axes[idx].set_xticklabels(quarters, fontsize=10)
    axes[idx].set_xlabel('Quarter', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Average Filled Jobs', fontsize=12, fontweight='bold')
    axes[idx].set_title(f'{industry}', fontsize=14, fontweight='bold')
    axes[idx].grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, value in zip(bars, quarterly_avg['mean'].values):
        height = bar.get_height()
        axes[idx].text(bar.get_x() + bar.get_width()/2., height,
                      f'{int(value):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.suptitle('Quarterly Employment Patterns by Industry', fontsize=20, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('./blackbox-analysis/visualization/19_quarterly_patterns_by_industry.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 19_quarterly_patterns_by_industry.png")

# ============================================================================
# CHART 20: Multi-Panel Dashboard Summary
# ============================================================================
print("\n📊 Creating Chart 20: Multi-Panel Dashboard Summary...")

fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Panel 1: Total Employment Over Time
ax1 = fig.add_subplot(gs[0, :2])
total_emp = df_clean[(df_clean['Series_title_1'] == 'Filled jobs') & 
                     (df_clean['Series_title_3'] == 'Actual')].groupby('Period')['Data_value'].sum()
ax1.plot(total_emp.index, total_emp.values, linewidth=3, color='steelblue', marker='o', markersize=3)
ax1.fill_between(total_emp.index, total_emp.values, alpha=0.3, color='steelblue')
ax1.set_title('Total Employment Over Time', fontsize=14, fontweight='bold')
ax1.set_xlabel('Period', fontsize=11)
ax1.set_ylabel('Total Filled Jobs', fontsize=11)
ax1.grid(True, alpha=0.3)

# Panel 2: Latest Age Distribution
ax2 = fig.add_subplot(gs[0, 2])
age_latest = age_jobs[age_jobs['Period'] == age_jobs['Period'].max()].groupby('Series_title_2')['Data_value'].sum()
colors_pie = sns.color_palette('Set3', len(age_latest))
ax2.pie(age_latest.values, labels=None, autopct='%1.0f%%', colors=colors_pie, startangle=90,
        textprops={'fontsize': 7, 'fontweight': 'bold'})
ax2.set_title('Age Distribution', fontsize=12, fontweight='bold')

# Panel 3: Top 5 Industries
ax3 = fig.add_subplot(gs[1, :])
top_5_ind = industry_jobs[industry_jobs['Series_title_3'] == 'Actual'].groupby('Series_title_2')['Data_value'].mean().nlargest(5)
bars = ax3.bar(range(len(top_5_ind)), top_5_ind.values, 
               color=sns.color_palette('muted', len(top_5_ind)), edgecolor='black', linewidth=1.5)
ax3.set_xticks(range(len(top_5_ind)))
ax3.set_xticklabels(top_5_ind.index, rotation=30, ha='right', fontsize=10)
ax3.set_title('Top 5 Industries by Average Employment', fontsize=14, fontweight='bold')
ax3.set_ylabel('Average Filled Jobs', fontsize=11)
ax3.grid(True, alpha=0.3, axis='y')
for bar, value in zip(bars, top_5_ind.values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(value):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Panel 4: Sex Comparison
ax4 = fig.add_subplot(gs[2, 0])
sex_jobs = df_clean[(df_clean['Group'] == 'Sex by employment variable') & 
                    (df_clean['Series_title_1'] == 'Filled jobs') &
                    (df_clean['Series_title_3'] == 'Actual')]
sex_latest = sex_jobs[sex_jobs['Period'] == sex_jobs['Period'].max()].groupby('Series_title_2')['Data_value'].sum()
bars = ax4.bar(range(len(sex_latest)), sex_latest.values, color=['#3498db', '#e74c3c'], 
               edgecolor='black', linewidth=2, alpha=0.8)
ax4.set_xticks(range(len(sex_latest)))
ax4.set_xticklabels(sex_latest.index, fontsize=11)
ax4.set_title('Employment by Sex (Latest)', fontsize=12, fontweight='bold')
ax4.set_ylabel('Filled Jobs', fontsize=11)
ax4.grid(True, alpha=0.3, axis='y')
for bar, value in zip(bars, sex_latest.values):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(value):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Panel 5: Top 5 Regions
ax5 = fig.add_subplot(gs[2, 1:])
top_5_regions = region_jobs[region_jobs['Period'] == region_jobs['Period'].max()].groupby('Series_title_2')['Data_value'].sum().nlargest(5)
bars = ax5.barh(range(len(top_5_regions)), top_5_regions.values, 
                color=sns.color_palette('coolwarm', len(top_5_regions)), edgecolor='black', linewidth=1.5)
ax5.set_yticks(range(len(top_5_regions)))
ax5.set_yticklabels(top_5_regions.index, fontsize=10)
ax5.set_title('Top 5 Regions by Employment (Latest)', fontsize=12, fontweight='bold')
ax5.set_xlabel('Filled Jobs', fontsize=11)
ax5.grid(True, alpha=0.3, axis='x')
for bar, value in zip(bars, top_5_regions.values):
    width = bar.get_width()
    ax5.text(width, bar.get_y() + bar.get_height()/2.,
             f' {int(value):,}', ha='left', va='center', fontsize=9, fontweight='bold')

plt.suptitle('Employment Data Dashboard - Key Metrics Summary', fontsize=20, fontweight='bold', y=0.998)
plt.savefig('./blackbox-analysis/visualization/20_dashboard_summary.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 20_dashboard_summary.png")

print("\n" + "=" * 80)
print("✅ ALL ADVANCED VISUALIZATIONS CREATED SUCCESSFULLY!")
print("=" * 80)
