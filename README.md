# Nifty 50 Stock Analysis

Comprehensive analysis of all 50 stocks in the Nifty 50 index with multi-dimensional scoring and rankings.

## Overview

This project analyzes all Nifty 50 stocks using technical, fundamental, sentiment, and risk analysis to generate a consolidated ranking report.

## Main Output

**`nifty50_analysis_2026-05-09.csv`** - Complete analysis with rankings for all 50 stocks

### Analysis Dimensions

Each stock is scored across 4 dimensions:
- **Technical Score** (0-100): Price action, indicators, patterns, momentum
- **Fundamental Score** (0-100): Valuation, growth, profitability, financial health
- **Sentiment Score** (0-100): Analyst ratings, institutional activity, market sentiment
- **Risk Score** (0-100): Volatility, beta, downside scenarios, liquidity

### Trade Score

Composite score calculated as weighted average:
- Technical: 30%
- Fundamental: 35%
- Sentiment: 20%
- Risk: 15%

## Top 10 Stocks by Trade Score

1. Kotak Mahindra Bank - 91 (Strong Buy)
2. Reliance Industries - 90 (Strong Buy)
3. Hero MotoCorp - 89 (Strong Buy)
4. Shriram Finance - 87 (Strong Buy)
5. Dr. Reddy's Labs - 86 (Strong Buy)
6. M&M - 85 (Strong Buy)
7. ICICI Bank - 84 (Strong Buy)
8. HDFC Bank - 83 (Strong Buy)
9. State Bank of India - 81 (Strong Buy)
10. BPCL - 80 (Strong Buy)

## Files

### Main Analysis
- `nifty50_analysis_2026-05-09.csv` - Complete ranked analysis of all 50 stocks
- `nifty50_analyzer.py` - Python script that performs the analysis

### Individual Stock Reports
- `TRADE-ANALYSIS-*.md` - Detailed 10-15 page reports for individual stocks

### Skills Configuration
- `.claude/skills/nifty50-analyzer/` - Claude skill configuration for orchestrating analysis

## Usage

### Running the Analysis

```bash
# Activate virtual environment
source venv/bin/activate

# Run the analyzer
python nifty50_analyzer.py
```

### Output Format

The CSV contains the following columns:
- Rank
- Ticker
- Company Name
- Trade Score
- Technical Score
- Fundamental Score
- Sentiment Score
- Risk Score
- Recommendation (Strong Buy / Buy / Hold / Sell)
- Status
- Notes

## Technology Stack

- **Python 3.11**
- **yfinance** - Market data fetching
- **pandas** - Data manipulation
- **numpy** - Numerical calculations

## Analysis Date

May 9, 2026

## Disclaimer

This analysis is for educational and research purposes only. Not financial advice. Always conduct your own due diligence and consult a licensed financial advisor before making investment decisions.
