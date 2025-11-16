import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import json
from fpdf import FPDF
import numpy as np

def create_visualizations():
    """Create comprehensive visualizations for the employment data"""

    # Load data and insights
    df = pd.read_csv('/vercel/sandbox/uploads/employment-data.csv')
    with open('./blackbox-analysis/comprehensive_insights.json', 'r') as f:
        insights = json.load(f)

    # Create output directories
    os.makedirs('./blackbox-analysis/visualization', exist_ok=True)
    os.makedirs('./blackbox-analysis/pdfs', exist_ok=True)

    # Set style
    plt.style.use('default')
    sns.set_palette("husl")

    # 1. Data Overview Charts
    create_data_overview_charts(df, insights)

    # 2. Industry Analysis Charts
    create_industry_analysis_charts(df, insights)

    # 3. Temporal Analysis Charts
    create_temporal_analysis_charts(df, insights)

    # 4. Data Quality Charts
    create_data_quality_charts(df, insights)

    # 5. Statistical Distribution Charts
    create_statistical_charts(df, insights)

    # 6. Create PDF Report
    create_pdf_report()

    print("All visualizations created successfully!")
    print("PDF report saved to ./blackbox-analysis/pdfs/visualizations_report.pdf")

def create_data_overview_charts(df, insights):
    """Create data overview visualizations"""

    # Figure 1: Data Types Distribution
    fig1 = plt.figure(figsize=(12, 8))

    # Status distribution
    plt.subplot(2, 2, 1)
    status_data = insights['content_analysis']['status_distribution']['status_counts']
    plt.bar(status_data.keys(), status_data.values())
    plt.title('Data Status Distribution')
    plt.xlabel('Status')
    plt.ylabel('Count')

    # Units distribution
    plt.subplot(2, 2, 2)
    units_data = insights['content_analysis']['units_distribution']['units_counts']
    plt.bar(units_data.keys(), units_data.values())
    plt.title('Units Distribution')
    plt.xlabel('Units')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

    # Industries count
    plt.subplot(2, 2, 3)
    industries = insights['content_analysis']['industries']['list'][:15]  # Top 15
    industry_counts = df['Series_title_2'].value_counts()[:15]
    plt.barh(range(len(industries)), industry_counts.values)
    plt.yticks(range(len(industries)), [x[:30] + '...' if len(x) > 30 else x for x in industries])
    plt.title('Top 15 Industries by Record Count')
    plt.xlabel('Record Count')

    # Data types
    plt.subplot(2, 2, 4)
    data_types = df['Series_title_3'].value_counts()
    plt.pie(data_types.values, labels=data_types.index, autopct='%1.1f%%')
    plt.title('Data Types Distribution')

    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/data_overview.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_industry_analysis_charts(df, insights):
    """Create industry analysis visualizations"""

    # Figure 2: Industry Data Types
    industry_type_data = insights['content_analysis']['industries']['data_types_per_industry']

    # Create a summary chart
    industry_df = pd.DataFrame(industry_type_data)
    pivot_table = industry_df.pivot_table(index='Series_title_2', columns='Series_title_3', values='count', aggfunc='sum', fill_value=0)

    fig2, ax = plt.subplots(figsize=(14, 10))
    pivot_table.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Data Types by Industry')
    plt.xlabel('Industry')
    plt.ylabel('Record Count')
    plt.legend(title='Data Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/industry_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Figure 3: Industry Value Ranges
    industry_stats = df.groupby('Series_title_2')['Data_value'].agg(['min', 'max', 'mean', 'count']).reset_index()
    industry_stats['Data_value'] = pd.to_numeric(industry_stats['Data_value'], errors='coerce')

    fig3, ax = plt.subplots(figsize=(14, 8))
    industries_short = [x[:25] + '...' if len(x) > 25 else x for x in industry_stats['Series_title_2']]
    ax.barh(range(len(industry_stats)), industry_stats['max'] - industry_stats['min'],
            left=industry_stats['min'], height=0.8)
    ax.set_yticks(range(len(industry_stats)))
    ax.set_yticklabels(industries_short)
    plt.title('Value Ranges by Industry')
    plt.xlabel('Data Value Range')
    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/industry_value_ranges.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_temporal_analysis_charts(df, insights):
    """Create temporal analysis visualizations"""

    # Prepare time data
    df['Year'] = df['Period'].str.split('.').str[0].astype(int)
    df['Quarter'] = df['Period'].str.split('.').str[1]

    # Figure 4: Records by Year
    yearly_counts = df.groupby('Year').size().reset_index(name='count')

    fig4, ax = plt.subplots(figsize=(12, 6))
    ax.plot(yearly_counts['Year'], yearly_counts['count'], marker='o', linewidth=2)
    ax.set_title('Records by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Records')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/temporal_yearly.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Figure 5: Quarterly Distribution
    quarterly_counts = df.groupby('Quarter').size().reset_index(name='count')

    fig5, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(quarterly_counts['Quarter'], quarterly_counts['count'])
    ax.set_title('Records by Quarter')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Number of Records')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/temporal_quarterly.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_data_quality_charts(df, insights):
    """Create data quality visualizations"""

    # Figure 6: Data Quality Overview
    fig6, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # Null values
    null_data = insights['data_quality']['completeness']['null_values']
    columns = list(null_data.keys())
    nulls = list(null_data.values())
    ax1.bar(columns, nulls)
    ax1.set_title('Null Values by Column')
    ax1.set_ylabel('Count')
    ax1.tick_params(axis='x', rotation=45)

    # Missing periods (if any)
    missing_periods = insights['data_quality']['completeness']['missing_periods']
    if missing_periods:
        ax2.text(0.5, 0.5, f'{len(missing_periods)} Missing Periods', transform=ax2.transAxes, ha='center', va='center', fontsize=14)
    else:
        ax2.text(0.5, 0.5, 'No Missing Periods', transform=ax2.transAxes, ha='center', va='center', fontsize=14)
    ax2.set_title('Period Completeness')

    # Anomalies
    anomalies = insights['data_quality']['anomalies']
    anomaly_labels = ['Negative Values', 'Extreme High Values']
    anomaly_counts = [anomalies['negative_values']['count'], anomalies['extreme_values']['count']]
    ax3.bar(anomaly_labels, anomaly_counts)
    ax3.set_title('Data Anomalies')
    ax3.set_ylabel('Count')

    # Industry completeness
    incomplete_data = insights['data_quality']['completeness']['incomplete_industries']
    if incomplete_data['industries_with_incomplete_data']:
        ax4.text(0.5, 0.5, f"{incomplete_data['incomplete_count']} Industries\nwith Incomplete Data",
                transform=ax4.transAxes, ha='center', va='center', fontsize=14)
    else:
        ax4.text(0.5, 0.5, 'All Industries Complete', transform=ax4.transAxes, ha='center', va='center', fontsize=14)
    ax4.set_title('Industry Completeness')

    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/data_quality.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_statistical_charts(df, insights):
    """Create statistical distribution charts"""

    # Convert data values to numeric
    df['Data_value_numeric'] = pd.to_numeric(df['Data_value'], errors='coerce')

    # Figure 7: Value Distribution
    fig7, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # Histogram
    valid_data = df['Data_value_numeric'].dropna()
    ax1.hist(valid_data, bins=50, alpha=0.7, edgecolor='black')
    ax1.set_title('Data Value Distribution')
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Frequency')
    ax1.axvline(valid_data.mean(), color='red', linestyle='--', label=f'Mean: {valid_data.mean():.0f}')
    ax1.legend()

    # Box plot
    ax2.boxplot(valid_data, vert=False)
    ax2.set_title('Data Value Box Plot')
    ax2.set_xlabel('Value')

    # Q-Q plot approximation
    sorted_data = np.sort(valid_data)
    theoretical_quantiles = np.linspace(0, 1, len(sorted_data))
    ax3.scatter(theoretical_quantiles, sorted_data, alpha=0.5, s=1)
    ax3.plot([0, 1], [sorted_data.min(), sorted_data.max()], 'r--', alpha=0.7)
    ax3.set_title('Q-Q Plot (vs Uniform)')
    ax3.set_xlabel('Theoretical Quantiles')
    ax3.set_ylabel('Sample Quantiles')

    # Cumulative distribution
    ax4.hist(valid_data, bins=50, cumulative=True, density=True, alpha=0.7, edgecolor='black')
    ax4.set_title('Cumulative Distribution')
    ax4.set_xlabel('Value')
    ax4.set_ylabel('Cumulative Probability')

    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/statistical_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Figure 8: Statistics Summary
    fig8, ax = plt.subplots(figsize=(10, 6))
    stats_labels = ['Mean', 'Median', 'Min', 'Max', 'Std Dev']
    stats_values = [
        insights['statistical_summary']['data_value_statistics']['mean'],
        insights['statistical_summary']['data_value_statistics']['median'],
        insights['statistical_summary']['data_value_statistics']['min'],
        insights['statistical_summary']['data_value_statistics']['max'],
        insights['statistical_summary']['data_value_statistics']['std']
    ]

    ax.bar(stats_labels, stats_values)
    ax.set_title('Key Statistics Summary')
    ax.set_ylabel('Value')

    # Add value labels
    for i, v in enumerate(stats_values):
        ax.text(i, v + max(stats_values) * 0.01, f'{v:,.0f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('./blackbox-analysis/visualization/statistics_summary.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_pdf_report():
    """Create a PDF report with all visualizations"""

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title page
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "Employment Data Analysis Report", ln=True, align='C')
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "Comprehensive Visual Analysis", ln=True, align='C')
    pdf.cell(0, 10, f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')

    # Overview page
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "1. Data Overview", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, "This report provides a comprehensive analysis of the employment dataset.", ln=True)
    pdf.cell(0, 8, "The following visualizations show key insights and patterns.", ln=True)

    # Add visualizations
    visualization_files = [
        ('./blackbox-analysis/visualization/data_overview.png', 'Data Overview'),
        ('./blackbox-analysis/visualization/industry_analysis.png', 'Industry Analysis'),
        ('./blackbox-analysis/visualization/industry_value_ranges.png', 'Industry Value Ranges'),
        ('./blackbox-analysis/visualization/temporal_yearly.png', 'Temporal Analysis - Yearly'),
        ('./blackbox-analysis/visualization/temporal_quarterly.png', 'Temporal Analysis - Quarterly'),
        ('./blackbox-analysis/visualization/data_quality.png', 'Data Quality Assessment'),
        ('./blackbox-analysis/visualization/statistical_distribution.png', 'Statistical Distributions'),
        ('./blackbox-analysis/visualization/statistics_summary.png', 'Statistics Summary')
    ]

    for img_path, title in visualization_files:
        if os.path.exists(img_path):
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 12, title, ln=True)
            pdf.image(img_path, x=10, y=30, w=180)

    # Save PDF
    pdf.output('./blackbox-analysis/pdfs/visualizations_report.pdf')

if __name__ == "__main__":
    create_visualizations()