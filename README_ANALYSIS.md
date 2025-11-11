# Steam Charts Data Analysis

## Quick Start

This directory contains a comprehensive analysis of **612,265 data points** across **6,729 Steam games** from July 2012 to September 2025.

## 📁 Files Overview

### Reports (Start Here!)
- **`steamcharts_report.html`** - Open this in your browser for a beautiful visual report
- **`STEAMCHARTS_ANALYSIS_REPORT.md`** - Detailed 20+ page analysis with all findings
- **`ANALYSIS_SUMMARY.txt`** - Quick reference summary

### Data Files
- **`steamcharts.csv`** - Original dataset (36MB, 612K records)
- **`steamcharts_sample.csv`** - Top 100 games (11,767 records)
- **`steamcharts_insights.json`** - Machine-readable insights

### Analysis Scripts
- **`analyze_steamcharts.py`** - Initial data exploration
- **`generate_insights.py`** - Advanced pattern detection and insights

### Interactive Dashboard
- **`steamcharts-dashboard/`** - React application with interactive charts
  - Run: `cd steamcharts-dashboard && npm start`
  - View at: http://localhost:3000

## 🎯 Key Findings

### Top 5 Games (September 2025)
1. **Counter-Strike 2** - 925,940 avg players (+10.72% YoY)
2. **PUBG: BATTLEGROUNDS** - 278,096 avg players (-6.76% YoY)
3. **Rust** - 85,515 avg players (+12.16% YoY)
4. **Wallpaper Engine** - 78,472 avg players (+4.54% YoY)
5. **HELLDIVERS™ 2** - 68,412 avg players (+164.29% YoY)

### Market Insights
- **Market Concentration**: Only 0.05% of records show 100K+ players
- **Long Tail**: 80% of games have <100 concurrent players
- **Growth Leader**: Indie games (+0.87% average growth)
- **Best Launch Month**: May (65.27% average growth)
- **All-Time Peak**: PUBG with 3,236,027 concurrent players

### Market Segments
| Segment | Games | Growth |
|---------|-------|--------|
| AAA Blockbusters (100K+) | 2 | -0.03% |
| Popular (10K-100K) | 51 | +0.02% |
| Mid-tier (1K-10K) | 153 | +0.04% |
| Indie (100-1K) | 636 | +0.87% ⭐ |
| Niche (<100) | 3,035 | +0.12% |

## 💡 Recommendations

### For Developers
- Target niche audiences for sustainable growth
- Focus on community engagement for retention
- Consider May launches for maximum visibility
- Indie segment shows strong growth potential

### For Publishers
- Mid-tier games (1K-10K) offer best risk/reward
- Sustained marketing crucial for new releases
- Diversification opportunities in indie segment

### For Investors
- Look for stable, engaged communities
- Long-term value in consistent player bases
- Growth opportunities in mid-tier and indie

## 🔧 Running the Analysis

### View Reports
```bash
# Open HTML report in browser
open steamcharts_report.html

# Read detailed analysis
cat STEAMCHARTS_ANALYSIS_REPORT.md

# Quick summary
cat ANALYSIS_SUMMARY.txt
```

### Run Analysis Scripts
```bash
# Initial exploration
python3 analyze_steamcharts.py

# Generate insights
python3 generate_insights.py
```

### Launch Dashboard
```bash
cd steamcharts-dashboard
npm install  # First time only
npm start
# Open http://localhost:3000
```

## 📊 Data Quality

- **Completeness**: 100% (no missing values)
- **Consistency**: All games tracked monthly
- **Time Span**: 13+ years (159 months)
- **Accuracy**: Official Steam tracking data

## 🔍 Analysis Methods

- Time series analysis
- Statistical modeling (mean, median, std dev, percentiles)
- Market segmentation
- Trend analysis (YoY, MoM)
- Volatility calculations
- Seasonal pattern detection

## 📈 Notable Trends

1. **HELLDIVERS™ 2** shows explosive growth (+164% YoY)
2. **Hollow Knight** experienced massive resurgence (+226%)
3. **Classic games** (Counter-Strike, TF2) maintain stability
4. **PUBG** declining but still massive (278K players)
5. **Indie games** outperforming AAA in growth

## 🎮 Stability Analysis

**Most Stable Games:**
- Counter-Strike (volatility: 0.082)
- Blender (volatility: 0.085)
- Sid Meier's Civilization V (volatility: 0.095)

**Most Volatile Games:**
- Total War: THREE KINGDOMS (volatility: 183,764)
- Mount & Blade II: Bannerlord (volatility: 55,087)
- Warframe (volatility: 35,391)

## 📅 Seasonal Patterns

- **May**: Highest growth (65.27% avg)
- **December**: Holiday boost
- **Summer**: More competitive
- **February**: High variance (major releases)

## 🏆 All-Time Records

- **Peak Players**: PUBG - 3,236,027
- **Longest Tracked**: Counter-Strike (159 months)
- **Biggest Growth**: Data Hacker: Initiation (+212%)
- **Most Stable**: Counter-Strike (0.082 volatility)

## 📞 Questions?

For detailed insights, refer to:
1. `STEAMCHARTS_ANALYSIS_REPORT.md` - Comprehensive analysis
2. `steamcharts_insights.json` - Raw data insights
3. Interactive dashboard - Visual exploration

---

**Analysis Date**: November 11, 2025  
**Data Coverage**: July 2012 - September 2025  
**Total Games**: 6,729  
**Total Records**: 612,265
