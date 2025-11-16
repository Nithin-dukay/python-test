import pandas as pd
import numpy as np
import json
import os
from collections import Counter

def phase1_analysis():
    """Phase 1: Load complete file and discover structure"""

    # Load the complete CSV file
    file_path = '/vercel/sandbox/uploads/employment-data.csv'
    df = pd.read_csv(file_path)

    # Basic structure discovery
    structure_info = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'column_names': list(df.columns),
        'data_types': df.dtypes.to_dict(),
        'null_counts': df.isnull().sum().to_dict(),
        'unique_values_per_column': {}
    }

    # Get unique values for key columns (limit to avoid too much output)
    for col in df.columns:
        unique_vals = df[col].unique()
        if len(unique_vals) <= 20:  # Only show if reasonable number
            structure_info['unique_values_per_column'][col] = unique_vals.tolist()
        else:
            structure_info['unique_values_per_column'][col] = f"{len(unique_vals)} unique values (too many to list)"

    # Sample data from beginning, middle, and end
    sample_data = {
        'first_5_rows': df.head(5).to_dict('records'),
        'middle_rows': df.iloc[len(df)//2:len(df)//2+5].to_dict('records'),
        'last_5_rows': df.tail(5).to_dict('records')
    }

    # Basic statistics for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    stats = {}
    for col in numeric_cols:
        stats[col] = {
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'min': float(df[col].min()),
            'max': float(df[col].max()),
            'std': float(df[col].std())
        }

    # Save phase 1 results
    phase1_results = {
        'structure_info': structure_info,
        'sample_data': sample_data,
        'basic_stats': stats
    }

    # Create output directory
    os.makedirs('./blackbox-analysis', exist_ok=True)

    # Save to JSON
    with open('./blackbox-analysis/phase1_structure.json', 'w') as f:
        json.dump(phase1_results, f, indent=2, default=str)

    print("Phase 1 Analysis Complete!")
    print(f"Total rows: {structure_info['total_rows']}")
    print(f"Total columns: {structure_info['total_columns']}")
    print(f"Column names: {structure_info['column_names']}")

    return df, phase1_results

def phase2_analysis(df):
    """Phase 2: Deep analysis with unique values, stats, patterns"""

    # Load phase 1 results
    with open('./blackbox-analysis/phase1_structure.json', 'r') as f:
        phase1_data = json.load(f)

    # Deep analysis of key columns
    analysis_results = {}

    # Analyze Series_reference patterns
    series_refs = df['Series_reference'].unique()
    analysis_results['series_reference_patterns'] = {
        'total_unique': len(series_refs),
        'sample_series': series_refs[:10].tolist(),
        'pattern_breakdown': {}
    }

    # Break down series reference patterns
    prefixes = [ref.split('.')[0] for ref in series_refs]
    suffixes = [ref.split('.')[1] for ref in series_refs]

    analysis_results['series_reference_patterns']['prefixes'] = list(set(prefixes))
    analysis_results['series_reference_patterns']['suffixes'] = list(set(suffixes))

    # Analyze Period column
    periods = df['Period'].unique()
    analysis_results['period_analysis'] = {
        'total_unique_periods': len(periods),
        'sample_periods': sorted(periods)[:20],
        'year_range': {
            'min_year': min([int(p.split('.')[0]) for p in periods]),
            'max_year': max([int(p.split('.')[0]) for p in periods])
        },
        'quarters': sorted(list(set([p.split('.')[1] for p in periods])))
    }

    # Analyze Data_value column
    data_values = pd.to_numeric(df['Data_value'], errors='coerce')
    analysis_results['data_value_analysis'] = {
        'total_valid_values': data_values.notna().sum(),
        'total_null_values': data_values.isna().sum(),
        'statistics': {
            'mean': float(data_values.mean()),
            'median': float(data_values.median()),
            'min': float(data_values.min()),
            'max': float(data_values.max()),
            'std': float(data_values.std())
        },
        'distribution': {
            'q25': float(data_values.quantile(0.25)),
            'q75': float(data_values.quantile(0.75)),
            'q90': float(data_values.quantile(0.90)),
            'q95': float(data_values.quantile(0.95))
        }
    }

    # Analyze STATUS column
    status_counts = df['STATUS'].value_counts().to_dict()
    analysis_results['status_analysis'] = {
        'status_counts': status_counts,
        'status_percentages': {k: f"{v/len(df)*100:.2f}%" for k, v in status_counts.items()}
    }

    # Analyze UNITS column
    units_counts = df['UNITS'].value_counts().to_dict()
    analysis_results['units_analysis'] = {
        'units_counts': units_counts,
        'units_percentages': {k: f"{v/len(df)*100:.2f}%" for k, v in units_counts.items()}
    }

    # Analyze Subject, Group, Series_title columns
    analysis_results['categorical_analysis'] = {
        'subject_unique': df['Subject'].unique().tolist(),
        'group_unique': df['Group'].unique().tolist(),
        'series_title_1_unique': df['Series_title_1'].unique().tolist(),
        'series_title_2_unique': sorted(df['Series_title_2'].unique().tolist()),
        'series_title_3_unique': df['Series_title_3'].unique().tolist()
    }

    # Find patterns and groupings
    analysis_results['groupings'] = {}

    # Group by industry and data type
    industry_groups = df.groupby(['Series_title_2', 'Series_title_3']).size().reset_index(name='count')
    analysis_results['groupings']['industry_by_type'] = industry_groups.to_dict('records')

    # Group by period and industry (sample)
    period_industry = df.groupby(['Period', 'Series_title_2']).size().reset_index(name='count')
    analysis_results['groupings']['period_industry_sample'] = period_industry.head(20).to_dict('records')

    # Save phase 2 results
    phase2_results = {
        'analysis_results': analysis_results,
        'phase1_summary': {
            'total_rows': phase1_data['structure_info']['total_rows'],
            'total_columns': phase1_data['structure_info']['total_columns']
        }
    }

    with open('./blackbox-analysis/phase2_analysis.json', 'w') as f:
        json.dump(phase2_results, f, indent=2, default=str)

    print("Phase 2 Analysis Complete!")
    print(f"Found {len(series_refs)} unique series references")
    print(f"Data spans from {analysis_results['period_analysis']['year_range']['min_year']} to {analysis_results['period_analysis']['year_range']['max_year']}")
    print(f"Data values range from {analysis_results['data_value_analysis']['statistics']['min']:.0f} to {analysis_results['data_value_analysis']['statistics']['max']:.0f}")

    return analysis_results

def phase3_analysis(df):
    """Phase 3: Detect structure changes and find groupings"""

    # Load previous results
    with open('./blackbox-analysis/phase2_analysis.json', 'r') as f:
        phase2_data = json.load(f)

    structure_changes = {}

    # Check for data consistency across periods
    periods = sorted(df['Period'].unique())
    structure_changes['period_consistency'] = {
        'total_periods': len(periods),
        'expected_quarters': ['03', '06', '09', '12'],
        'missing_periods': []
    }

    # Check for missing periods
    years = sorted(list(set([p.split('.')[0] for p in periods])))
    for year in years:
        for quarter in ['03', '06', '09', '12']:
            period = f"{year}.{quarter}"
            if period not in periods:
                structure_changes['period_consistency']['missing_periods'].append(period)

    # Analyze data value patterns by industry
    industries = df['Series_title_2'].unique()
    structure_changes['industry_patterns'] = {}

    for industry in industries:
        industry_data = df[df['Series_title_2'] == industry]
        data_types = industry_data['Series_title_3'].unique()

        structure_changes['industry_patterns'][industry] = {
            'data_types': data_types.tolist(),
            'record_count': len(industry_data),
            'period_coverage': len(industry_data['Period'].unique()),
            'value_range': {
                'min': float(pd.to_numeric(industry_data['Data_value'], errors='coerce').min()),
                'max': float(pd.to_numeric(industry_data['Data_value'], errors='coerce').max())
            }
        }

    # Detect anomalies in data values
    structure_changes['data_anomalies'] = {}

    # Check for negative values (might indicate errors)
    data_values = pd.to_numeric(df['Data_value'], errors='coerce')
    negative_values = df[data_values < 0]
    structure_changes['data_anomalies']['negative_values'] = {
        'count': len(negative_values),
        'sample': negative_values.head(5)[['Series_reference', 'Period', 'Data_value', 'Series_title_2']].to_dict('records')
    }

    # Check for extremely high values
    q95 = data_values.quantile(0.95)
    extreme_high = df[data_values > q95 * 2]  # Values more than 2x the 95th percentile
    structure_changes['data_anomalies']['extreme_high_values'] = {
        'count': len(extreme_high),
        'threshold': float(q95 * 2),
        'sample': extreme_high.head(5)[['Series_reference', 'Period', 'Data_value', 'Series_title_2']].to_dict('records')
    }

    # Analyze temporal patterns
    structure_changes['temporal_patterns'] = {}

    # Group by year and quarter to see patterns
    df['Year'] = df['Period'].str.split('.').str[0].astype(int)
    df['Quarter'] = df['Period'].str.split('.').str[1]

    yearly_totals = df.groupby('Year').size().reset_index(name='record_count')
    structure_changes['temporal_patterns']['yearly_distribution'] = yearly_totals.to_dict('records')

    quarterly_totals = df.groupby('Quarter').size().reset_index(name='record_count')
    structure_changes['temporal_patterns']['quarterly_distribution'] = quarterly_totals.to_dict('records')

    # Find industries with incomplete data
    industry_completeness = df.groupby('Series_title_2')['Period'].nunique().reset_index(name='unique_periods')
    total_periods = len(df['Period'].unique())
    industry_completeness['completeness_ratio'] = industry_completeness['unique_periods'] / total_periods

    incomplete_industries = industry_completeness[industry_completeness['completeness_ratio'] < 0.8]
    structure_changes['incomplete_data'] = {
        'industries_with_incomplete_data': incomplete_industries.to_dict('records'),
        'total_industries': len(industry_completeness),
        'incomplete_count': len(incomplete_industries)
    }

    # Save phase 3 results
    phase3_results = {
        'structure_changes': structure_changes,
        'summary': {
            'total_industries': len(industries),
            'total_periods': len(periods),
            'missing_periods_count': len(structure_changes['period_consistency']['missing_periods']),
            'industries_with_anomalies': len([k for k, v in structure_changes['industry_patterns'].items() if v['record_count'] < 50])
        }
    }

    with open('./blackbox-analysis/phase3_structure_changes.json', 'w') as f:
        json.dump(phase3_results, f, indent=2, default=str)

    print("Phase 3 Analysis Complete!")
    print(f"Found {len(structure_changes['period_consistency']['missing_periods'])} missing periods")
    print(f"Analyzed {len(industries)} different industries")
    print(f"Found {structure_changes['data_anomalies']['negative_values']['count']} negative values")
    print(f"Found {structure_changes['data_anomalies']['extreme_high_values']['count']} extreme high values")

    return structure_changes

def phase4_analysis(df):
    """Phase 4: Save comprehensive insights to JSON"""

    # Load all previous results
    with open('./blackbox-analysis/phase1_structure.json', 'r') as f:
        phase1_data = json.load(f)

    with open('./blackbox-analysis/phase2_analysis.json', 'r') as f:
        phase2_data = json.load(f)

    with open('./blackbox-analysis/phase3_structure_changes.json', 'r') as f:
        phase3_data = json.load(f)

    # Comprehensive insights
    comprehensive_insights = {
        'dataset_overview': {
            'name': 'Employment Data Analysis',
            'source': 'employment-data.csv',
            'total_records': phase1_data['structure_info']['total_rows'],
            'total_columns': phase1_data['structure_info']['total_columns'],
            'date_range': phase2_data['analysis_results']['period_analysis']['year_range'],
            'industries_covered': len(phase2_data['analysis_results']['categorical_analysis']['series_title_2_unique'])
        },

        'data_structure': {
            'columns': phase1_data['structure_info']['column_names'],
            'data_types': phase1_data['structure_info']['data_types'],
            'key_columns': {
                'series_reference': {
                    'description': 'Unique identifier for each data series',
                    'pattern': 'BDCQ.SECTION.CODE',
                    'total_unique': phase2_data['analysis_results']['series_reference_patterns']['total_unique']
                },
                'period': {
                    'description': 'Time period in YYYY.QQ format',
                    'range': phase2_data['analysis_results']['period_analysis']['year_range'],
                    'frequency': 'Quarterly'
                },
                'data_value': {
                    'description': 'Employment numbers or earnings values',
                    'units': list(phase2_data['analysis_results']['units_analysis']['units_counts'].keys()),
                    'range': {
                        'min': phase2_data['analysis_results']['data_value_analysis']['statistics']['min'],
                        'max': phase2_data['analysis_results']['data_value_analysis']['statistics']['max']
                    }
                }
            }
        },

        'content_analysis': {
            'industries': {
                'total': len(phase2_data['analysis_results']['categorical_analysis']['series_title_2_unique']),
                'list': phase2_data['analysis_results']['categorical_analysis']['series_title_2_unique'],
                'data_types_per_industry': phase2_data['analysis_results']['groupings']['industry_by_type']
            },
            'data_types': {
                'total': len(phase2_data['analysis_results']['categorical_analysis']['series_title_3_unique']),
                'types': phase2_data['analysis_results']['categorical_analysis']['series_title_3_unique']
            },
            'status_distribution': phase2_data['analysis_results']['status_analysis'],
            'units_distribution': phase2_data['analysis_results']['units_analysis']
        },

        'data_quality': {
            'completeness': {
                'null_values': phase1_data['structure_info']['null_counts'],
                'missing_periods': phase3_data['structure_changes']['period_consistency']['missing_periods'],
                'incomplete_industries': phase3_data['structure_changes']['incomplete_data']
            },
            'anomalies': {
                'negative_values': phase3_data['structure_changes']['data_anomalies']['negative_values'],
                'extreme_values': phase3_data['structure_changes']['data_anomalies']['extreme_high_values']
            },
            'consistency': {
                'temporal_patterns': phase3_data['structure_changes']['temporal_patterns'],
                'industry_coverage': phase3_data['structure_changes']['industry_patterns']
            }
        },

        'statistical_summary': {
            'data_value_statistics': phase2_data['analysis_results']['data_value_analysis']['statistics'],
            'distribution': phase2_data['analysis_results']['data_value_analysis']['distribution'],
            'temporal_distribution': phase3_data['structure_changes']['temporal_patterns']
        },

        'key_findings': [
            f"Dataset contains {phase1_data['structure_info']['total_rows']:,} records spanning {phase2_data['analysis_results']['period_analysis']['year_range']['min_year']} to {phase2_data['analysis_results']['period_analysis']['year_range']['max_year']}",
            f"Data covers {len(phase2_data['analysis_results']['categorical_analysis']['series_title_2_unique'])} different industries with employment and earnings data",
            f"Values range from {phase2_data['analysis_results']['data_value_analysis']['statistics']['min']:,.0f} to {phase2_data['analysis_results']['data_value_analysis']['statistics']['max']:,.0f}",
            f"Found {len(phase3_data['structure_changes']['period_consistency']['missing_periods'])} missing periods in the time series",
            f"Data includes both 'Filled jobs' and 'Total earnings' metrics across different industries",
            f"{phase3_data['structure_changes']['data_anomalies']['negative_values']['count']} records contain negative values (potential data quality issue)",
            f"Most industries have complete quarterly data, but some show gaps in coverage"
        ],

        'recommendations': [
            "Verify negative values to ensure they represent valid data points",
            "Investigate missing periods to understand data collection gaps",
            "Consider standardizing industry naming conventions",
            "Validate extreme high values against known benchmarks",
            "Document the meaning of different STATUS codes (F, R, C, etc.)",
            "Create data quality checks for future data updates"
        ]
    }

    # Save comprehensive insights
    with open('./blackbox-analysis/comprehensive_insights.json', 'w') as f:
        json.dump(comprehensive_insights, f, indent=2, default=str)

    print("Phase 4 Analysis Complete!")
    print("Comprehensive insights saved to comprehensive_insights.json")
    print("\nKey Findings:")
    for finding in comprehensive_insights['key_findings']:
        print(f"- {finding}")

    return comprehensive_insights

if __name__ == "__main__":
    df, results = phase1_analysis()
    phase2_results = phase2_analysis(df)
    phase3_results = phase3_analysis(df)
    phase4_results = phase4_analysis(df)