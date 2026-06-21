# Stock Analysis Framework - Documentation

A comprehensive multi-agent stock analysis system that replicates the `/trade-analyze` skill functionality without using skill tokens.

## Overview

This framework performs deep stock analysis using 5 specialized AI agents running in parallel:

1. **Technical Analysis Agent** — Chart patterns, indicators, support/resistance
2. **Fundamental Analysis Agent** — Valuation, growth, profitability, moat
3. **Sentiment Analysis Agent** — News, social media, analyst ratings, institutional flows
4. **Risk Assessment Agent** — Volatility, downside scenarios, position sizing
5. **Investment Thesis Agent** — Bull/bear cases, catalysts, entry/exit strategy

The system produces a comprehensive markdown report with:
- Composite Trade Score (0-100)
- Letter Grade (A+ to F)
- Trading Signal (Strong Buy to Avoid)
- Detailed analysis from each agent
- Entry/exit levels with risk/reward ratios

## Files in This Framework

```
stock_analyzer.py          # Python orchestrator (full automation)
analyze_stock.sh          # Bash orchestrator (semi-automated)
README-STOCK-ANALYZER.md  # This documentation
agent_outputs/            # Directory for agent outputs
prompts/                  # Directory for agent prompts (auto-created)
```

## Installation & Setup

### Prerequisites

1. **Claude CLI** must be installed and configured
   ```bash
   # Install claude-code CLI
   npm install -g @anthropic-ai/claude-code

   # Or if using the official CLI
   pip install anthropic
   ```

2. **Python 3.8+** (for Python orchestrator)
   ```bash
   python --version  # Should be 3.8 or higher
   ```

3. **API Key** configured
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

### Setup

```bash
# Make scripts executable
chmod +x analyze_stock.sh
chmod +x stock_analyzer.py

# Create required directories
mkdir -p agent_outputs prompts
```

## Usage

### Method 1: Python Orchestrator (Recommended)

**Fully automated with parallel agent execution:**

```bash
# Basic usage
python stock_analyzer.py MUTHOOTFIN --market NSE

# US stock
python stock_analyzer.py AAPL --market NYSE

# With specific options
python stock_analyzer.py RELIANCE.NS --market NSE
```

**What it does:**
1. Creates discovery brief with context
2. Launches all 5 agents in parallel using `concurrent.futures`
3. Waits for all agents to complete
4. Extracts scores from each agent output
5. Calculates weighted composite score
6. Generates comprehensive markdown report

**Output:**
- `discovery_brief_TICKER.txt` — Foundational context
- `agent_outputs/agent1_technical.txt` — Technical analysis
- `agent_outputs/agent2_fundamental.txt` — Fundamental analysis
- `agent_outputs/agent3_sentiment.txt` — Sentiment analysis
- `agent_outputs/agent4_risk.txt` — Risk assessment
- `agent_outputs/agent5_thesis.txt` — Investment thesis
- `TRADE-ANALYSIS-TICKER.md` — Final comprehensive report

### Method 2: Bash Script (Semi-Automated)

**Creates framework and prompts, you run agents manually:**

```bash
./analyze_stock.sh MUTHOOTFIN NSE
```

**What it does:**
1. Creates discovery brief
2. Generates prompts for all 5 agents
3. Creates placeholder outputs
4. Shows commands to run agents manually

**Then you execute each agent:**
```bash
# Run each agent (can do in parallel in different terminals)
claude agentic --model sonnet < agent_outputs/agent1_technical_prompt.txt > agent_outputs/agent1_technical.txt
claude agentic --model sonnet < agent_outputs/agent2_fundamental_prompt.txt > agent_outputs/agent2_fundamental.txt
claude agentic --model sonnet < agent_outputs/agent3_sentiment_prompt.txt > agent_outputs/agent3_sentiment.txt
claude agentic --model sonnet < agent_outputs/agent4_risk_prompt.txt > agent_outputs/agent4_risk.txt
claude agentic --model sonnet < agent_outputs/agent5_thesis_prompt.txt > agent_outputs/agent5_thesis.txt
```

### Method 3: Manual Step-by-Step

For maximum control, run each step manually:

```bash
# 1. Create discovery brief
cat > discovery_brief_TICKER.txt <<EOF
Ticker: TICKER
Market: NSE
Date: $(date +%Y-%m-%d)
[Add company context here]
EOF

# 2. Create agent prompts (see examples below)
# 3. Run each agent with claude CLI
# 4. Synthesize results into final report
```

## Agent Prompt Templates

### Technical Analysis Agent

```
You are a Technical Analysis specialist analyzing [TICKER].

Use WebSearch and WebFetch to gather:
- Current price and recent price action
- Moving averages (20/50/200 EMA)
- RSI, MACD, Stochastic indicators
- Support and resistance levels
- Volume patterns and trends
- Chart patterns (flags, triangles, H&S, etc.)

Provide:
1. Trend Analysis (direction, MA alignment)
2. Support/Resistance (3+ levels each with reasoning)
3. Momentum Indicators (RSI, MACD, Stochastic)
4. Volume Analysis (vs averages, OBV, divergences)
5. Chart Patterns (active patterns with targets)
6. Additional Factors (Bollinger Bands, relative strength, Fibonacci)

SCORING (0-100):
- Trend Score: 0-20
- Momentum Score: 0-20
- Volume Score: 0-20
- Pattern Quality: 0-20
- Relative Strength: 0-20

OUTPUT:
## Technical Analysis: [TICKER]
### Technical Score: X/100
[Trend: X/20 | Momentum: X/20 | Volume: X/20 | Pattern: X/20 | Rel Strength: X/20]
### Signal: Bullish/Neutral/Bearish

[Detailed analysis]

### Key Levels
- Entry Zone: $X - $X
- Stop Loss: $X (X% risk)
- Target 1: $X (X% upside)
- Target 2: $X (X% upside)
```

### Fundamental Analysis Agent

```
You are a Fundamental Analysis specialist analyzing [TICKER].

Research using WebSearch:
- Valuation metrics (P/E, P/B, PEG, EV/EBITDA vs peers)
- Growth trajectory (revenue, earnings, guidance)
- Profitability (margins, ROE, ROIC)
- Financial health (debt, cash flow, liquidity)
- Competitive moat (brand, network effects, cost advantages)
- Management quality (ownership, track record, capital allocation)

SCORING (0-100):
- Valuation: 0-20
- Growth: 0-20
- Profitability: 0-20
- Financial Health: 0-20
- Moat Strength: 0-20

OUTPUT:
## Fundamental Analysis: [TICKER]
### Fundamental Score: X/100
[Valuation: X/20 | Growth: X/20 | Profitability: X/20 | Health: X/20 | Moat: X/20]
### Signal: Strong/Adequate/Weak

[Detailed analysis]
```

### Sentiment Analysis Agent

```
You are a Sentiment specialist analyzing [TICKER].

Research:
- News sentiment (recent headlines, positive/negative/neutral)
- Social media (Reddit, Twitter discussion volume and tone)
- Analyst ratings (consensus, price targets, upgrades/downgrades)
- Institutional activity (FII/DII flows, ownership trends)
- Insider trading (promoter buying/selling, pledged shares)
- Derivatives (short interest, put/call ratios, OI buildup)

SCORING (0-100):
- News Sentiment: 0-20
- Social Media: 0-20
- Analyst Ratings: 0-20
- Institutional Activity: 0-20
- Insider/Derivatives: 0-20

OUTPUT:
## Sentiment Analysis: [TICKER]
### Sentiment Score: X/100
[News: X/20 | Social: X/20 | Analysts: X/20 | Institutional: X/20 | Insider: X/20]
### Signal: Bullish/Neutral/Bearish

[Detailed analysis]
```

### Risk Assessment Agent

```
You are a Risk Assessment specialist analyzing [TICKER].

Assess:
- Volatility profile (historical vol, beta, ATR)
- Downside scenarios (bear case, max drawdown, stress tests)
- Correlation & macro risks (interest rates, regulatory)
- Liquidity risk (volume, spreads, float)
- Position sizing recommendations
- Top 10 risks with probability × impact matrix

SCORING (0-100, HIGHER = LOWER RISK):
- Volatility: 0-20 (20 = low vol)
- Downside Protection: 0-20 (20 = limited downside)
- Macro Resilience: 0-20 (20 = macro-resistant)
- Liquidity: 0-20 (20 = very liquid)
- Risk/Reward: 0-20 (20 = excellent R/R)

OUTPUT:
## Risk Assessment: [TICKER]
### Risk Score: X/100 (higher = lower risk)
[Volatility: X/20 | Downside: X/20 | Macro: X/20 | Liquidity: X/20 | R/R: X/20]
### Risk Level: Low/Moderate/High/Extreme

[Detailed analysis]
```

### Investment Thesis Agent

```
You are an Investment Thesis specialist building a complete thesis for [TICKER].

Develop:
1. Core Thesis (2-3 sentences: why this stock, why now)
2. Bull Case (5-7 catalysts, target price, probability)
3. Bear Case (5-7 risks, target price, probability)
4. Catalyst Calendar (upcoming events with dates and impact)
5. Entry/Exit Strategy (zones, stops, targets, sizing, timeframe)
6. Conviction Assessment (what gives/reduces conviction, invalidation triggers)

SCORING (0-100):
- Catalyst Clarity: 0-20
- Timing: 0-20
- Asymmetry: 0-20
- Edge: 0-20
- Conviction: 0-20

OUTPUT:
## Investment Thesis: [TICKER]
### Thesis Score: X/100
[Catalyst: X/20 | Timing: X/20 | Asymmetry: X/20 | Edge: X/20 | Conviction: X/20]
### Thesis: Strong/Moderate/Weak

[Detailed analysis with bull/bear cases, catalysts, strategy]
```

## Composite Scoring

The final Trade Score is calculated as:

```
Composite Score = (Technical × 0.25) + (Fundamental × 0.25) +
                  (Sentiment × 0.20) + (Risk × 0.15) + (Thesis × 0.15)
```

**Grade Mapping:**
- 85-100: A+ (Strong Buy)
- 70-84: A (Buy)
- 55-69: B (Hold/Accumulate)
- 40-54: C (Neutral)
- 25-39: D (Caution)
- 0-24: F (Avoid)

## Example Workflow

### Complete Analysis in 5 Minutes

```bash
# 1. Run Python orchestrator (fully automated)
python stock_analyzer.py MUTHOOTFIN --market NSE

# 2. Wait for completion (5-15 minutes depending on complexity)
# All 5 agents run in parallel

# 3. Review outputs
cat TRADE-ANALYSIS-MUTHOOTFIN.md

# 4. Check individual agent outputs if needed
cat agent_outputs/agent1_technical.txt
cat agent_outputs/agent2_fundamental.txt
cat agent_outputs/agent3_sentiment.txt
cat agent_outputs/agent4_risk.txt
cat agent_outputs/agent5_thesis.txt
```

### Batch Analysis (Multiple Stocks)

```bash
# Analyze multiple stocks
for ticker in MUTHOOTFIN MANAPPURAM IIFL BAJFINANCE; do
    echo "Analyzing $ticker..."
    python stock_analyzer.py $ticker --market NSE
    sleep 60  # Rate limiting
done

# Or use GNU parallel for faster execution
parallel -j 3 "python stock_analyzer.py {} --market NSE" ::: MUTHOOTFIN MANAPPURAM IIFL
```

## Customization

### Adjust Agent Weights

Edit `stock_analyzer.py`:

```python
self.weights = {
    "technical": 0.30,      # Increase technical weight
    "fundamental": 0.30,    # Increase fundamental weight
    "sentiment": 0.15,      # Decrease sentiment
    "risk": 0.15,          # Decrease risk
    "thesis": 0.10         # Decrease thesis
}
```

### Change Model

Use faster/cheaper model for agents:

```python
# In launch_agent method
cmd = [
    "claude",
    "agentic",
    "--model", "haiku",  # Use haiku instead of sonnet
    "--max-turns", "20",
    prompt
]
```

### Add Custom Agents

Add a 6th agent for sector analysis:

```python
agents_config["sector"] = {
    "description": "Sector Analysis for {ticker}",
    "prompt_file": self.base_dir / "prompts" / "agent6_sector_prompt.txt",
    "output_file": self.outputs_dir / "agent6_sector.txt"
}

# Update weights to include sector
self.weights["sector"] = 0.10
# Adjust other weights to sum to 1.0
```

## Troubleshooting

### Issue: Claude CLI not found

```bash
# Check if claude is installed
which claude

# Install if missing
npm install -g @anthropic-ai/claude-code

# Or add to PATH
export PATH="$PATH:/path/to/claude"
```

### Issue: API rate limits

```bash
# Add delays between agent launches
time.sleep(5)  # Wait 5 seconds between agents

# Or use exponential backoff
```

### Issue: Agent timeout

```bash
# Increase timeout in launch_agent
timeout=1800  # 30 minutes instead of 15
```

### Issue: Parsing agent scores fails

The script looks for patterns like:
- `Technical Score: 85/100`
- `### Score: 85/100`

Ensure agents output scores in this format.

## Advanced Usage

### Integration with Trading Bot

```python
from stock_analyzer import StockAnalyzer

def should_trade(ticker):
    analyzer = StockAnalyzer(ticker)
    report_path = analyzer.run_full_analysis()

    # Parse report and extract composite score
    with open(report_path) as f:
        content = f.read()

    # Extract score (implement parsing logic)
    score = extract_score(content)

    if score >= 70:
        return "BUY"
    elif score <= 40:
        return "SELL"
    else:
        return "HOLD"
```

### Scheduled Daily Analysis

```bash
# Add to crontab
0 9 * * 1-5 cd /path/to/analysis && python stock_analyzer.py NIFTY --market NSE
```

### Export to Dashboard

```python
# Export results to JSON
import json

results_json = {
    "ticker": ticker,
    "date": datetime.now().isoformat(),
    "composite_score": composite_score,
    "grade": grade,
    "signal": signal,
    "agent_scores": {
        "technical": tech_score,
        "fundamental": fund_score,
        "sentiment": sent_score,
        "risk": risk_score,
        "thesis": thesis_score
    }
}

with open(f"results_{ticker}.json", "w") as f:
    json.dump(results_json, f, indent=2)
```

## Performance Tips

1. **Parallel Execution**: Python orchestrator runs all 5 agents in parallel (5x faster)
2. **Model Selection**: Use `haiku` for faster (but less detailed) analysis
3. **Caching**: Cache discovery briefs to avoid redundant web searches
4. **Rate Limiting**: Add delays between API calls to avoid throttling
5. **Batch Processing**: Analyze multiple stocks in one session

## Cost Estimation

**Per Stock Analysis (using Sonnet model):**
- 5 agents × ~50K tokens each = ~250K tokens total
- At $3 per million tokens = ~$0.75 per stock analysis

**Cost Optimization:**
- Use Haiku model: ~$0.15 per analysis (5x cheaper)
- Cache common data: Save ~20% tokens
- Adjust max-turns: Reduce from 30 to 20 turns

## Comparison: Script vs Skill

| Feature | This Script | `/trade-analyze` Skill |
|---------|-------------|------------------------|
| Token Usage | Full control | Fixed skill cost |
| Customization | Fully customizable | Limited |
| Parallel Execution | Yes (Python) | Yes |
| Model Selection | Configurable | Fixed (Sonnet) |
| Weight Adjustment | Easy | Not possible |
| Add Custom Agents | Supported | Not possible |
| Debugging | Full visibility | Limited |
| Cost | Pay per use | Skill tokens |

## Limitations

1. **No Risk-Free Rate**: Unlike Bloomberg terminal, can't access risk-free rate data automatically
2. **Real-Time Data**: Depends on web search quality and recency
3. **Accuracy**: AI analysis may contain errors; always verify independently
4. **Rate Limits**: Claude API has rate limits; may need delays between requests
5. **Market Hours**: Analysis quality may vary during/after market hours

## Support & Contributing

For issues or improvements:
1. Check existing agent outputs for errors
2. Verify API key and CLI setup
3. Test with a simple ticker first (e.g., AAPL)
4. Review prompt templates for accuracy

## Disclaimer

**THIS IS FOR EDUCATIONAL PURPOSES ONLY. NOT FINANCIAL ADVICE.**

- Always conduct your own due diligence
- Verify all data independently
- Consult qualified financial advisors
- AI analysis may contain errors or outdated information
- Past performance does not guarantee future results
- Stock investments carry risk of capital loss

---

## Quick Reference

```bash
# Basic usage
python stock_analyzer.py TICKER --market NSE

# With bash script
./analyze_stock.sh TICKER NSE

# Manual agent execution
claude agentic --model sonnet < prompt.txt > output.txt

# View results
cat TRADE-ANALYSIS-TICKER.md
```

**Happy Analyzing! 📈**
