#!/usr/bin/env python3
"""
Comprehensive Stock Analysis Script
Replicates the /trade-analyze skill functionality without using the skill itself.

Usage:
    python stock_analyzer.py TICKER [--market NSE|NYSE]

Example:
    python stock_analyzer.py MUTHOOTFIN --market NSE
    python stock_analyzer.py AAPL --market NYSE
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import concurrent.futures


class StockAnalyzer:
    """Main orchestrator for comprehensive stock analysis."""

    def __init__(self, ticker: str, market: str = "NSE"):
        self.ticker = ticker
        self.market = market
        self.base_dir = Path.cwd()
        self.outputs_dir = self.base_dir / "agent_outputs"
        self.outputs_dir.mkdir(exist_ok=True)

        # Analysis weights for composite score
        self.weights = {
            "technical": 0.25,
            "fundamental": 0.25,
            "sentiment": 0.20,
            "risk": 0.15,
            "thesis": 0.15
        }

    def run_discovery(self) -> str:
        """Phase 1: Gather foundational data about the stock."""
        print(f"\n{'='*70}")
        print(f"PHASE 1: DISCOVERY - Gathering data for {self.ticker}")
        print(f"{'='*70}\n")

        discovery_brief = f"""═══════════════════════════════════════════════════════════════
DISCOVERY BRIEF: {self.ticker}
Analysis Date: {datetime.now().strftime('%B %d, %Y')}
Market: {self.market}
═══════════════════════════════════════════════════════════════

This discovery brief will be populated with:
- Current market data (price, volume, market cap)
- Company overview (business description, products, leadership)
- Recent financial performance (revenue, profit, margins)
- Key financial metrics (P/E, ROE, debt ratios)
- Recent news and catalysts
- Competitive position and sector context

Status: Ready for agent analysis
═══════════════════════════════════════════════════════════════
"""

        # Save discovery brief
        discovery_path = self.base_dir / f"discovery_brief_{self.ticker}.txt"
        discovery_path.write_text(discovery_brief)

        print(f"✓ Discovery brief created: {discovery_path}")
        print(f"  Note: Agents will perform their own web research for detailed data\n")

        return str(discovery_path)

    def launch_agent(self, agent_name: str, agent_type: str, description: str,
                     prompt_file: str, output_file: str) -> Dict:
        """Launch a single analysis agent using claude CLI."""
        print(f"🚀 Launching {agent_name}...")

        # Read the prompt template
        prompt = Path(prompt_file).read_text()

        # Prepare claude command
        cmd = [
            "claude",
            "agentic",
            "--model", "sonnet",
            "--max-turns", "30",
            prompt
        ]

        try:
            # Run the agent
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=900  # 15 minute timeout
            )

            # Save output
            Path(output_file).write_text(result.stdout)

            # Extract score from output (looking for patterns like "Score: X/100")
            score = self._extract_score(result.stdout)

            return {
                "name": agent_name,
                "status": "completed" if result.returncode == 0 else "failed",
                "score": score,
                "output_file": output_file,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except subprocess.TimeoutExpired:
            return {
                "name": agent_name,
                "status": "timeout",
                "score": None,
                "output_file": output_file
            }
        except Exception as e:
            return {
                "name": agent_name,
                "status": "error",
                "score": None,
                "error": str(e),
                "output_file": output_file
            }

    def _extract_score(self, output: str) -> Optional[int]:
        """Extract score from agent output."""
        import re

        # Look for patterns like "Score: 85/100" or "### Score: 85/100"
        patterns = [
            r'(?:Technical|Fundamental|Sentiment|Risk|Thesis)\s+Score:\s*(\d+)/100',
            r'Score:\s*(\d+)/100',
            r'##\s+\w+\s+Score:\s*(\d+)/100'
        ]

        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return None

    def launch_parallel_agents(self, discovery_path: str) -> Dict[str, Dict]:
        """Phase 2: Launch all 5 agents in parallel."""
        print(f"\n{'='*70}")
        print(f"PHASE 2: PARALLEL AGENT DEPLOYMENT")
        print(f"{'='*70}\n")

        # Define agent configurations
        agents_config = {
            "technical": {
                "description": "Technical Analysis for {ticker}",
                "prompt_file": self.base_dir / "prompts" / "agent1_technical_prompt.txt",
                "output_file": self.outputs_dir / "agent1_technical.txt"
            },
            "fundamental": {
                "description": "Fundamental Analysis for {ticker}",
                "prompt_file": self.base_dir / "prompts" / "agent2_fundamental_prompt.txt",
                "output_file": self.outputs_dir / "agent2_fundamental.txt"
            },
            "sentiment": {
                "description": "Sentiment Analysis for {ticker}",
                "prompt_file": self.base_dir / "prompts" / "agent3_sentiment_prompt.txt",
                "output_file": self.outputs_dir / "agent3_sentiment.txt"
            },
            "risk": {
                "description": "Risk Assessment for {ticker}",
                "prompt_file": self.base_dir / "prompts" / "agent4_risk_prompt.txt",
                "output_file": self.outputs_dir / "agent4_risk.txt"
            },
            "thesis": {
                "description": "Investment Thesis for {ticker}",
                "prompt_file": self.base_dir / "prompts" / "agent5_thesis_prompt.txt",
                "output_file": self.outputs_dir / "agent5_thesis.txt"
            }
        }

        # Create prompt templates if they don't exist
        self._create_prompt_templates(agents_config, discovery_path)

        # Launch agents in parallel using ThreadPoolExecutor
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_agent = {
                executor.submit(
                    self.launch_agent,
                    agent_name,
                    agent_name,
                    config["description"].format(ticker=self.ticker),
                    str(config["prompt_file"]),
                    str(config["output_file"])
                ): agent_name
                for agent_name, config in agents_config.items()
            }

            for future in concurrent.futures.as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    result = future.result()
                    results[agent_name] = result

                    status_symbol = "✓" if result["status"] == "completed" else "✗"
                    score_text = f"Score: {result['score']}/100" if result['score'] else "No score"
                    print(f"{status_symbol} {result['name'].capitalize()}: {result['status']} - {score_text}")

                except Exception as e:
                    results[agent_name] = {
                        "name": agent_name,
                        "status": "error",
                        "error": str(e)
                    }
                    print(f"✗ {agent_name.capitalize()}: Failed - {str(e)}")

        return results

    def _create_prompt_templates(self, agents_config: Dict, discovery_path: str):
        """Create prompt template files for each agent."""
        prompts_dir = self.base_dir / "prompts"
        prompts_dir.mkdir(exist_ok=True)

        # Read discovery brief
        discovery_content = Path(discovery_path).read_text()

        # Template for each agent type
        templates = {
            "technical": self._get_technical_prompt_template(),
            "fundamental": self._get_fundamental_prompt_template(),
            "sentiment": self._get_sentiment_prompt_template(),
            "risk": self._get_risk_prompt_template(),
            "thesis": self._get_thesis_prompt_template()
        }

        for agent_name, config in agents_config.items():
            prompt_file = config["prompt_file"]
            if not prompt_file.exists():
                template = templates[agent_name]
                prompt = template.format(
                    ticker=self.ticker,
                    discovery_brief=discovery_content,
                    output_file=str(config["output_file"])
                )
                prompt_file.write_text(prompt)
                print(f"  Created prompt: {prompt_file.name}")

    def synthesize_report(self, agent_results: Dict[str, Dict]) -> str:
        """Phase 3: Synthesize all agent outputs into final report."""
        print(f"\n{'='*70}")
        print(f"PHASE 3: SYNTHESIS - Generating comprehensive report")
        print(f"{'='*70}\n")

        # Calculate composite score
        composite_score = self._calculate_composite_score(agent_results)
        grade = self._get_grade(composite_score)
        signal = self._get_signal(composite_score)

        # Read all agent outputs
        agent_outputs = {}
        for agent_name, result in agent_results.items():
            if result["status"] == "completed":
                output_file = result["output_file"]
                if Path(output_file).exists():
                    agent_outputs[agent_name] = Path(output_file).read_text()

        # Generate comprehensive report
        report = self._generate_comprehensive_report(
            agent_outputs,
            composite_score,
            grade,
            signal
        )

        # Save report
        report_path = self.base_dir / f"TRADE-ANALYSIS-{self.ticker}.md"
        report_path.write_text(report)

        print(f"✓ Comprehensive report generated: {report_path}")
        print(f"\n{'='*70}")
        print(f"ANALYSIS COMPLETE")
        print(f"{'='*70}")
        print(f"\nComposite Trade Score: {composite_score}/100")
        print(f"Grade: {grade}")
        print(f"Signal: {signal}")
        print(f"\nReport saved to: {report_path}")

        return str(report_path)

    def _calculate_composite_score(self, results: Dict[str, Dict]) -> int:
        """Calculate weighted composite score."""
        total_score = 0
        total_weight = 0

        for agent_name, result in results.items():
            if result.get("score") is not None:
                weight = self.weights.get(agent_name, 0)
                total_score += result["score"] * weight
                total_weight += weight

        if total_weight > 0:
            return round(total_score / total_weight)
        return 0

    def _get_grade(self, score: int) -> str:
        """Convert score to letter grade."""
        if score >= 85: return "A+"
        elif score >= 70: return "A"
        elif score >= 55: return "B"
        elif score >= 40: return "C"
        elif score >= 25: return "D"
        else: return "F"

    def _get_signal(self, score: int) -> str:
        """Convert score to trading signal."""
        if score >= 85: return "Strong Buy"
        elif score >= 70: return "Buy"
        elif score >= 55: return "Hold/Accumulate"
        elif score >= 40: return "Neutral"
        elif score >= 25: return "Caution"
        else: return "Avoid"

    def _generate_comprehensive_report(self, agent_outputs: Dict,
                                      composite_score: int,
                                      grade: str,
                                      signal: str) -> str:
        """Generate the final markdown report."""

        report = f"""# Trade Analysis: {self.ticker}
> Generated by AI Trading Analyst | {datetime.now().strftime('%B %d, %Y')}

---

## Executive Summary

[This section would be auto-generated by synthesizing all agent findings]

---

## Trade Score Dashboard

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Technical Strength | {agent_outputs.get('technical', {}).get('score', 'N/A')}/100 | 25% | - |
| Fundamental Quality | {agent_outputs.get('fundamental', {}).get('score', 'N/A')}/100 | 25% | - |
| Sentiment & Momentum | {agent_outputs.get('sentiment', {}).get('score', 'N/A')}/100 | 20% | - |
| Risk Profile | {agent_outputs.get('risk', {}).get('score', 'N/A')}/100 | 15% | - |
| Thesis Conviction | {agent_outputs.get('thesis', {}).get('score', 'N/A')}/100 | 15% | - |
| **Composite Trade Score** | | | **{composite_score}/100** |

**Grade: {grade}** | **Signal: {signal}**

---

## Technical Analysis

{agent_outputs.get('technical', 'Technical analysis not available')}

---

## Fundamental Analysis

{agent_outputs.get('fundamental', 'Fundamental analysis not available')}

---

## Sentiment Analysis

{agent_outputs.get('sentiment', 'Sentiment analysis not available')}

---

## Risk Assessment

{agent_outputs.get('risk', 'Risk assessment not available')}

---

## Investment Thesis

{agent_outputs.get('thesis', 'Investment thesis not available')}

---

## Disclaimer

This analysis is for educational and research purposes only. Not financial advice.
Always conduct your own due diligence and consult qualified financial advisors.

---

**Report Generated:** {datetime.now().strftime('%B %d, %Y')}
**Ticker:** {self.ticker}
**Market:** {self.market}
**Composite Score:** {composite_score}/100
**Grade:** {grade}
**Signal:** {signal}
"""
        return report

    # Prompt templates for each agent
    def _get_technical_prompt_template(self) -> str:
        return """You are a Technical Analysis specialist. Analyze {ticker} comprehensively.

DISCOVERY DATA:
{discovery_brief}

YOUR MANDATE — Deliver a comprehensive technical analysis covering:

1. TREND ANALYSIS
   - Primary trend direction (bullish / bearish / sideways)
   - Moving average analysis (20/50/200 EMA)
   - Price position relative to key MAs
   - Higher highs / higher lows pattern

2. SUPPORT & RESISTANCE
   - Identify at least 3 support levels with reasoning
   - Identify at least 3 resistance levels with reasoning
   - Note highest confluence zones

3. MOMENTUM INDICATORS
   - RSI (14): current value, trend, overbought/oversold
   - MACD: signal line position, histogram, divergences
   - Stochastic: position and crossover status

4. VOLUME ANALYSIS
   - Current volume vs averages
   - Accumulation/distribution pattern
   - On-Balance Volume (OBV) trend
   - Volume divergences

5. CHART PATTERNS
   - Active patterns (flags, wedges, H&S, etc.)
   - Pattern completion and targets
   - Breakout/breakdown levels

6. ADDITIONAL FACTORS
   - Bollinger Band position and squeeze status
   - Moving average crossovers
   - Relative strength vs index
   - Fibonacci retracement levels

SCORING — Provide a Technical Score (0-100) broken into:
   - Trend Score (0-20)
   - Momentum Score (0-20)
   - Volume Score (0-20)
   - Pattern Quality (0-20)
   - Relative Strength (0-20)

OUTPUT FORMAT:
## Technical Analysis: {ticker}
### Technical Score: [X]/100
[Trend: X/20 | Momentum: X/20 | Volume: X/20 | Pattern: X/20 | Rel Strength: X/20]
### Signal: [Bullish / Neutral / Bearish]

[Full analysis with all 6 sections]

### Key Levels
- Entry Zone: $X - $X
- Stop Loss: $X (X% below entry)
- Target 1: $X (X% upside)
- Target 2: $X (X% upside)

Write your analysis to: {output_file}

Use WebSearch and WebFetch tools to gather current price data and technical indicators.
Be specific with numbers, prices, and percentages.
"""

    def _get_fundamental_prompt_template(self) -> str:
        return """You are a Fundamental Analysis specialist. Analyze {ticker} comprehensively.

DISCOVERY DATA:
{discovery_brief}

YOUR MANDATE — Deliver a comprehensive fundamental analysis covering:

1. VALUATION
   - P/E (trailing & forward) vs sector and 5-year average
   - P/S and P/B ratios vs sector
   - PEG ratio assessment
   - EV/EBITDA vs sector
   - Verdict: Undervalued / Fair Value / Overvalued

2. GROWTH
   - Revenue growth (QoQ, YoY, CAGR)
   - Earnings growth rates
   - Forward guidance and analyst estimates
   - TAM and penetration

3. PROFITABILITY
   - Margin analysis (gross, operating, net)
   - ROE and ROIC
   - Return trends

4. FINANCIAL HEALTH
   - Debt ratios and coverage
   - Cash flow analysis
   - Liquidity metrics

5. COMPETITIVE MOAT
   - Brand strength
   - Network effects
   - Switching costs
   - Cost advantages
   - Moat rating: Wide / Narrow / None

6. MANAGEMENT QUALITY
   - Insider ownership
   - Track record
   - Capital allocation
   - Alignment with shareholders

SCORING — Provide a Fundamental Score (0-100):
   - Valuation (0-20)
   - Growth (0-20)
   - Profitability (0-20)
   - Financial Health (0-20)
   - Moat Strength (0-20)

OUTPUT FORMAT:
## Fundamental Analysis: {ticker}
### Fundamental Score: [X]/100
[Valuation: X/20 | Growth: X/20 | Profitability: X/20 | Health: X/20 | Moat: X/20]
### Signal: [Strong / Adequate / Weak]

[Full analysis with all 6 sections]

Write to: {output_file}
"""

    def _get_sentiment_prompt_template(self) -> str:
        return """You are a Sentiment & Momentum specialist. Analyze {ticker} comprehensively.

DISCOVERY DATA:
{discovery_brief}

YOUR MANDATE — Deliver comprehensive sentiment analysis covering:

1. NEWS SENTIMENT
   - Recent headlines (last 30-60 days)
   - Positive/negative/neutral scoring
   - Major catalysts identified

2. SOCIAL MEDIA BUZZ
   - Reddit, Twitter/X mentions
   - Retail sentiment direction
   - Discussion volume and themes

3. ANALYST RATINGS
   - Consensus rating
   - Average price target vs current
   - Recent upgrades/downgrades

4. INSTITUTIONAL ACTIVITY
   - FII/DII activity
   - Ownership trends
   - Major fund positions

5. INSIDER TRADING
   - Recent buys/sells
   - Promoter activity
   - Pledged shares status

6. SHORT INTEREST & OPTIONS
   - Short interest as % float
   - Put/call ratios
   - Derivatives buildups

SCORING — Sentiment Score (0-100):
   - News (0-20)
   - Social (0-20)
   - Analysts (0-20)
   - Institutional (0-20)
   - Insider/Derivatives (0-20)

OUTPUT FORMAT:
## Sentiment Analysis: {ticker}
### Sentiment Score: [X]/100
[News: X/20 | Social: X/20 | Analysts: X/20 | Institutional: X/20 | Insider: X/20]
### Signal: [Bullish / Neutral / Bearish]

[Full analysis]

Write to: {output_file}
"""

    def _get_risk_prompt_template(self) -> str:
        return """You are a Risk Assessment specialist. Analyze {ticker} comprehensively.

DISCOVERY DATA:
{discovery_brief}

YOUR MANDATE — Deliver comprehensive risk assessment covering:

1. VOLATILITY PROFILE
   - Historical volatility (30/90/365 day)
   - Beta vs benchmark
   - ATR and typical ranges

2. DOWNSIDE SCENARIOS
   - Bear case price target
   - Maximum drawdown scenarios
   - Key risk events

3. CORRELATION & MACRO RISK
   - Market correlation
   - Interest rate sensitivity
   - Regulatory risks

4. LIQUIDITY RISK
   - Daily volume
   - Bid-ask spreads
   - Float analysis

5. POSITION SIZING
   - Conservative/Moderate/Aggressive sizing
   - Stop-loss recommendations
   - Risk/reward ratios

6. RISK FACTORS SUMMARY
   - Top 10 risks ranked
   - Risk matrix
   - Mitigating factors

SCORING — Risk Score (0-100, HIGHER = LOWER RISK):
   - Volatility (0-20)
   - Downside Protection (0-20)
   - Macro Resilience (0-20)
   - Liquidity (0-20)
   - Risk/Reward (0-20)

OUTPUT FORMAT:
## Risk Assessment: {ticker}
### Risk Score: [X]/100 (higher = lower risk)
[Volatility: X/20 | Downside: X/20 | Macro: X/20 | Liquidity: X/20 | R/R: X/20]
### Risk Level: [Low / Moderate / High / Extreme]

[Full analysis]

Write to: {output_file}
"""

    def _get_thesis_prompt_template(self) -> str:
        return """You are an Investment Thesis specialist. Build a complete thesis for {ticker}.

DISCOVERY DATA:
{discovery_brief}

YOUR MANDATE — Build comprehensive investment thesis covering:

1. CORE THESIS (2-3 sentences)
   - Why this stock, why now, what is the edge

2. BULL CASE
   - 5-7 specific catalysts
   - Bull target with timeline
   - What needs to go right
   - Probability assessment

3. BEAR CASE
   - 5-7 specific risks
   - Bear target with timeline
   - What needs to go wrong
   - Probability assessment

4. CATALYST CALENDAR
   - Upcoming events with dates
   - Expected impact (bullish/bearish/neutral)

5. ENTRY/EXIT STRATEGY
   - Entry zone with reasoning
   - Stop-loss with reasoning
   - Targets (conservative & aggressive)
   - Position sizing
   - Timeframe recommendation

6. CONVICTION ASSESSMENT
   - What gives conviction
   - What reduces conviction
   - Invalidation triggers
   - Opportunity cost comparison

SCORING — Thesis Score (0-100):
   - Catalyst Clarity (0-20)
   - Timing (0-20)
   - Asymmetry (0-20)
   - Edge (0-20)
   - Conviction (0-20)

OUTPUT FORMAT:
## Investment Thesis: {ticker}
### Thesis Score: [X]/100
[Catalyst: X/20 | Timing: X/20 | Asymmetry: X/20 | Edge: X/20 | Conviction: X/20]
### Thesis: [Strong / Moderate / Weak]

[Full analysis]

Write to: {output_file}
"""

    def run_full_analysis(self):
        """Execute the complete 3-phase analysis."""
        print(f"\n{'#'*70}")
        print(f"#  COMPREHENSIVE STOCK ANALYSIS: {self.ticker}")
        print(f"#  Market: {self.market}")
        print(f"#  Date: {datetime.now().strftime('%B %d, %Y')}")
        print(f"{'#'*70}\n")

        # Phase 1: Discovery
        discovery_path = self.run_discovery()

        # Phase 2: Parallel agent deployment
        agent_results = self.launch_parallel_agents(discovery_path)

        # Phase 3: Synthesis
        report_path = self.synthesize_report(agent_results)

        return report_path


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Comprehensive Stock Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python stock_analyzer.py MUTHOOTFIN --market NSE
    python stock_analyzer.py AAPL --market NYSE
    python stock_analyzer.py RELIANCE.NS --market NSE
        """
    )

    parser.add_argument('ticker', help='Stock ticker symbol')
    parser.add_argument('--market', default='NSE', choices=['NSE', 'NYSE', 'NASDAQ'],
                       help='Market exchange (default: NSE)')

    args = parser.parse_args()

    # Run analysis
    analyzer = StockAnalyzer(args.ticker, args.market)
    report_path = analyzer.run_full_analysis()

    print(f"\n✅ Analysis complete! Report: {report_path}\n")


if __name__ == "__main__":
    main()
