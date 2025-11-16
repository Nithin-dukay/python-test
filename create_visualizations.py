#!/usr/bin/env python3
"""
Create comprehensive visualizations for employment data
Uses only standard library to generate HTML-based visualizations
"""

import csv
import json
from collections import defaultdict, Counter
import os

INPUT_FILE = '/vercel/sandbox/uploads/employment-data.csv'
OUTPUT_DIR = '/vercel/sandbox/blackbox-analysis'
VIZ_DIR = os.path.join(OUTPUT_DIR, 'visualization')
HTML_FILE = os.path.join(OUTPUT_DIR, 'dashboard.html')

def load_data():
    """Load complete CSV data"""
    print("Loading data...")
    data = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    print(f"✓ Loaded {len(data)} rows")
    return data

def prepare_industry_trends(data):
    """Prepare industry employment trends over time"""
    print("Preparing industry trends...")
    
    # Filter for filled jobs, actual data only
    industry_data = defaultdict(lambda: defaultdict(float))
    
    for row in data:
        if (row['Series_title_1'] == 'Filled jobs' and 
            row['Series_title_3'] == 'Actual' and 
            row['Data_value'] and
            row['Group'] == 'Industry by employment variable'):
            try:
                value = float(row['Data_value'])
                industry = row['Series_title_2']
                period = row['Period']
                industry_data[industry][period] = value
            except ValueError:
                pass
    
    return industry_data

def prepare_gender_trends(data):
    """Prepare gender employment trends"""
    print("Preparing gender trends...")
    
    gender_data = defaultdict(lambda: defaultdict(float))
    
    for row in data:
        if (row['Series_title_1'] == 'Filled jobs' and 
            row['Series_title_3'] == 'Actual' and 
            row['Data_value'] and
            row['Group'] == 'Sex by employment variable'):
            try:
                value = float(row['Data_value'])
                gender = row['Series_title_2']
                period = row['Period']
                gender_data[gender][period] = value
            except ValueError:
                pass
    
    return gender_data

def prepare_age_distribution(data):
    """Prepare age group distribution"""
    print("Preparing age distribution...")
    
    age_data = defaultdict(lambda: defaultdict(float))
    
    for row in data:
        if (row['Series_title_1'] == 'Filled jobs' and 
            row['Series_title_3'] == 'Actual' and 
            row['Data_value'] and
            row['Group'] == 'Age by employment variable'):
            try:
                value = float(row['Data_value'])
                age_group = row['Series_title_2']
                period = row['Period']
                age_data[age_group][period] = value
            except ValueError:
                pass
    
    return age_data

def prepare_earnings_data(data):
    """Prepare total earnings data"""
    print("Preparing earnings data...")
    
    earnings_data = defaultdict(lambda: defaultdict(float))
    
    for row in data:
        if (row['Series_title_1'] == 'Total earnings' and 
            row['Series_title_3'] == 'Actual' and 
            row['Data_value'] and
            row['Group'] == 'Industry by employment variable'):
            try:
                value = float(row['Data_value'])
                industry = row['Series_title_2']
                period = row['Period']
                # Magnitude 6 means millions
                if row['Magnitude'] == '6':
                    value = value  # Already in millions
                earnings_data[industry][period] = value
            except ValueError:
                pass
    
    return earnings_data

def create_html_dashboard(industry_data, gender_data, age_data, earnings_data):
    """Create interactive HTML dashboard with Chart.js"""
    print("Creating HTML dashboard...")
    
    # Prepare data for top 5 industries
    top_industries = sorted(industry_data.items(), 
                           key=lambda x: sum(x[1].values()), 
                           reverse=True)[:8]
    
    # Get all periods sorted
    all_periods = sorted(set(period for ind_data in industry_data.values() for period in ind_data.keys()))
    
    # Prepare industry chart data
    industry_datasets = []
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF']
    
    for idx, (industry, periods) in enumerate(top_industries):
        values = [periods.get(p, 0) for p in all_periods]
        industry_datasets.append({
            'label': industry,
            'data': values,
            'borderColor': colors[idx % len(colors)],
            'backgroundColor': colors[idx % len(colors)] + '33',
            'tension': 0.4
        })
    
    # Prepare gender chart data
    gender_datasets = []
    gender_colors = {'Male': '#36A2EB', 'Female': '#FF6384'}
    
    for gender, periods in gender_data.items():
        values = [periods.get(p, 0) for p in all_periods]
        gender_datasets.append({
            'label': gender,
            'data': values,
            'borderColor': gender_colors.get(gender, '#999'),
            'backgroundColor': gender_colors.get(gender, '#999') + '33',
            'tension': 0.4
        })
    
    # Prepare age distribution for latest period
    latest_period = all_periods[-1] if all_periods else None
    age_labels = []
    age_values = []
    
    if latest_period:
        for age_group, periods in sorted(age_data.items()):
            if latest_period in periods:
                age_labels.append(age_group)
                age_values.append(periods[latest_period])
    
    # Prepare earnings data for top industries
    top_earnings_industries = sorted(earnings_data.items(), 
                                    key=lambda x: sum(x[1].values()), 
                                    reverse=True)[:6]
    
    earnings_datasets = []
    for idx, (industry, periods) in enumerate(top_earnings_industries):
        values = [periods.get(p, 0) for p in all_periods]
        earnings_datasets.append({
            'label': industry,
            'data': values,
            'borderColor': colors[idx % len(colors)],
            'backgroundColor': colors[idx % len(colors)] + '33',
            'tension': 0.4
        })
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employment Data Analysis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .subtitle {{
            color: rgba(255,255,255,0.9);
            text-align: center;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .chart-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        canvas {{
            max-height: 400px;
        }}
        
        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
        }}
        
        @media (max-width: 768px) {{
            .grid-2 {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Employment Data Analysis Dashboard</h1>
        <p class="subtitle">New Zealand Business Data Collection (2011-2025)</p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">20,108</div>
                <div class="stat-label">Total Records</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">57</div>
                <div class="stat-label">Time Periods</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">106</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">14 Years</div>
                <div class="stat-label">Data Span</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h2 class="chart-title">Industry Employment Trends (Top 8 Industries)</h2>
            <canvas id="industryChart"></canvas>
        </div>
        
        <div class="grid-2">
            <div class="chart-container">
                <h2 class="chart-title">Employment by Gender</h2>
                <canvas id="genderChart"></canvas>
            </div>
            
            <div class="chart-container">
                <h2 class="chart-title">Age Distribution (Latest Period: {latest_period})</h2>
                <canvas id="ageChart"></canvas>
            </div>
        </div>
        
        <div class="chart-container">
            <h2 class="chart-title">Total Earnings by Industry (Top 6)</h2>
            <canvas id="earningsChart"></canvas>
        </div>
    </div>
    
    <script>
        // Industry Chart
        const industryCtx = document.getElementById('industryChart').getContext('2d');
        new Chart(industryCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(all_periods)},
                datasets: {json.dumps(industry_datasets)}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }},
                    title: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }}
                    }},
                    x: {{
                        ticks: {{
                            maxRotation: 45,
                            minRotation: 45
                        }}
                    }}
                }}
            }}
        }});
        
        // Gender Chart
        const genderCtx = document.getElementById('genderChart').getContext('2d');
        new Chart(genderCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(all_periods)},
                datasets: {json.dumps(gender_datasets)}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }}
                    }},
                    x: {{
                        ticks: {{
                            maxRotation: 45,
                            minRotation: 45
                        }}
                    }}
                }}
            }}
        }});
        
        // Age Chart
        const ageCtx = document.getElementById('ageChart').getContext('2d');
        new Chart(ageCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(age_labels)},
                datasets: [{{
                    label: 'Filled Jobs',
                    data: {json.dumps(age_values)},
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40',
                        '#FF6384',
                        '#C9CBCF'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Earnings Chart
        const earningsCtx = document.getElementById('earningsChart').getContext('2d');
        new Chart(earningsCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(all_periods)},
                datasets: {json.dumps(earnings_datasets)}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.dataset.label || '';
                                if (label) {{
                                    label += ': ';
                                }}
                                label += '$' + context.parsed.y.toLocaleString() + 'M';
                                return label;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toLocaleString() + 'M';
                            }}
                        }}
                    }},
                    x: {{
                        ticks: {{
                            maxRotation: 45,
                            minRotation: 45
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Dashboard created: {HTML_FILE}")

def create_detailed_statistics(data):
    """Create detailed statistical analysis"""
    print("\nCreating detailed statistics...")
    
    stats = {
        'overview': {},
        'by_industry': {},
        'by_period': {},
        'by_gender': {},
        'by_age': {}
    }
    
    # Overall statistics
    total_records = len(data)
    filled_jobs_records = sum(1 for row in data if row['Series_title_1'] == 'Filled jobs')
    earnings_records = sum(1 for row in data if row['Series_title_1'] == 'Total earnings')
    
    stats['overview'] = {
        'total_records': total_records,
        'filled_jobs_records': filled_jobs_records,
        'earnings_records': earnings_records,
        'data_types': {
            'actual': sum(1 for row in data if row['Series_title_3'] == 'Actual'),
            'seasonally_adjusted': sum(1 for row in data if row['Series_title_3'] == 'Seasonally adjusted'),
            'trend': sum(1 for row in data if row['Series_title_3'] == 'Trend')
        }
    }
    
    # Industry statistics
    industry_stats = defaultdict(lambda: {'count': 0, 'total_value': 0, 'periods': set()})
    
    for row in data:
        if row['Series_title_2'] and row['Data_value'] and row['Series_title_3'] == 'Actual':
            industry = row['Series_title_2']
            try:
                value = float(row['Data_value'])
                industry_stats[industry]['count'] += 1
                industry_stats[industry]['total_value'] += value
                industry_stats[industry]['periods'].add(row['Period'])
            except ValueError:
                pass
    
    # Convert to serializable format
    for industry, data_dict in industry_stats.items():
        stats['by_industry'][industry] = {
            'record_count': data_dict['count'],
            'average_value': round(data_dict['total_value'] / data_dict['count'], 2) if data_dict['count'] > 0 else 0,
            'period_count': len(data_dict['periods'])
        }
    
    # Save statistics
    stats_file = os.path.join(OUTPUT_DIR, 'detailed_statistics.json')
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, default=str)
    
    print(f"✓ Statistics saved to {stats_file}")
    
    return stats

def main():
    """Main execution"""
    print("=" * 70)
    print("CREATING EMPLOYMENT DATA VISUALIZATIONS")
    print("=" * 70)
    
    # Load data
    data = load_data()
    
    # Prepare datasets
    industry_data = prepare_industry_trends(data)
    gender_data = prepare_gender_trends(data)
    age_data = prepare_age_distribution(data)
    earnings_data = prepare_earnings_data(data)
    
    # Create visualizations
    create_html_dashboard(industry_data, gender_data, age_data, earnings_data)
    
    # Create detailed statistics
    stats = create_detailed_statistics(data)
    
    print("\n" + "=" * 70)
    print("VISUALIZATION COMPLETE!")
    print("=" * 70)
    print(f"\nOutputs:")
    print(f"  - Interactive Dashboard: {HTML_FILE}")
    print(f"  - Detailed Statistics: {os.path.join(OUTPUT_DIR, 'detailed_statistics.json')}")
    print(f"\nOpen the dashboard in a browser to view interactive charts!")

if __name__ == '__main__':
    main()
