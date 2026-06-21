# Quick Start Guide - Stock Analysis Without Skill Tokens

Get started analyzing stocks in under 5 minutes!

## ⚡ Fastest Way (3 Steps)

### Option 1: Using Existing `TRADE-ANALYSIS-MUTHOOTFIN.md` as Template

You already have a complete analysis! Just modify it for new stocks:

```bash
# 1. Copy the existing analysis as template
cp TRADE-ANALYSIS-MUTHOOTFIN.md TRADE-ANALYSIS-NEWSTOCK.md

# 2. Search and replace ticker name
sed -i '' 's/MUTHOOTFIN/NEWSTOCK/g' TRADE-ANALYSIS-NEWSTOCK.md
sed -i '' 's/Muthoot Finance/New Company Name/g' TRADE-ANALYSIS-NEWSTOCK.md

# 3. Update with new data (manually or run agents)
```

### Option 2: Minimal Manual Process

Create a simple script that asks Claude to do everything:

```bash
#!/bin/bash
# simple_analyze.sh

TICKER=$1

cat <<EOF | claude --model sonnet
Perform a comprehensive stock analysis for ${TICKER} (NSE) with 5 dimensions:

1. TECHNICAL ANALYSIS (Score 0-100)
   - Trend, momentum, volume, patterns, relative strength
   - Provide current price, support/resistance, entry/exit levels

2. FUNDAMENTAL ANALYSIS (Score 0-100)
   - Valuation, growth, profitability, financial health, moat
   - Include P/E, ROE, margins, debt ratios

3. SENTIMENT ANALYSIS (Score 0-100)
   - News, social media, analyst ratings, institutional flows
   - Insider trading, derivatives activity

4. RISK ASSESSMENT (Score 0-100, higher = lower risk)
   - Volatility, downside scenarios, macro risks, liquidity
   - Position sizing recommendations

5. INVESTMENT THESIS (Score 0-100)
   - Bull case (targets, catalysts, probability)
   - Bear case (risks, targets, probability)
   - Entry/exit strategy with specific price levels

Calculate composite score as:
(Technical × 0.25) + (Fundamental × 0.25) + (Sentiment × 0.20) + (Risk × 0.15) + (Thesis × 0.15)

Provide letter grade (A+ to F) and signal (Strong Buy to Avoid).

Format output as a comprehensive markdown report with:
- Executive summary
- Trade score dashboard
- Detailed analysis for each dimension
- Entry/exit strategy table
- Bull vs bear comparison
- Risk factors
- Final recommendation

Use WebSearch extensively to get current, accurate data.
Save output to TRADE-ANALYSIS-${TICKER}.md
EOF
```

**Usage:**
```bash
chmod +x simple_analyze.sh
./simple_analyze.sh TICKER
```

### Option 3: Python One-Liner

```python
# quick_analyze.py
import subprocess, sys

ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
prompt = f"""
Analyze {ticker} stock comprehensively:
1. Technical (0-100): trend, momentum, volume, patterns
2. Fundamental (0-100): valuation, growth, profitability, health, moat
3. Sentiment (0-100): news, analysts, institutional, insider
4. Risk (0-100): volatility, downside, macro, liquidity
5. Thesis (0-100): bull/bear cases, catalysts, strategy

Composite = Tech×0.25 + Fund×0.25 + Sent×0.20 + Risk×0.15 + Thesis×0.15
Provide grade (A+ to F) and signal (Strong Buy to Avoid).
Generate detailed markdown report with entry/exit levels.
Save to TRADE-ANALYSIS-{ticker}.md
"""

subprocess.run(["claude", "--model", "sonnet", prompt])
```

**Usage:**
```bash
python quick_analyze.py TICKER
```

## 🚀 Using the Full Framework

### Step 1: Make Scripts Executable

```bash
chmod +x analyze_stock.sh
chmod +x stock_analyzer.py
```

### Step 2: Run Analysis

**Python (Automated):**
```bash
python stock_analyzer.py MUTHOOTFIN --market NSE
```

**Bash (Semi-Automated):**
```bash
./analyze_stock.sh MUTHOOTFIN NSE
```

### Step 3: View Results

```bash
cat TRADE-ANALYSIS-MUTHOOTFIN.md
```

## 📋 Manual Agent Execution (If You Want Control)

The bash script creates prompt files. Run each agent individually:

```bash
# Technical Analysis
claude agentic --model sonnet < agent_outputs/agent1_technical_prompt.txt > agent_outputs/agent1_technical.txt

# Fundamental Analysis
claude agentic --model sonnet < agent_outputs/agent2_fundamental_prompt.txt > agent_outputs/agent2_fundamental.txt

# Sentiment Analysis
claude agentic --model sonnet < agent_outputs/agent3_sentiment_prompt.txt > agent_outputs/agent3_sentiment.txt

# Risk Assessment
claude agentic --model sonnet < agent_outputs/agent4_risk_prompt.txt > agent_outputs/agent4_risk.txt

# Investment Thesis
claude agentic --model sonnet < agent_outputs/agent5_thesis_prompt.txt > agent_outputs/agent5_thesis.txt
```

## 🎯 What You Get

Every analysis produces:

1. **TRADE-ANALYSIS-TICKER.md** — Comprehensive report with:
   - Executive summary
   - Composite trade score (0-100)
   - Grade (A+ to F) and signal (Strong Buy to Avoid)
   - Technical analysis with entry/exit levels
   - Fundamental deep-dive
   - Sentiment assessment
   - Risk analysis with position sizing
   - Investment thesis with bull/bear cases

2. **Agent Output Files**:
   - `agent1_technical.txt` — Chart analysis
   - `agent2_fundamental.txt` — Valuation & financials
   - `agent3_sentiment.txt` — Market perception
   - `agent4_risk.txt` — Risk assessment
   - `agent5_thesis.txt` — Investment thesis

3. **Discovery Brief**: Context document agents use

## 🔧 Troubleshooting

**Problem: `claude: command not found`**
```bash
# Install claude-code CLI
npm install -g @anthropic-ai/claude-code
```

**Problem: Python script fails**
```bash
# Check Python version (need 3.8+)
python --version

# Run with python3 explicitly
python3 stock_analyzer.py TICKER --market NSE
```

**Problem: Agents take too long**
```bash
# Use faster haiku model
claude agentic --model haiku < prompt.txt > output.txt
```

**Problem: Need to stop using skill tokens**

Just use these scripts instead of `/trade-analyze TICKER`!

## 💡 Pro Tips

### Batch Analyze Multiple Stocks

```bash
# Sequential
for ticker in MUTHOOTFIN MANAPPURAM BAJFINANCE; do
    python stock_analyzer.py $ticker --market NSE
done

# Parallel (faster)
parallel python stock_analyzer.py {} --market NSE ::: MUTHOOTFIN MANAPPURAM BAJFINANCE
```

### Create a Cron Job (Daily Analysis)

```bash
# Add to crontab (runs every weekday at 9 AM)
crontab -e

# Add this line:
0 9 * * 1-5 cd /path/to/analysis && python stock_analyzer.py NIFTY50 --market NSE
```

### Compare Multiple Stocks

```bash
# Analyze 3 stocks
python stock_analyzer.py MUTHOOTFIN --market NSE
python stock_analyzer.py MANAPPURAM --market NSE
python stock_analyzer.py BAJFINANCE --market NSE

# Compare scores
grep "Composite Trade Score" TRADE-ANALYSIS-*.md
```

## 📊 Cost Comparison

**Using Skill:**
- `/trade-analyze TICKER` = 1 skill token
- Limited customization

**Using These Scripts:**
- ~$0.75 per analysis (Sonnet model)
- ~$0.15 per analysis (Haiku model)
- Full customization
- Can adjust weights, add agents, modify prompts

## 🎓 Learning Path

1. **Start Simple**: Run `./simple_analyze.sh TICKER`
2. **Understand Agents**: Read the prompt templates
3. **Customize**: Modify agent prompts for your needs
4. **Automate**: Set up cron jobs or trading bot integration
5. **Optimize**: Use caching, parallel execution, model selection

## 📁 Files You Need

**Minimum:**
- `simple_analyze.sh` — Basic one-command analysis
- OR `quick_analyze.py` — Python one-liner

**Full Framework:**
- `stock_analyzer.py` — Python orchestrator (automated)
- `analyze_stock.sh` — Bash orchestrator (semi-automated)
- `README-STOCK-ANALYZER.md` — Full documentation

**Generated:**
- `TRADE-ANALYSIS-{TICKER}.md` — Your comprehensive report
- `agent_outputs/` — Individual agent analyses
- `discovery_brief_{TICKER}.txt` — Context document

## ✅ Quick Checklist

- [ ] Claude CLI installed (`which claude`)
- [ ] API key configured (`echo $ANTHROPIC_API_KEY`)
- [ ] Scripts are executable (`chmod +x *.sh *.py`)
- [ ] Python 3.8+ available (`python --version`)
- [ ] Output directories created (`mkdir -p agent_outputs prompts`)

## 🚦 Start Now!

```bash
# One command to rule them all
python stock_analyzer.py MUTHOOTFIN --market NSE

# Then view the report
cat TRADE-ANALYSIS-MUTHOOTFIN.md
```

---

**Need help? Check `README-STOCK-ANALYZER.md` for detailed documentation.**

**Want to customize? Edit the prompt templates in the scripts.**

**Happy Analyzing! 📈🎯**
