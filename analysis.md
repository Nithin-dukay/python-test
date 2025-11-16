# Employment Data Analysis Report

**Analysis Date:** November 16, 2025  
**Dataset:** Business Data Collection (BDC) - Employment Statistics  
**Time Period:** Q2 2011 - Q2 2025 (14 years)  
**Total Records:** 20,108

---

## Executive Summary

This comprehensive analysis examines employment data from New Zealand's Business Data Collection spanning 14 years (2011-2025). The dataset contains **20,108 records** tracking filled jobs and total earnings across multiple dimensions:

- **5 Major Groups**: Industry, Region, Territorial Authority, Age, and Sex
- **106 Unique Categories**: Including 10 industries, 16 regions, 68 territorial authorities, 11 age groups, and 2 gender categories
- **3 Data Types**: Actual, Seasonally Adjusted, and Trend data
- **2 Key Metrics**: Filled Jobs (count) and Total Earnings (value in millions)

### Key Findings

1. **Overall Employment Growth**: +30.8% increase from 2011 to 2025
2. **Gender Parity**: Nearly equal growth rates (Male: +30.6%, Female: +31.1%)
3. **Strongest Industry Growth**: Electricity, Gas, Water & Waste Services (+63.5%)
4. **Fastest Growing Region**: Tasman (+95.9%)
5. **Aging Workforce**: 65+ age group showed +108.5% growth
6. **Earnings Surge**: Health Care sector earnings grew +169.5%

---

## 1. Dataset Overview

### 1.1 Data Structure

| Attribute | Details |
|-----------|---------|
| **Total Records** | 20,108 |
| **Columns** | 14 |
| **File Size** | 2.97 MB |
| **Time Span** | 14 years (2011.06 - 2025.06) |
| **Unique Periods** | 57 quarterly periods |
| **Data Completeness** | 91.5% (18,390 records with values) |
| **Suppressed Records** | 1,718 (8.5%) |

### 1.2 Column Information

1. **Series_reference** - Unique identifier for each data series (370 unique codes)
2. **Period** - Time period in YYYY.MM format (quarterly: .03, .06, .09, .12)
3. **Data_value** - Numeric value (jobs count or earnings in millions)
4. **Suppressed** - Data suppression flag ('Y' for suppressed data)
5. **STATUS** - Data status (F=Final 81%, R=Revised 14%, C=Confidential 5%)
6. **UNITS** - Measurement unit (Number=63%, Value=37%)
7. **Magnitude** - Scale factor (0 for counts, 6 for millions)
8. **Subject** - Data source (Business Data Collection - BDC)
9. **Group** - Primary categorization dimension
10. **Series_title_1** - Employment variable type
11. **Series_title_2** - Specific category (industry, region, age, etc.)
12. **Series_title_3** - Data adjustment type (Actual, Seasonally adjusted, Trend)
13-14. **Series_title_4/5** - Empty fields (100% null)

### 1.3 Data Quality

- **Missing Values**: Only in Data_value (8.5%) and Suppressed fields
- **Data Status**: 81% Final, 14% Revised, 5% Confidential
- **Temporal Coverage**: Consistent quarterly data from 2011-2024, partial 2025 data

---

## 2. Group Analysis

### 2.1 Distribution by Group

| Group | Records | % of Total | Categories |
|-------|---------|------------|------------|
| Territorial Authority | 11,488 | 57.1% | 68 authorities |
| Region | 5,808 | 28.9% | 16 regions |
| Industry | 1,330 | 6.6% | 10 industries |
| Age | 1,254 | 6.2% | 11 age groups |
| Sex | 228 | 1.1% | 2 categories |

### 2.2 Employment Variables

1. **Filled jobs** - 39.3% of records (7,903 records)
2. **Total earnings** - 37.0% of records (7,445 records)
3. **Filled jobs (workplace location based)** - 23.7% of records (4,760 records)

---

## 3. Industry Analysis

### 3.1 Industries Covered

The dataset tracks 10 major industry sectors:

1. Agriculture, Forestry and Fishing
2. Mining
3. Manufacturing
4. Electricity, Gas, Water and Waste Services
5. Education and Training
6. Health Care and Social Assistance
7. Public Administration and Safety
8. Arts and Recreation Services
9. Other Services
10. Total Industry (aggregate)

### 3.2 Industry Employment Trends (2011-2025)

| Industry | 2011 Jobs | 2025 Jobs | Change | Growth % |
|----------|-----------|-----------|--------|----------|
| **Agriculture, Forestry & Fishing** | 80,078 | 92,128 | +12,050 | +15.1% |
| **Mining** | 5,234 | 6,106 | +872 | +16.7% |
| **Manufacturing** | 206,633 | 222,420 | +15,787 | +7.6% |
| **Electricity, Gas, Water & Waste** | 14,486 | 23,678 | +9,192 | **+63.5%** ⭐ |

**Key Insights:**
- **Electricity, Gas, Water & Waste Services** showed the strongest growth at +63.5%
- **Manufacturing** remains the largest employer with 222,420 jobs
- **Mining** sector is the smallest but showed healthy +16.7% growth
- All tracked industries showed positive employment growth

### 3.3 Industry Earnings Trends (2011-2025)

| Industry | 2011 Earnings | 2025 Earnings | Growth % |
|----------|---------------|---------------|----------|
| **Arts & Recreation** | $329.95M | $637.18M | +93.1% |
| **Education & Training** | $2,194.27M | $3,938.57M | +79.5% |
| **Health Care & Social Assistance** | $2,217.71M | $5,976.45M | **+169.5%** ⭐ |
| **Other Services** | $530.62M | $1,177.24M | +121.9% |
| **Total Industry** | $20,722.45M | $45,102.99M | +117.7% |

**Key Insights:**
- **Health Care** earnings nearly tripled (+169.5%), reflecting sector expansion and wage growth
- **Total Industry** earnings more than doubled (+117.7%)
- All sectors showed strong earnings growth, outpacing employment growth (wage increases)

---

## 4. Regional Analysis

### 4.1 New Zealand Regions (16 Total)

Auckland, Bay of Plenty, Canterbury, Gisborne, Hawke's Bay, Manawatu-Whanganui, Marlborough, Nelson, Northland, Otago, Southland, Taranaki, Tasman, Waikato, Wellington, West Coast

### 4.2 Top 10 Regions by Current Employment (Q2 2025)

| Rank | Region | Current Jobs | Growth % |
|------|--------|--------------|----------|
| 1 | **Auckland** | 769,959 | +37.8% |
| 2 | **Canterbury** | 302,898 | +32.8% |
| 3 | **Wellington** | 246,835 | +20.3% |
| 4 | **Waikato** | 219,360 | +37.8% |
| 5 | **Bay of Plenty** | 143,673 | +35.8% |
| 6 | **Otago** | 112,962 | +30.1% |
| 7 | **Manawatu-Whanganui** | 107,443 | +17.0% |
| 8 | **Hawke's Bay** | 79,104 | +22.6% |
| 9 | **Northland** | 71,066 | +41.5% |
| 10 | **Taranaki** | 52,477 | +17.2% |

### 4.3 Fastest Growing Regions

| Rank | Region | Growth % | Job Increase |
|------|--------|----------|--------------|
| 1 | **Tasman** | **+95.9%** ⭐ | +12,052 |
| 2 | **Northland** | +41.5% | +20,832 |
| 3 | **Auckland** | +37.8% | +211,363 |
| 4 | **Waikato** | +37.8% | +60,164 |
| 5 | **Bay of Plenty** | +35.8% | +37,867 |

**Key Insights:**
- **Auckland** dominates with 769,959 jobs (34% of total employment)
- **Tasman** region nearly doubled its employment (+95.9%)
- **Northern regions** (Northland, Auckland, Waikato) showed strong growth
- **Wellington** grew more slowly (+20.3%) despite being 3rd largest

---

## 5. Demographic Analysis

### 5.1 Age Group Employment Trends (2011-2025)

| Age Group | 2011 Jobs | 2025 Jobs | Change | Growth % |
|-----------|-----------|-----------|--------|----------|
| **15-19** | 98,572 | 113,927 | +15,355 | +15.6% |
| **20-24** | 191,834 | 214,165 | +22,331 | +11.6% |
| **25-29** | 184,750 | 244,477 | +59,727 | +32.3% |
| **30-34** | 173,195 | 278,578 | +105,383 | **+60.9%** |
| **35-39** | 186,714 | 270,882 | +84,168 | +45.1% |
| **40-44** | 200,611 | 239,524 | +38,913 | +19.4% |
| **45-49** | 200,716 | 211,645 | +10,929 | +5.4% |
| **50-54** | 178,833 | 208,581 | +29,748 | +16.6% |
| **55-59** | 140,309 | 184,468 | +44,159 | +31.5% |
| **60-64** | 105,985 | 157,693 | +51,708 | +48.8% |
| **65+** | 61,853 | 128,988 | +67,135 | **+108.5%** ⭐ |

**Key Insights:**
- **65+ age group** more than doubled (+108.5%), indicating aging workforce participation
- **30-34 age group** showed strongest growth in prime working years (+60.9%)
- **45-49 age group** showed slowest growth (+5.4%)
- **Younger workers (15-24)** showed modest growth, possibly due to education trends
- **Older workers (55+)** all showed strong growth, reflecting delayed retirement

### 5.2 Gender Employment Analysis

| Gender | 2011 Jobs | 2025 Jobs | Change | Growth % | Average Jobs |
|--------|-----------|-----------|--------|----------|--------------|
| **Male** | 861,368 | 1,124,807 | +263,439 | +30.6% | 1,015,877 |
| **Female** | 865,507 | 1,134,933 | +269,426 | +31.1% | 1,005,377 |

**Key Insights:**
- **Near parity**: Female employment slightly exceeded male employment in 2011
- **Equal growth**: Both genders showed nearly identical growth rates (~31%)
- **2025 balance**: Female employment slightly higher (1,134,933 vs 1,124,807)
- **Consistent trend**: Gender balance maintained throughout 14-year period

---

## 6. Temporal Patterns

### 6.1 Quarterly Distribution

| Quarter | Records | Average Jobs |
|---------|---------|--------------|
| **Q1 (March)** | 4,913 | - |
| **Q2 (June)** | 5,279 | - |
| **Q3 (September)** | 4,959 | - |
| **Q4 (December)** | 4,957 | - |

### 6.2 Year-over-Year Trends

- **2011-2015**: Steady growth period
- **2016-2019**: Accelerated growth phase
- **2020**: COVID-19 impact (slight dip in some sectors)
- **2021-2023**: Recovery and strong growth
- **2024-2025**: Continued expansion

### 6.3 Seasonal Patterns

Employment data shows quarterly variations, particularly in:
- **Agriculture**: Peak in Q1 (March) and Q4 (December) - harvest seasons
- **Education**: Variations aligned with academic calendar
- **Tourism-related**: Higher in summer quarters

---

## 7. Territorial Authority Analysis

### 7.1 Coverage

The dataset includes **68 territorial authorities** across New Zealand, each with 171 records representing:
- Different employment variables (filled jobs, earnings)
- Multiple time periods (quarterly data)
- Various data types (actual, seasonally adjusted, trend)

### 7.2 Major Urban Centers

Top territorial authorities by employment (based on record patterns):
- Auckland City
- Wellington City
- Christchurch City (Canterbury)
- Hamilton City
- Tauranga City

---

## 8. Data Quality & Methodology

### 8.1 Data Status Codes

- **F (Final)**: 81.2% - Finalized, official statistics
- **R (Revised)**: 14.2% - Revised figures (typically seasonally adjusted/trend data)
- **C (Confidential)**: 4.7% - Suppressed for confidentiality

### 8.2 Data Types

- **Actual**: 80.7% - Raw, unadjusted data
- **Seasonally Adjusted**: 9.7% - Adjusted for seasonal variations
- **Trend**: 9.7% - Smoothed trend data

### 8.3 Suppression

- **1,718 records (8.5%)** have suppressed values (marked with 'Y')
- Suppression typically occurs for confidentiality when:
  - Small numbers could identify specific businesses
  - Data quality concerns exist
  - Statistical reliability is low

---

## 9. Key Trends & Insights

### 9.1 Economic Transformation

**Service Sector Dominance:**
- Health Care, Education, and Other Services showed exceptional growth
- Traditional sectors (Manufacturing, Agriculture) showed moderate growth
- Utilities sector (Electricity, Gas, Water) expanded significantly

### 9.2 Regional Development Patterns

**Urban Concentration:**
- Auckland continues to dominate (34% of total employment)
- Major cities (Auckland, Canterbury, Wellington) account for ~60% of jobs

**Regional Growth:**
- Smaller regions (Tasman, Northland) showed highest percentage growth
- Indicates regional development and decentralization trends

### 9.3 Demographic Shifts

**Aging Workforce:**
- Dramatic increase in 65+ employment (+108.5%)
- Strong growth in 55-64 age groups (+31-49%)
- Reflects policy changes, retirement age increases, and economic necessity

**Prime Working Age:**
- 30-39 age groups showed strong growth
- Indicates population growth and immigration in these cohorts

**Youth Employment:**
- Modest growth in 15-24 age groups
- May reflect higher education participation rates

### 9.4 Gender Equality Progress

- **Balanced growth** across genders
- **Female employment** slightly exceeds male in absolute numbers
- Suggests successful gender equality policies and workforce participation

### 9.5 Earnings vs Employment Growth

**Earnings outpaced employment growth significantly:**
- Total earnings: +117.7%
- Total employment: +30.8%
- **Indicates**: Real wage growth, productivity improvements, and economic expansion

---

## 10. Sector-Specific Insights

### 10.1 Health Care & Social Assistance

- **Employment**: Moderate growth
- **Earnings**: +169.5% (highest growth)
- **Interpretation**: Aging population, increased healthcare demand, wage improvements

### 10.2 Education & Training

- **Earnings**: +79.5% growth
- **Pattern**: Strong seasonal variations (academic calendar)
- **Trend**: Expansion of education sector

### 10.3 Manufacturing

- **Jobs**: 222,420 (largest single industry)
- **Growth**: +7.6% (modest)
- **Stability**: Consistent employment levels throughout period

### 10.4 Agriculture, Forestry & Fishing

- **Growth**: +15.1%
- **Seasonality**: Strong quarterly variations
- **Pattern**: Peak employment in harvest seasons (Q1, Q4)

---

## 11. COVID-19 Impact Analysis

### 11.1 Timeline

- **Pre-COVID (2011-2019)**: Steady growth trajectory
- **2020 Q1-Q2**: Initial pandemic impact
- **2020 Q3-Q4**: Recovery begins
- **2021-2025**: Strong recovery and growth

### 11.2 Observations

- **Resilience**: Overall employment continued growing through pandemic
- **Sector variations**: Some sectors more affected than others
- **Recovery**: Strong bounce-back in 2021-2023

---

## 12. Statistical Summary

### 12.1 Employment Metrics

| Metric | Value |
|--------|-------|
| **Total Records Analyzed** | 20,108 |
| **Filled Jobs Records** | 7,902 |
| **Earnings Records** | 5,757 |
| **Time Periods** | 57 quarters |
| **Geographic Coverage** | 16 regions, 68 authorities |

### 12.2 Value Ranges

| Measure | Minimum | Maximum | Mean | Median |
|---------|---------|---------|------|--------|
| **Data Values** | 1.17 | 1,163,117 | 53,632.55 | 10,953.50 |

### 12.3 Growth Summary (2011-2025)

- **Overall Employment**: +30.8%
- **Male Employment**: +30.6%
- **Female Employment**: +31.1%
- **Total Earnings**: +117.7%
- **Average Wage Growth**: ~66% (earnings growth minus employment growth)

---

## 13. Conclusions

### 13.1 Major Findings

1. **Robust Growth**: New Zealand employment grew consistently over 14 years
2. **Regional Diversity**: Growth distributed across regions, not just urban centers
3. **Demographic Shift**: Significant increase in older worker participation
4. **Gender Equality**: Balanced employment growth between genders
5. **Wage Growth**: Earnings significantly outpaced employment growth
6. **Sector Transformation**: Service sectors (health, education) expanding rapidly

### 13.2 Implications

**For Policy Makers:**
- Aging workforce requires retirement policy adjustments
- Regional development strategies showing success
- Service sector investment yielding results

**For Businesses:**
- Growing markets in health care, utilities, education
- Regional expansion opportunities beyond major cities
- Older worker recruitment and retention important

**For Workers:**
- Strong job market across most sectors
- Wage growth exceeding inflation in many industries
- Opportunities in growing regions and sectors

### 13.3 Future Outlook

Based on 2024-2025 trends:
- **Continued growth** expected in service sectors
- **Regional development** likely to continue
- **Aging workforce** trend will accelerate
- **Technology sectors** (not separately tracked) likely embedded in growth

---

## 14. Methodology Notes

### 14.1 Data Processing

- All 20,108 records processed without sampling
- Numeric conversions applied to Data_value field
- Period parsed into Year and Quarter components
- Suppressed data excluded from statistical calculations

### 14.2 Calculations

- **Growth rates**: ((Latest - Earliest) / Earliest) × 100
- **Averages**: Mean of all non-null values in period
- **Trends**: Based on actual (non-adjusted) data unless specified

### 14.3 Visualizations

15 comprehensive charts created covering:
- Time series trends
- Growth comparisons
- Distributions
- Multi-panel dashboards

All visualizations saved as:
- High-resolution PNG files (300 DPI)
- Compiled PDF report

---

## 15. Data Dictionary

### 15.1 Series Reference Codes

Format: `BDCQ.SExxxx`
- **BDCQ**: Business Data Collection Quarterly
- **SE**: Series identifier
- **A/B/C**: Group indicator (A=Industry, B=Sex, C=Age, etc.)
- **1/2**: Variable type (1=Filled jobs, 2=Earnings)
- **Last letter**: Data type (A=Actual, S=Seasonally adjusted, T=Trend)

### 15.2 Period Format

- **YYYY.MM**: Year.Month
- **Quarters**: .03 (Q1), .06 (Q2), .09 (Q3), .12 (Q4)

### 15.3 Magnitude

- **0**: Actual count (for filled jobs)
- **6**: Millions (for earnings values)

---

## Appendix: Technical Details

**Analysis Tools:**
- Python 3.9.24
- pandas, numpy (data processing)
- matplotlib, seaborn (visualization)
- reportlab (PDF generation)

**Files Generated:**
- `employment_insights_phase1.json` - Data structure insights
- `employment_insights_phase2.json` - Deep dive analysis
- `employment_insights_phase3.json` - Statistical trends
- `analysis.md` - This comprehensive report
- `./blackbox-analysis/visualization/*.png` - 15 visualization charts
- `./blackbox-analysis/pdfs/employment_analysis_report.pdf` - Visual PDF report

**Analysis Date:** November 16, 2025  
**Analyst:** Blackbox AI Data Analysis System

---

*End of Report*
