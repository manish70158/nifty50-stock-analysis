---
name: nifty50-analyzer
description: Comprehensive Nifty 50 Stock Analysis with Consolidated CSV Report. Use this skill whenever the user mentions analyzing Nifty 50 stocks, Indian market screening, bulk analysis of Indian stocks, NSE top stocks, or wants a comparative analysis of India's top companies. Triggers on phrases like "analyze nifty 50", "screen nifty stocks", "compare nifty 50 companies", "bulk analyze Indian stocks", or "nifty 50 analysis report". Even if the user doesn't explicitly say "all nifty 50", use this skill when they want insights across multiple major Indian stocks.
---

# Nifty 50 Comprehensive Stock Analyzer

This skill analyzes all 50 stocks in the Nifty 50 index using the `/trade-analyze` skill and consolidates results into a ranked CSV report.

## Workflow

### 1. Get the stock list

Read the Nifty 50 stock list from `references/nifty50_tickers.txt`. Each line contains a ticker symbol with the `.NS` suffix for NSE (National Stock Exchange).

### 2. Launch parallel analyses

For each stock in the Nifty 50 list, invoke the `/trade-analyze` skill in parallel. This skill launches 5 sub-agents (technical, fundamental, sentiment, risk, and options analysis) for comprehensive multi-dimensional analysis.

**Important execution notes:**
- Launch all 50 analyses in parallel using the Task tool with `run_in_background: true`
- Store each task ID to track completion
- The analyses will run independently and complete at different times

**Example invocation:**
```
Use the Skill tool to invoke "trade-analyze" with args: "RELIANCE.NS"
```

### 3. Monitor progress

As analyses complete, provide periodic progress updates to the user:
- "Completed 10/50 stocks..."
- "Completed 25/50 stocks..."
- "Completed 40/50 stocks..."

Show which stocks have completed and approximately how many are remaining.

### 4. Collect results

For each completed analysis, extract the following information from the trade-analyze output:

**Required fields:**
- **Ticker symbol** (e.g., RELIANCE.NS)
- **Company name** (if available in the analysis)
- **Technical Score** (0-100)
- **Fundamental Score** (0-100)
- **Sentiment Score** (0-100)
- **Risk Score** (0-100)
- **Trade Score** (composite score, 0-100)
- **Recommendation** (Strong Buy / Buy / Hold / Sell / Strong Sell)

**Error handling:**
If an analysis fails or times out:
- Mark the status as "FAILED"
- Record the error message in the "Notes" column
- Set all scores to "N/A"
- Continue processing other stocks

### 5. Generate CSV report

Create a CSV file named `nifty50_analysis_YYYY-MM-DD.csv` with the following structure:

**Columns:**
```
Rank,Ticker,Company,Trade_Score,Technical_Score,Fundamental_Score,Sentiment_Score,Risk_Score,Recommendation,Status,Notes
```

**Sorting and ranking:**
- Sort all successfully analyzed stocks by Trade Score in descending order (highest first)
- Assign ranks: 1 for highest Trade Score, 2 for second highest, etc.
- Place failed analyses at the bottom with rank marked as "-"

**Example rows:**
```csv
Rank,Ticker,Company,Trade_Score,Technical_Score,Fundamental_Score,Sentiment_Score,Risk_Score,Recommendation,Status,Notes
1,RELIANCE.NS,Reliance Industries,85,82,88,80,75,Strong Buy,SUCCESS,
2,TCS.NS,Tata Consultancy Services,82,78,86,83,70,Buy,SUCCESS,
3,HDFCBANK.NS,HDFC Bank,80,75,84,82,68,Buy,SUCCESS,
...
-,SOMESTOCK.NS,Some Company,N/A,N/A,N/A,N/A,N/A,N/A,FAILED,Timeout after 300s
```

### 6. Summary statistics

After generating the CSV, provide the user with a summary:

```
Nifty 50 Analysis Complete
===========================
Successfully analyzed: 48/50 stocks
Failed: 2 stocks (see CSV for details)

Top 5 Performers by Trade Score:
1. [Ticker] - [Company] - Score: [XX]
2. [Ticker] - [Company] - Score: [XX]
...

Bottom 5 Performers by Trade Score:
46. [Ticker] - [Company] - Score: [XX]
...

CSV saved to: nifty50_analysis_YYYY-MM-DD.csv
```

## Output format

The primary output is a CSV file that can be:
- Opened in Excel/Google Sheets for further analysis
- Sorted and filtered by any column
- Used for comparison and screening

The CSV should be clean, properly formatted, and ready for immediate use.

## Tips for efficient execution

**Parallel execution:** Launch all 50 Task tool calls in a single message to maximize parallelization. Don't wait for one to finish before starting the next.

**Resource management:** The trade-analyze skill is comprehensive (runs 5 sub-analyses per stock). Monitor system resources if running into issues.

**Timeout handling:** If a stock analysis takes longer than 5 minutes, consider it failed and move on.

**Data validation:** After collecting results, verify that:
- All scores are numeric (0-100) or "N/A"
- Recommendations match expected values
- Ticker symbols are correct

## Common issues and solutions

**Issue:** Some analyses timeout
**Solution:** Mark as failed in CSV, note the timeout. User can re-run individual stocks later if needed.

**Issue:** Inconsistent output format from trade-analyze
**Solution:** Parse flexibly. Look for score patterns like "Technical Score: 85" or "Technical: 85/100". Extract the numeric value.

**Issue:** Company names not available
**Solution:** Use ticker symbol as fallback for company name column.

## Example user prompts that trigger this skill

- "Analyze all Nifty 50 stocks"
- "Give me a comprehensive report on Nifty 50"
- "Screen the Nifty 50 index"
- "Which Nifty 50 stocks are best to buy right now?"
- "Compare all stocks in the Nifty 50"
- "Run a full analysis on India's top 50 companies"
