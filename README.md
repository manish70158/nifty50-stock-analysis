# Stock Analysis Framework

Comprehensive multi-dimensional stock analysis system with automated scoring and recommendations. Includes both batch analysis (Nifty 50) and individual stock deep-dive capabilities.

---

## 📊 Overview

This project provides two complementary analysis tools:

1. **Nifty 50 Batch Analyzer** - Rank all 50 Nifty stocks by composite score
2. **Individual Stock Analyzer** - Deep-dive comprehensive analysis of any stock (no skill tokens required)

---

## 🚀 Quick Start - Individual Stock Analysis

**Analyze any stock in one command:**

```bash
# Simplest method (recommended)
./simple_analyze.sh MUTHOOTFIN NSE

# View the report
cat TRADE-ANALYSIS-MUTHOOTFIN.md
```

**Output:** Comprehensive 15-20 page analysis with:
- Composite Trade Score (0-100)
- Letter Grade (A+ to F)
- Trading Signal (Strong Buy to Avoid)
- Technical analysis with entry/exit levels
- Fundamental deep-dive with valuation
- Sentiment analysis with analyst ratings
- Risk assessment with position sizing
- Investment thesis with bull/bear cases

**Time:** 3-5 minutes | **Cost:** ~$0.50-0.75 per analysis

---

## 📁 Project Structure

### Individual Stock Analysis Tools (NEW)

```
simple_analyze.sh          # ⭐ One-command comprehensive analysis
analyze_stock.sh           # Manual multi-agent framework
stock_analyzer.py          # Python automation with parallel agents

QUICKSTART.md             # Quick start guide
README-STOCK-ANALYZER.md  # Detailed documentation
COMMANDS_CHEATSHEET.txt   # Command reference
CREATED_FILES_SUMMARY.md  # System overview
```

### Nifty 50 Batch Analysis (Original)

```
nifty50_analyzer.py                    # Batch analysis script
nifty50_analysis_2026-05-09.csv       # Ranked results for all 50 stocks
.claude/skills/nifty50-analyzer/      # Claude skill configuration
```

### Output Files

```
TRADE-ANALYSIS-{TICKER}.md            # Individual stock reports
agent_outputs/agent*.txt              # Individual agent analyses
discovery_brief_{TICKER}.txt          # Context documents
```

---

## 🎯 Individual Stock Analysis - Usage Guide

### Method 1: Simple One-Command Analysis (Recommended)

**Use when:** You want fastest results with one command

```bash
# Analyze any NSE stock
./simple_analyze.sh TICKER NSE

# Analyze any NYSE/NASDAQ stock
./simple_analyze.sh TICKER NYSE

# Examples
./simple_analyze.sh MUTHOOTFIN NSE
./simple_analyze.sh RELIANCE NSE
./simple_analyze.sh AAPL NYSE
```

**Features:**
- ✅ Single Claude API call (cost-effective)
- ✅ Complete analysis in 3-5 minutes
- ✅ No manual steps required
- ✅ Full comprehensive report

### Method 2: Multi-Agent Framework (Manual Control)

**Use when:** You want to understand the system or run specific agents only

```bash
# Step 1: Generate framework and prompts
./analyze_stock.sh MUTHOOTFIN NSE

# Step 2: Run agents individually (can do in parallel)
claude agentic --model sonnet < agent_outputs/agent1_technical_prompt.txt > agent_outputs/agent1_technical.txt
claude agentic --model sonnet < agent_outputs/agent2_fundamental_prompt.txt > agent_outputs/agent2_fundamental.txt
claude agentic --model sonnet < agent_outputs/agent3_sentiment_prompt.txt > agent_outputs/agent3_sentiment.txt
claude agentic --model sonnet < agent_outputs/agent4_risk_prompt.txt > agent_outputs/agent4_risk.txt
claude agentic --model sonnet < agent_outputs/agent5_thesis_prompt.txt > agent_outputs/agent5_thesis.txt

# Step 3: View individual agent outputs
cat agent_outputs/agent1_technical.txt
```

**Features:**
- ✅ Full visibility into each agent
- ✅ Run only the agents you need
- ✅ Customize individual prompts
- ✅ Learn how the system works

### Method 3: Python Automation (Batch Processing)

**Use when:** You need to analyze multiple stocks or integrate with other tools

```bash
# Single stock
python stock_analyzer.py MUTHOOTFIN --market NSE

# Batch analysis (sequential)
for ticker in MUTHOOTFIN MANAPPURAM BAJFINANCE; do
    python stock_analyzer.py $ticker --market NSE
done

# Batch analysis (parallel - faster)
parallel python stock_analyzer.py {} --market NSE ::: MUTHOOTFIN MANAPPURAM BAJFINANCE
```

**Features:**
- ✅ All 5 agents run in parallel (faster)
- ✅ Automatic score calculation
- ✅ Can be integrated into cron jobs
- ✅ Python-based for easy integration

---

## 📊 Analysis Framework

### The 5-Agent System

Each stock is analyzed by 5 specialized AI agents:

```
┌─────────────────────────────────────────────────────────┐
│ 1. TECHNICAL ANALYSIS AGENT          | Weight: 25%     │
│    • Trend, momentum, volume, patterns                  │
│    • Support/resistance levels                          │
│    • Entry/exit recommendations                         │
│    Score: 0-100 (breakdown: 5 × 0-20 subscores)        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 2. FUNDAMENTAL ANALYSIS AGENT        | Weight: 25%     │
│    • Valuation (P/E, P/B, PEG)                         │
│    • Growth trajectory                                  │
│    • Profitability (ROE, margins)                      │
│    • Financial health (debt, cash flow)                │
│    • Competitive moat assessment                        │
│    Score: 0-100 (breakdown: 5 × 0-20 subscores)        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 3. SENTIMENT ANALYSIS AGENT          | Weight: 20%     │
│    • News sentiment & catalysts                         │
│    • Analyst ratings & price targets                    │
│    • Institutional activity (FII/DII)                  │
│    • Insider trading patterns                           │
│    • Social media & retail sentiment                    │
│    Score: 0-100 (breakdown: 5 × 0-20 subscores)        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 4. RISK ASSESSMENT AGENT             | Weight: 15%     │
│    • Volatility profile & beta                          │
│    • Downside scenarios & max drawdown                  │
│    • Macro & regulatory risks                           │
│    • Liquidity assessment                               │
│    • Position sizing recommendations                    │
│    Score: 0-100 (higher = lower risk)                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 5. INVESTMENT THESIS AGENT           | Weight: 15%     │
│    • Bull case with catalysts & targets                │
│    • Bear case with risks & targets                    │
│    • Catalyst calendar (upcoming events)               │
│    • Entry/exit strategy                                │
│    • Conviction assessment                              │
│    Score: 0-100 (breakdown: 5 × 0-20 subscores)        │
└─────────────────────────────────────────────────────────┘
```

### Composite Score Calculation

```
Composite Score = (Technical × 0.25) + (Fundamental × 0.25) +
                  (Sentiment × 0.20) + (Risk × 0.15) + (Thesis × 0.15)
```

### Grade & Signal Mapping

| Score Range | Grade | Signal | Action |
|-------------|-------|--------|--------|
| 85-100 | A+ | Strong Buy | 🟢 Highly attractive |
| 70-84 | A | Buy | 🟢 Attractive |
| 55-69 | B | Hold/Accumulate | 🟡 Neutral to positive |
| 40-54 | C | Neutral | 🟡 Wait and watch |
| 25-39 | D | Caution | 🔴 Avoid or reduce |
| 0-24 | F | Avoid | 🔴 Do not buy |

---

## 📋 Example: MUTHOOTFIN Analysis Results

**Composite Trade Score:** 71/100 (Grade A)
**Signal:** BUY

**Dimension Scores:**
- Technical: 58/100 (Neutral with bearish bias - at critical support)
- Fundamental: 84/100 (Strong - exceptional profitability, 31% ROE, 34% margins)
- Sentiment: 68/100 (Neutral to bullish - recent analyst upgrade)
- Risk: Not completed
- Thesis: 73/100 (Strong - compelling valuation at 12x P/E for 25%+ growth)

**Key Findings:**
- Trading at ₹3,153 (24% below January high)
- Entry Zone: ₹2,900-3,200
- Stop Loss: ₹2,600 (15% risk)
- Target 1: ₹4,200 (33% upside)
- Target 2: ₹5,500 (74% upside)
- Risk/Reward: 1:3 to 1:4

See `TRADE-ANALYSIS-MUTHOOTFIN.md` for full 15-page analysis.

---

## 🏆 Nifty 50 Batch Analysis

### Top 10 Stocks by Trade Score

1. **Kotak Mahindra Bank** - 91 (Strong Buy)
2. **Reliance Industries** - 90 (Strong Buy)
3. **Hero MotoCorp** - 89 (Strong Buy)
4. **Shriram Finance** - 87 (Strong Buy)
5. **Dr. Reddy's Labs** - 86 (Strong Buy)
6. **M&M** - 85 (Strong Buy)
7. **ICICI Bank** - 84 (Strong Buy)
8. **HDFC Bank** - 83 (Strong Buy)
9. **State Bank of India** - 81 (Strong Buy)
10. **BPCL** - 80 (Strong Buy)

### Running Nifty 50 Analysis

```bash
# Activate virtual environment
source venv/bin/activate

# Run the batch analyzer
python nifty50_analyzer.py

# Output: nifty50_analysis_YYYY-MM-DD.csv
```

**Output Format:** CSV with rankings, scores, and recommendations for all 50 stocks

---

## 💰 Cost Comparison

### Individual Stock Analysis

| Method | Cost | Time | Use Case |
|--------|------|------|----------|
| **simple_analyze.sh** | **~$0.50-0.75** | **3-5 min** | **Quick one-off analysis** |
| analyze_stock.sh | ~$0.75-1.00 | 10-15 min | Learning/debugging |
| stock_analyzer.py | ~$0.75-1.00 | 5-10 min | Batch/automation |
| `/trade-analyze` skill | 1 skill token | 5-10 min | Limited customization |

**Cost Optimization:** Use `--model haiku` for 5x cheaper analysis (~$0.15 per stock)

### Nifty 50 Batch Analysis

- **Cost:** ~$25-40 for all 50 stocks (depending on model)
- **Time:** 2-4 hours for complete batch
- **Frequency:** Run weekly or monthly for updated rankings

---

## 🛠️ Installation & Setup

### Prerequisites

```bash
# 1. Install Claude CLI
npm install -g @anthropic-ai/claude-code

# 2. Set API key
export ANTHROPIC_API_KEY="your-api-key-here"

# 3. Verify installation
claude --version
```

### Python Setup (for stock_analyzer.py and nifty50_analyzer.py)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install yfinance pandas numpy anthropic

# Verify
python --version  # Should be 3.8+
```

### Make Scripts Executable

```bash
chmod +x simple_analyze.sh
chmod +x analyze_stock.sh
chmod +x stock_analyzer.py
```

---

## 📖 Documentation

- **`QUICKSTART.md`** - Get started in 5 minutes
- **`README-STOCK-ANALYZER.md`** - Complete technical documentation
- **`COMMANDS_CHEATSHEET.txt`** - Quick command reference
- **`CREATED_FILES_SUMMARY.md`** - Detailed system overview

---

## 🎓 Usage Examples

### Example 1: Analyze Your Watchlist

```bash
# Morning routine: analyze watchlist
./simple_analyze.sh MUTHOOTFIN NSE
./simple_analyze.sh MANAPPURAM NSE
./simple_analyze.sh BAJFINANCE NSE

# Compare scores
grep "Composite Trade Score" TRADE-ANALYSIS-*.md

# Output:
# TRADE-ANALYSIS-MUTHOOTFIN.md:  71/100 (Grade A)
# TRADE-ANALYSIS-MANAPPURAM.md:  65/100 (Grade B)
# TRADE-ANALYSIS-BAJFINANCE.md:  82/100 (Grade A)
```

### Example 2: Deep Dive on Top Nifty 50 Stock

```bash
# First, identify top stocks from batch analysis
head -11 nifty50_analysis_2026-05-09.csv

# Then deep-dive on the top pick
./simple_analyze.sh KOTAKBANK NSE

# Review the comprehensive report
cat TRADE-ANALYSIS-KOTAKBANK.md
```

### Example 3: Automated Daily Analysis

```bash
# Add to crontab for daily analysis at 9 AM (weekdays)
crontab -e

# Add this line:
0 9 * * 1-5 cd /path/to/analysis && ./simple_analyze.sh NIFTY NSE
```

### Example 4: Compare Similar Stocks

```bash
# Analyze competing companies
./simple_analyze.sh MUTHOOTFIN NSE
./simple_analyze.sh MANAPPURAM NSE

# Extract key metrics for comparison
grep -A 5 "Trade Score Dashboard" TRADE-ANALYSIS-MUTHOOTFIN.md
grep -A 5 "Trade Score Dashboard" TRADE-ANALYSIS-MANAPPURAM.md
```

---

## 🔧 Customization

### Adjust Agent Weights

Edit `stock_analyzer.py`:

```python
self.weights = {
    "technical": 0.30,      # Increase technical weight
    "fundamental": 0.30,    # Increase fundamental weight
    "sentiment": 0.15,      # Decrease sentiment
    "risk": 0.15,
    "thesis": 0.10
}
```

### Change AI Model

For faster/cheaper analysis:

```bash
# In scripts, change:
--model sonnet  # Current (best quality)
--model haiku   # 5x cheaper, slightly less detailed
--model opus    # Highest quality (most expensive)
```

### Add Custom Agents

Create a 6th agent for sector analysis:

```python
# In stock_analyzer.py
agents_config["sector"] = {
    "description": "Sector Analysis for {ticker}",
    "prompt_file": self.base_dir / "prompts" / "agent6_sector_prompt.txt",
    "output_file": self.outputs_dir / "agent6_sector.txt"
}

# Update weights
self.weights["sector"] = 0.10
```

---

## 🚨 Troubleshooting

### Issue: `claude: command not found`

```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-code

# Or add to PATH
export PATH="$PATH:/path/to/claude"
```

### Issue: `Permission denied` when running scripts

```bash
chmod +x simple_analyze.sh analyze_stock.sh stock_analyzer.py
```

### Issue: Python script fails

```bash
# Check Python version (need 3.8+)
python --version

# Activate virtual environment
source venv/bin/activate

# Run with python3 explicitly
python3 stock_analyzer.py TICKER --market NSE
```

### Issue: API rate limits

```bash
# Add delay between analyses
sleep 60

# Or use Haiku model (smaller, faster)
--model haiku
```

---

## 📊 Technology Stack

### Individual Stock Analysis
- **Bash** - Shell scripting for simple_analyze.sh and analyze_stock.sh
- **Python 3.8+** - Automation and parallel processing
- **Claude CLI** - AI agent orchestration
- **Anthropic API** - Claude Sonnet/Opus/Haiku models

### Nifty 50 Batch Analysis
- **Python 3.11+**
- **yfinance** - Market data fetching
- **pandas** - Data manipulation and CSV generation
- **numpy** - Numerical calculations

---

## 📅 Analysis Date

- **Individual Stock Analyses:** Real-time (generated on demand)
- **Nifty 50 Batch Analysis:** May 9, 2026
- **MUTHOOTFIN Deep Dive:** June 7, 2026

---

## 🎯 Use Cases

### For Individual Investors
- ✅ Research stocks before investing
- ✅ Get unbiased AI analysis
- ✅ Understand risk/reward profile
- ✅ Set proper entry/exit levels

### For Traders
- ✅ Technical setups with precise levels
- ✅ Short-term catalyst identification
- ✅ Position sizing recommendations
- ✅ Risk management guidelines

### For Portfolio Managers
- ✅ Batch analyze entire universe
- ✅ Rank stocks by composite score
- ✅ Compare similar companies
- ✅ Monitor watchlist systematically

### For Researchers
- ✅ Study AI-driven analysis methodology
- ✅ Understand multi-agent systems
- ✅ Validate against fundamental research
- ✅ Educational tool for learning

---

## 🌟 Key Features

### Individual Stock Analyzer
✅ **No skill tokens required** - Use API credits directly
✅ **Full customization** - Adjust weights, models, agents
✅ **Parallel execution** - Faster analysis with Python
✅ **Comprehensive reports** - 15-20 page deep-dives
✅ **Actionable insights** - Specific entry/exit levels
✅ **Bull/bear scenarios** - Probability-weighted returns

### Nifty 50 Analyzer
✅ **Batch processing** - All 50 stocks in one run
✅ **Ranked output** - CSV sorted by composite score
✅ **Consistent scoring** - Same methodology for all
✅ **Easy comparison** - Side-by-side metrics

---

## ⚠️ Important Disclaimer

**THIS IS FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY. NOT FINANCIAL ADVICE.**

- Always conduct your own due diligence
- Verify AI-generated analysis with independent research
- Check current prices and data from official sources
- Consult qualified financial advisors before investing
- Past performance does not guarantee future results
- Stock investments carry risk of capital loss
- AI analysis may contain errors or outdated information
- Use proper risk management and position sizing
- Never invest more than you can afford to lose

---

## 📝 License

This project is for educational and personal use only.

---

## 🙏 Acknowledgments

- Claude AI (Anthropic) for powering the analysis agents
- Yahoo Finance for market data (Nifty 50 analyzer)
- Open source community for tools and libraries

---

## 📞 Support

**For questions or issues:**

1. Check documentation:
   - `QUICKSTART.md` for quick start
   - `README-STOCK-ANALYZER.md` for detailed docs
   - `COMMANDS_CHEATSHEET.txt` for commands

2. Review example output:
   - `TRADE-ANALYSIS-MUTHOOTFIN.md` for sample report

3. Test with simple command:
   ```bash
   ./simple_analyze.sh AAPL NYSE
   ```

---

## 🚀 Quick Commands Reference

```bash
# INDIVIDUAL STOCK ANALYSIS
./simple_analyze.sh TICKER NSE              # One-command analysis
./analyze_stock.sh TICKER NSE               # Manual multi-agent
python stock_analyzer.py TICKER --market NSE # Python automation

# NIFTY 50 BATCH ANALYSIS
python nifty50_analyzer.py                  # Analyze all 50 stocks

# VIEW RESULTS
cat TRADE-ANALYSIS-TICKER.md               # Full report
grep "Composite" TRADE-ANALYSIS-*.md       # Compare scores
cat nifty50_analysis_*.csv                 # Batch rankings

# BATCH ANALYSIS
for t in T1 T2 T3; do ./simple_analyze.sh $t NSE; done

# HELP
cat QUICKSTART.md                          # Quick start guide
cat COMMANDS_CHEATSHEET.txt                # Command reference
```

---

**Ready to start? Run your first analysis:**

```bash
./simple_analyze.sh MUTHOOTFIN NSE
```

**Then view the report:**

```bash
cat TRADE-ANALYSIS-MUTHOOTFIN.md
```

**Happy Analyzing! 📈🎯**
