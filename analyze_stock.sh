#!/bin/bash
# Comprehensive Stock Analysis Script
# Usage: ./analyze_stock.sh TICKER [MARKET]
# Example: ./analyze_stock.sh MUTHOOTFIN NSE

set -e

TICKER="${1:-}"
MARKET="${2:-NSE}"
DATE=$(date +"%Y-%m-%d")
BASE_DIR=$(pwd)
OUTPUTS_DIR="$BASE_DIR/agent_outputs"
DISCOVERY_FILE="$BASE_DIR/discovery_brief_${TICKER}.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if ticker is provided
if [ -z "$TICKER" ]; then
    echo -e "${RED}Error: Ticker symbol required${NC}"
    echo "Usage: $0 TICKER [MARKET]"
    echo "Example: $0 MUTHOOTFIN NSE"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUTS_DIR"

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  COMPREHENSIVE STOCK ANALYSIS: $TICKER${NC}"
echo -e "${BLUE}  Market: $MARKET | Date: $DATE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"

# ============================================================================
# PHASE 1: DISCOVERY
# ============================================================================
echo -e "${YELLOW}PHASE 1: DISCOVERY${NC}\n"

cat > "$DISCOVERY_FILE" <<EOF
═══════════════════════════════════════════════════════════════
DISCOVERY BRIEF: $TICKER
Analysis Date: $DATE
Market: $MARKET
═══════════════════════════════════════════════════════════════

This brief provides foundational context for analysis agents.
Each agent will perform additional web research for their domain.

STATUS: Ready for agent deployment
═══════════════════════════════════════════════════════════════
EOF

echo -e "${GREEN}✓${NC} Discovery brief created: $DISCOVERY_FILE\n"

# ============================================================================
# PHASE 2: PARALLEL AGENT DEPLOYMENT
# ============================================================================
echo -e "${YELLOW}PHASE 2: LAUNCHING 5 PARALLEL AGENTS${NC}\n"

# Function to launch an agent
launch_agent() {
    local AGENT_NAME=$1
    local AGENT_NUM=$2
    local OUTPUT_FILE="$OUTPUTS_DIR/agent${AGENT_NUM}_${AGENT_NAME}.txt"
    local PROMPT_FILE="$OUTPUTS_DIR/agent${AGENT_NUM}_${AGENT_NAME}_prompt.txt"

    echo -e "${BLUE}🚀 Launching Agent $AGENT_NUM: ${AGENT_NAME}...${NC}"

    # Create agent-specific prompt
    create_agent_prompt "$AGENT_NAME" "$AGENT_NUM" "$PROMPT_FILE"

    # Launch agent using claude (this will be replaced with actual implementation)
    # For now, create a placeholder
    {
        echo "## $AGENT_NAME Analysis: $TICKER"
        echo "### Score: [Pending]/100"
        echo ""
        echo "Analysis in progress..."
        echo ""
        echo "Agent was launched with prompt from: $PROMPT_FILE"
        echo "Discovery brief: $DISCOVERY_FILE"
        echo ""
        echo "To actually run this agent, you would execute:"
        echo "claude agentic --model sonnet --max-turns 30 < $PROMPT_FILE > $OUTPUT_FILE"
    } > "$OUTPUT_FILE"

    echo -e "${GREEN}✓${NC} Agent $AGENT_NUM ($AGENT_NAME) output: $OUTPUT_FILE"
}

# Create agent prompts
create_agent_prompt() {
    local AGENT_NAME=$1
    local AGENT_NUM=$2
    local PROMPT_FILE=$3

    local DISCOVERY_CONTENT=$(cat "$DISCOVERY_FILE")

    case $AGENT_NAME in
        "technical")
            cat > "$PROMPT_FILE" <<EOF
You are a Technical Analysis specialist. Analyze $TICKER comprehensively using WebSearch and WebFetch.

DISCOVERY DATA:
$DISCOVERY_CONTENT

YOUR MANDATE:
1. Gather current price data, charts, and technical indicators
2. Analyze trend, momentum, volume, patterns, and relative strength
3. Provide specific support/resistance levels with entry/exit strategy
4. Score: Trend (0-20), Momentum (0-20), Volume (0-20), Pattern (0-20), Rel Strength (0-20)

OUTPUT FORMAT:
## Technical Analysis: $TICKER
### Technical Score: [X]/100
[Trend: X/20 | Momentum: X/20 | Volume: X/20 | Pattern: X/20 | Rel Strength: X/20]
### Signal: [Bullish/Neutral/Bearish]

[Detailed analysis with 6 sections: Trend, Support/Resistance, Momentum, Volume, Patterns, Additional Factors]

### Key Levels
- Entry Zone: ₹X - ₹X
- Stop Loss: ₹X (X% risk)
- Target 1: ₹X (X% upside)
- Target 2: ₹X (X% upside)

Save to: $OUTPUTS_DIR/agent1_technical.txt
EOF
            ;;
        "fundamental")
            cat > "$PROMPT_FILE" <<EOF
You are a Fundamental Analysis specialist. Analyze $TICKER comprehensively.

DISCOVERY DATA:
$DISCOVERY_CONTENT

YOUR MANDATE:
1. Research valuation metrics (P/E, P/B, PEG, EV/EBITDA vs peers)
2. Analyze growth trajectory (revenue, earnings, forecasts)
3. Assess profitability (margins, ROE, ROIC)
4. Evaluate financial health (debt, cash flow, liquidity)
5. Determine competitive moat strength
6. Review management quality

SCORING:
- Valuation (0-20)
- Growth (0-20)
- Profitability (0-20)
- Financial Health (0-20)
- Moat (0-20)

OUTPUT FORMAT:
## Fundamental Analysis: $TICKER
### Fundamental Score: [X]/100
[Valuation: X/20 | Growth: X/20 | Profitability: X/20 | Health: X/20 | Moat: X/20]
### Signal: [Strong/Adequate/Weak]

[Detailed analysis]

Save to: $OUTPUTS_DIR/agent2_fundamental.txt
EOF
            ;;
        "sentiment")
            cat > "$PROMPT_FILE" <<EOF
You are a Sentiment & Momentum specialist. Analyze $TICKER.

DISCOVERY DATA:
$DISCOVERY_CONTENT

YOUR MANDATE:
1. News sentiment (recent headlines, catalyst identification)
2. Social media buzz (Reddit, Twitter discussion)
3. Analyst ratings (consensus, price targets, upgrades/downgrades)
4. Institutional activity (FII/DII flows, ownership trends)
5. Insider trading (promoter activity, pledged shares)
6. Derivatives (short interest, put/call ratios, OI buildup)

SCORING:
- News (0-20)
- Social (0-20)
- Analysts (0-20)
- Institutional (0-20)
- Insider/Derivatives (0-20)

OUTPUT FORMAT:
## Sentiment Analysis: $TICKER
### Sentiment Score: [X]/100
[News: X/20 | Social: X/20 | Analysts: X/20 | Institutional: X/20 | Insider: X/20]
### Signal: [Bullish/Neutral/Bearish]

[Detailed analysis]

Save to: $OUTPUTS_DIR/agent3_sentiment.txt
EOF
            ;;
        "risk")
            cat > "$PROMPT_FILE" <<EOF
You are a Risk Assessment specialist. Analyze $TICKER.

DISCOVERY DATA:
$DISCOVERY_CONTENT

YOUR MANDATE:
1. Volatility profile (historical vol, beta, ATR)
2. Downside scenarios (bear case, max drawdown, stress tests)
3. Correlation & macro risks (interest rates, regulatory, sector)
4. Liquidity risk (volume, spreads, float)
5. Position sizing (conservative/moderate/aggressive recommendations)
6. Top 10 risk factors with probability × impact matrix

SCORING (HIGHER = LOWER RISK):
- Volatility (0-20)
- Downside Protection (0-20)
- Macro Resilience (0-20)
- Liquidity (0-20)
- Risk/Reward (0-20)

OUTPUT FORMAT:
## Risk Assessment: $TICKER
### Risk Score: [X]/100 (higher = lower risk)
[Volatility: X/20 | Downside: X/20 | Macro: X/20 | Liquidity: X/20 | R/R: X/20]
### Risk Level: [Low/Moderate/High/Extreme]

[Detailed analysis]

Save to: $OUTPUTS_DIR/agent4_risk.txt
EOF
            ;;
        "thesis")
            cat > "$PROMPT_FILE" <<EOF
You are an Investment Thesis specialist. Build complete thesis for $TICKER.

DISCOVERY DATA:
$DISCOVERY_CONTENT

YOUR MANDATE:
1. Core thesis (2-3 sentences: why this stock, why now)
2. Bull case (5-7 catalysts, target, probability)
3. Bear case (5-7 risks, target, probability)
4. Catalyst calendar (upcoming events with dates)
5. Entry/exit strategy (zones, stops, targets, sizing, timeframe)
6. Conviction assessment (what gives/reduces conviction, invalidation triggers)

SCORING:
- Catalyst Clarity (0-20)
- Timing (0-20)
- Asymmetry (0-20)
- Edge (0-20)
- Conviction (0-20)

OUTPUT FORMAT:
## Investment Thesis: $TICKER
### Thesis Score: [X]/100
[Catalyst: X/20 | Timing: X/20 | Asymmetry: X/20 | Edge: X/20 | Conviction: X/20]
### Thesis: [Strong/Moderate/Weak]

[Detailed analysis with all 6 sections]

Save to: $OUTPUTS_DIR/agent5_thesis.txt
EOF
            ;;
    esac
}

# Launch all agents (in reality, these would run in parallel)
# For demonstration, we'll launch them sequentially
launch_agent "technical" 1 &
PID1=$!

launch_agent "fundamental" 2 &
PID2=$!

launch_agent "sentiment" 3 &
PID3=$!

launch_agent "risk" 4 &
PID4=$!

launch_agent "thesis" 5 &
PID5=$!

# Wait for all background jobs
echo -e "\n${YELLOW}Waiting for all agents to complete...${NC}\n"
wait $PID1 $PID2 $PID3 $PID4 $PID5

echo -e "\n${GREEN}✓ All agents completed${NC}\n"

# ============================================================================
# PHASE 3: SYNTHESIS
# ============================================================================
echo -e "${YELLOW}PHASE 3: SYNTHESIZING COMPREHENSIVE REPORT${NC}\n"

REPORT_FILE="$BASE_DIR/TRADE-ANALYSIS-${TICKER}.md"

# For now, create a template report
# In production, you would parse the agent outputs and calculate scores
cat > "$REPORT_FILE" <<EOF
# Trade Analysis: $TICKER
> Generated by AI Trading Analyst | $DATE

---

## Executive Summary

[This section synthesizes findings from all 5 agents]

Current Status: Analysis completed with 5-agent framework
- Technical Analysis: See agent_outputs/agent1_technical.txt
- Fundamental Analysis: See agent_outputs/agent2_fundamental.txt
- Sentiment Analysis: See agent_outputs/agent3_sentiment.txt
- Risk Assessment: See agent_outputs/agent4_risk.txt
- Investment Thesis: See agent_outputs/agent5_thesis.txt

---

## Trade Score Dashboard

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Technical Strength | [Pending]/100 | 25% | - |
| Fundamental Quality | [Pending]/100 | 25% | - |
| Sentiment & Momentum | [Pending]/100 | 20% | - |
| Risk Profile | [Pending]/100 | 15% | - |
| Thesis Conviction | [Pending]/100 | 15% | - |
| **Composite Trade Score** | | | **[Pending]/100** |

**Grade: [Pending]** | **Signal: [Pending]**

---

## Agent Outputs

### Technical Analysis
\`\`\`
$(cat "$OUTPUTS_DIR/agent1_technical.txt" 2>/dev/null || echo "Output pending")
\`\`\`

### Fundamental Analysis
\`\`\`
$(cat "$OUTPUTS_DIR/agent2_fundamental.txt" 2>/dev/null || echo "Output pending")
\`\`\`

### Sentiment Analysis
\`\`\`
$(cat "$OUTPUTS_DIR/agent3_sentiment.txt" 2>/dev/null || echo "Output pending")
\`\`\`

### Risk Assessment
\`\`\`
$(cat "$OUTPUTS_DIR/agent4_risk.txt" 2>/dev/null || echo "Output pending")
\`\`\`

### Investment Thesis
\`\`\`
$(cat "$OUTPUTS_DIR/agent5_thesis.txt" 2>/dev/null || echo "Output pending")
\`\`\`

---

## Next Steps

To actually execute the analysis:

1. Run each agent manually:
   \`\`\`bash
   claude agentic --model sonnet < agent_outputs/agent1_technical_prompt.txt > agent_outputs/agent1_technical.txt
   claude agentic --model sonnet < agent_outputs/agent2_fundamental_prompt.txt > agent_outputs/agent2_fundamental.txt
   # ... repeat for agents 3, 4, 5
   \`\`\`

2. Or use the Python orchestrator:
   \`\`\`bash
   python stock_analyzer.py $TICKER --market $MARKET
   \`\`\`

3. Then re-run this script to generate the synthesized report

---

**Disclaimer:** This is for educational purposes only. Not financial advice.
Always conduct your own due diligence and consult qualified advisors.
EOF

echo -e "${GREEN}✓${NC} Report template created: $REPORT_FILE\n"

# ============================================================================
# SUMMARY
# ============================================================================
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ANALYSIS FRAMEWORK COMPLETE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"

echo -e "Generated Files:"
echo -e "  ${GREEN}✓${NC} Discovery Brief: $DISCOVERY_FILE"
echo -e "  ${GREEN}✓${NC} Agent Prompts: $OUTPUTS_DIR/agent*_prompt.txt"
echo -e "  ${GREEN}✓${NC} Agent Outputs: $OUTPUTS_DIR/agent*.txt"
echo -e "  ${GREEN}✓${NC} Final Report: $REPORT_FILE"

echo -e "\n${YELLOW}NOTE:${NC} This script creates the framework and prompts."
echo -e "To actually run the analysis, either:"
echo -e "  1. Execute each agent prompt manually with: ${BLUE}claude agentic${NC}"
echo -e "  2. Use the Python orchestrator: ${BLUE}python stock_analyzer.py $TICKER${NC}"
echo -e "  3. Use claude-code skill: ${BLUE}/trade-analyze $TICKER${NC}\n"
