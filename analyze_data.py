import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

def load_and_explore_data(file_path):
    """Load the CSV file and perform initial exploration"""
    print("Loading employment data...")
    df = pd.read_csv(file_path)

    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nData types:")
    print(df.dtypes)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nBasic statistics:")
    print(df.describe())

    # Check for missing values
    print("\nMissing values per column:")
    print(df.isnull().sum())

    # Unique values in key columns
    print("\nUnique values in key columns:")
    for col in ['STATUS', 'UNITS', 'Magnitude', 'Subject', 'Group', 'Series_title_1']:
        print(f"{col}: {df[col].unique()}")

    # Industries
    print(f"\nIndustries (Series_title_2): {sorted(df['Series_title_2'].unique())}")

    # Data types
    print(f"\nData types (Series_title_3): {sorted(df['Series_title_3'].unique())}")

    # Time period range
    print(f"\nPeriod range: {df['Period'].min()} to {df['Period'].max()}")

    # Data value statistics
    print(f"\nData_value statistics:")
    print(f"Min: {df['Data_value'].min()}")
    print(f"Max: {df['Data_value'].max()}")
    print(f"Mean: {df['Data_value'].mean():.2f}")
    print(f"Median: {df['Data_value'].median():.2f}")

    return df

def analyze_series_structure(df):
    """Analyze the series reference structure"""
    print("\n=== SERIES STRUCTURE ANALYSIS ===")

    # Extract components from Series_reference
    df['series_prefix'] = df['Series_reference'].str[:4]  # BDCQ
    df['series_type'] = df['Series_reference'].str[4:7]   # SEA
    df['series_number'] = df['Series_reference'].str[7:9] # 1A, 1B, etc.
    df['series_suffix'] = df['Series_reference'].str[9:]   # A, AS, AT, etc.

    print("Series reference components:")
    print(f"Prefixes: {sorted(df['series_prefix'].unique())}")
    print(f"Types: {sorted(df['series_type'].unique())}")
    print(f"Numbers: {sorted(df['series_number'].unique())}")
    print(f"Suffixes: {sorted(df['series_suffix'].unique())}")

    # Group by series components
    series_groups = df.groupby(['series_number', 'series_suffix']).size()
    print(f"\nSeries groups (number + suffix):")
    print(series_groups)

    return df

def analyze_temporal_patterns(df):
    """Analyze temporal patterns in the data"""
    print("\n=== TEMPORAL ANALYSIS ===")

    # Convert Period to datetime
    df['period_date'] = pd.to_datetime(df['Period'], format='%Y.%m')

    # Group by year and month
    df['year'] = df['period_date'].dt.year
    df['month'] = df['period_date'].dt.month

    print(f"Years covered: {sorted(df['year'].unique())}")
    print(f"Months present: {sorted(df['month'].unique())}")

    # Records per year
    yearly_counts = df.groupby('year').size()
    print(f"\nRecords per year:")
    print(yearly_counts)

    return df

def save_initial_insights(df, output_file='initial_insights.json'):
    """Save initial insights to JSON file"""
    insights = {
        'dataset_info': {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'period_range': [df['Period'].min(), df['Period'].max()],
            'years_covered': sorted(df['year'].unique().tolist())
        },
        'data_characteristics': {
            'industries': sorted(df['Series_title_2'].unique().tolist()),
            'data_types': sorted(df['Series_title_3'].unique().tolist()),
            'statuses': sorted(df['STATUS'].unique().tolist()),
            'series_components': {
                'prefixes': sorted(df['series_prefix'].unique().tolist()),
                'types': sorted(df['series_type'].unique().tolist()),
                'numbers': sorted(df['series_number'].unique().tolist()),
                'suffixes': sorted(df['series_suffix'].unique().tolist())
            }
        },
        'statistics': {
            'data_value_min': float(df['Data_value'].min()),
            'data_value_max': float(df['Data_value'].max()),
            'data_value_mean': float(df['Data_value'].mean()),
            'data_value_median': float(df['Data_value'].median())
        },
        'analysis_timestamp': datetime.now().isoformat()
    }

    with open(output_file, 'w') as f:
        json.dump(insights, f, indent=2, default=str)

    print(f"\nInitial insights saved to {output_file}")

if __name__ == "__main__":
    file_path = "/vercel/sandbox/uploads/employment-data.csv"

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        exit(1)

    # Load and explore data
    df = load_and_explore_data(file_path)

    # Analyze series structure
    df = analyze_series_structure(df)

    # Analyze temporal patterns
    df = analyze_temporal_patterns(df)

    # Save insights
    save_initial_insights(df)