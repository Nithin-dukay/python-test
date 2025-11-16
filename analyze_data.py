#!/usr/bin/env python3
"""
Employment Data Analysis Script
Analyzes the complete employment-data.csv file iteratively
"""

import csv
import json
from collections import defaultdict, Counter
from datetime import datetime
import os

# File paths
INPUT_FILE = '/vercel/sandbox/uploads/employment-data.csv'
OUTPUT_DIR = '/vercel/sandbox/blackbox-analysis'
INSIGHTS_FILE = os.path.join(OUTPUT_DIR, 'insights.json')
ANALYSIS_FILE = os.path.join(OUTPUT_DIR, 'analysis.md')

def load_complete_data():
    """Load and parse the complete CSV file"""
    print("Phase 1: Loading complete dataset...")
    
    data = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    print(f"✓ Loaded {len(data)} rows")
    return data

def analyze_structure(data):
    """Phase 2: Analyze data structure and columns"""
    print("\nPhase 2: Analyzing data structure...")
    
    if not data:
        return {}
    
    # Get column names
    columns = list(data[0].keys())
    
    # Analyze each column
    column_analysis = {}
    for col in columns:
        values = [row[col] for row in data if row[col]]
        unique_values = set(values)
        
        column_analysis[col] = {
            'total_values': len(values),
            'unique_count': len(unique_values),
            'null_count': len(data) - len(values),
            'sample_values': list(unique_values)[:10] if len(unique_values) <= 10 else list(unique_values)[:5]
        }
    
    print(f"✓ Analyzed {len(columns)} columns")
    return {
        'total_rows': len(data),
        'columns': columns,
        'column_analysis': column_analysis
    }

def deep_analysis(data):
    """Phase 3: Deep analysis - patterns, statistics, groupings"""
    print("\nPhase 3: Performing deep analysis...")
    
    # Time period analysis
    periods = [row['Period'] for row in data if row['Period']]
    period_range = {
        'min': min(periods) if periods else None,
        'max': max(periods) if periods else None,
        'count': len(set(periods))
    }
    
    # Industry analysis
    industries = [row['Series_title_2'] for row in data if row['Series_title_2']]
    industry_counts = Counter(industries)
    
    # Group analysis
    groups = [row['Group'] for row in data if row['Group']]
    group_counts = Counter(groups)
    
    # Series type analysis (Actual, Seasonally adjusted, Trend)
    series_types = [row['Series_title_3'] for row in data if row['Series_title_3']]
    series_type_counts = Counter(series_types)
    
    # Employment variable analysis
    employment_vars = [row['Series_title_1'] for row in data if row['Series_title_1']]
    employment_var_counts = Counter(employment_vars)
    
    # Data value statistics (for numeric values)
    numeric_values = []
    suppressed_count = 0
    for row in data:
        if row['Data_value']:
            try:
                numeric_values.append(float(row['Data_value']))
            except ValueError:
                pass
        if row['Suppressed'] == 'Y':
            suppressed_count += 1
    
    value_stats = {}
    if numeric_values:
        numeric_values.sort()
        n = len(numeric_values)
        value_stats = {
            'count': n,
            'min': numeric_values[0],
            'max': numeric_values[-1],
            'mean': sum(numeric_values) / n,
            'median': numeric_values[n//2] if n % 2 == 1 else (numeric_values[n//2-1] + numeric_values[n//2]) / 2
        }
    
    print(f"✓ Analyzed {len(set(industries))} industries")
    print(f"✓ Analyzed {len(set(periods))} time periods")
    
    return {
        'period_range': period_range,
        'industries': dict(industry_counts.most_common(20)),
        'groups': dict(group_counts),
        'series_types': dict(series_type_counts),
        'employment_variables': dict(employment_var_counts),
        'value_statistics': value_stats,
        'suppressed_data_count': suppressed_count
    }

def detect_patterns(data):
    """Phase 4: Detect patterns and trends"""
    print("\nPhase 4: Detecting patterns and trends...")
    
    # Group data by industry and time
    industry_time_data = defaultdict(lambda: defaultdict(list))
    
    for row in data:
        if row['Data_value'] and row['Series_title_2'] and row['Period'] and row['Series_title_3'] == 'Actual':
            try:
                value = float(row['Data_value'])
                industry = row['Series_title_2']
                period = row['Period']
                industry_time_data[industry][period].append(value)
            except ValueError:
                pass
    
    # Calculate trends for top industries
    trends = {}
    for industry, periods in list(industry_time_data.items())[:10]:
        sorted_periods = sorted(periods.keys())
        if len(sorted_periods) >= 2:
            first_period_avg = sum(periods[sorted_periods[0]]) / len(periods[sorted_periods[0]])
            last_period_avg = sum(periods[sorted_periods[-1]]) / len(periods[sorted_periods[-1]])
            
            change = last_period_avg - first_period_avg
            pct_change = (change / first_period_avg * 100) if first_period_avg > 0 else 0
            
            trends[industry] = {
                'first_period': sorted_periods[0],
                'last_period': sorted_periods[-1],
                'first_value': round(first_period_avg, 2),
                'last_value': round(last_period_avg, 2),
                'absolute_change': round(change, 2),
                'percent_change': round(pct_change, 2)
            }
    
    print(f"✓ Detected trends for {len(trends)} industries")
    
    return {
        'industry_trends': trends,
        'total_industries_analyzed': len(industry_time_data)
    }

def save_insights(insights):
    """Save insights to JSON file"""
    print("\nSaving insights to JSON...")
    
    with open(INSIGHTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Insights saved to {INSIGHTS_FILE}")

def generate_markdown_report(insights):
    """Generate comprehensive markdown analysis report"""
    print("\nGenerating markdown analysis report...")
    
    report = []
    report.append("# Employment Data Analysis Report\n")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("---\n\n")
    
    # Dataset Overview
    report.append("## 1. Dataset Overview\n\n")
    structure = insights.get('structure', {})
    report.append(f"- **Total Records:** {structure.get('total_rows', 0):,}\n")
    report.append(f"- **Columns:** {len(structure.get('columns', []))}\n")
    report.append(f"- **Data Source:** Business Data Collection - BDC (New Zealand)\n\n")
    
    # Column Information
    report.append("### Column Structure\n\n")
    report.append("| Column | Unique Values | Null Count | Sample Values |\n")
    report.append("|--------|---------------|------------|---------------|\n")
    
    col_analysis = structure.get('column_analysis', {})
    for col, info in col_analysis.items():
        sample = ', '.join(str(v) for v in info.get('sample_values', [])[:3])
        report.append(f"| {col} | {info.get('unique_count', 0):,} | {info.get('null_count', 0):,} | {sample}... |\n")
    
    report.append("\n")
    
    # Deep Analysis Results
    report.append("## 2. Data Analysis\n\n")
    deep = insights.get('deep_analysis', {})
    
    # Time Period
    report.append("### Time Period Coverage\n\n")
    period_range = deep.get('period_range', {})
    report.append(f"- **Start Period:** {period_range.get('min', 'N/A')}\n")
    report.append(f"- **End Period:** {period_range.get('max', 'N/A')}\n")
    report.append(f"- **Total Periods:** {period_range.get('count', 0):,}\n")
    report.append(f"- **Time Span:** {period_range.get('min', '')[:4]} - {period_range.get('max', '')[:4]}\n\n")
    
    # Employment Variables
    report.append("### Employment Variables\n\n")
    emp_vars = deep.get('employment_variables', {})
    for var, count in emp_vars.items():
        report.append(f"- **{var}:** {count:,} records\n")
    report.append("\n")
    
    # Series Types
    report.append("### Data Series Types\n\n")
    series_types = deep.get('series_types', {})
    for stype, count in series_types.items():
        report.append(f"- **{stype}:** {count:,} records\n")
    report.append("\n")
    
    # Value Statistics
    report.append("### Value Statistics\n\n")
    value_stats = deep.get('value_statistics', {})
    if value_stats:
        report.append(f"- **Count:** {value_stats.get('count', 0):,}\n")
        report.append(f"- **Minimum:** {value_stats.get('min', 0):,.2f}\n")
        report.append(f"- **Maximum:** {value_stats.get('max', 0):,.2f}\n")
        report.append(f"- **Mean:** {value_stats.get('mean', 0):,.2f}\n")
        report.append(f"- **Median:** {value_stats.get('median', 0):,.2f}\n")
    
    suppressed = deep.get('suppressed_data_count', 0)
    report.append(f"- **Suppressed Data Points:** {suppressed:,}\n\n")
    
    # Industries
    report.append("### Top Industries by Record Count\n\n")
    industries = deep.get('industries', {})
    report.append("| Industry | Record Count |\n")
    report.append("|----------|-------------|\n")
    for industry, count in list(industries.items())[:15]:
        report.append(f"| {industry} | {count:,} |\n")
    report.append("\n")
    
    # Groups
    report.append("### Data Groups\n\n")
    groups = deep.get('groups', {})
    for group, count in groups.items():
        report.append(f"- **{group}:** {count:,} records\n")
    report.append("\n")
    
    # Patterns and Trends
    report.append("## 3. Patterns and Trends\n\n")
    patterns = insights.get('patterns', {})
    
    report.append("### Industry Employment Trends (First vs Last Period)\n\n")
    trends = patterns.get('industry_trends', {})
    
    if trends:
        report.append("| Industry | Period Range | First Value | Last Value | Change | % Change |\n")
        report.append("|----------|--------------|-------------|------------|--------|----------|\n")
        
        # Sort by absolute change
        sorted_trends = sorted(trends.items(), key=lambda x: abs(x[1].get('absolute_change', 0)), reverse=True)
        
        for industry, trend in sorted_trends[:15]:
            first_val = trend.get('first_value', 0)
            last_val = trend.get('last_value', 0)
            change = trend.get('absolute_change', 0)
            pct = trend.get('percent_change', 0)
            period_range = f"{trend.get('first_period', '')} - {trend.get('last_period', '')}"
            
            change_sign = "+" if change >= 0 else ""
            pct_sign = "+" if pct >= 0 else ""
            
            report.append(f"| {industry} | {period_range} | {first_val:,.0f} | {last_val:,.0f} | {change_sign}{change:,.0f} | {pct_sign}{pct:.1f}% |\n")
    
    report.append("\n")
    
    # Key Findings
    report.append("## 4. Key Findings\n\n")
    
    # Growth industries
    if trends:
        growth_industries = [(k, v) for k, v in trends.items() if v.get('percent_change', 0) > 0]
        decline_industries = [(k, v) for k, v in trends.items() if v.get('percent_change', 0) < 0]
        
        growth_industries.sort(key=lambda x: x[1].get('percent_change', 0), reverse=True)
        decline_industries.sort(key=lambda x: x[1].get('percent_change', 0))
        
        report.append("### Growing Industries\n\n")
        for industry, trend in growth_industries[:5]:
            pct = trend.get('percent_change', 0)
            report.append(f"- **{industry}:** +{pct:.1f}% growth\n")
        
        report.append("\n### Declining Industries\n\n")
        for industry, trend in decline_industries[:5]:
            pct = trend.get('percent_change', 0)
            report.append(f"- **{industry}:** {pct:.1f}% decline\n")
    
    report.append("\n")
    
    # Data Quality
    report.append("## 5. Data Quality Notes\n\n")
    report.append(f"- **Suppressed Records:** {suppressed:,} ({(suppressed/structure.get('total_rows', 1)*100):.2f}%)\n")
    report.append("- **Data Types:** Includes Actual, Seasonally Adjusted, and Trend data\n")
    report.append("- **Frequency:** Quarterly data (periods in format YYYY.MM)\n")
    report.append("- **Coverage:** Multiple industries, age groups, and gender breakdowns\n\n")
    
    # Save report
    with open(ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        f.write(''.join(report))
    
    print(f"✓ Analysis report saved to {ANALYSIS_FILE}")

def main():
    """Main analysis pipeline"""
    print("=" * 60)
    print("EMPLOYMENT DATA COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    
    # Phase 1: Load data
    data = load_complete_data()
    
    # Phase 2: Analyze structure
    structure = analyze_structure(data)
    
    # Phase 3: Deep analysis
    deep_analysis_results = deep_analysis(data)
    
    # Phase 4: Pattern detection
    patterns = detect_patterns(data)
    
    # Combine all insights
    insights = {
        'structure': structure,
        'deep_analysis': deep_analysis_results,
        'patterns': patterns
    }
    
    # Save insights
    save_insights(insights)
    
    # Generate markdown report
    generate_markdown_report(insights)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\nOutputs:")
    print(f"  - JSON insights: {INSIGHTS_FILE}")
    print(f"  - Analysis report: {ANALYSIS_FILE}")
    print("\nNote: PDF visualization requires additional packages.")
    print("      The markdown report contains all analysis findings.")

if __name__ == '__main__':
    main()
