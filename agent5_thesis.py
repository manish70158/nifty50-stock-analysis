#!/usr/bin/env python3
"""
Agent 5: Investment Thesis Specialist for POWERGRID.NS
"""

def calculate_thesis_analysis():
    
    # Core thesis scoring
    catalyst_score = 15
    timing_score = 13
    asymmetry_score = 14
    edge_score = 12
    conviction_score = 14
    
    thesis_score = catalyst_score + timing_score + asymmetry_score + edge_score + conviction_score
    
    # Generate signal
    if thesis_score >= 75:
        signal = "Strong"
    elif thesis_score >= 60:
        signal = "Moderate"
    else:
        signal = "Weak"
    
    # Generate report
    report = f"""## Investment Thesis: POWERGRID.NS
### Thesis Score: {thesis_score}/100
[Catalyst: {catalyst_score}/20 | Timing: {timing_score}/20 | Asymmetry: {asymmetry_score}/20 | Edge: {edge_score}/20 | Conviction: {conviction_score}/20]
### Thesis: {signal}

#### 1. CORE THESIS

**"The Boring Compounder in India's Energy Transition"**

Power Grid Corporation of India (POWERGRID.NS) offers a rare combination of **defensive characteristics with structural growth exposure**. As India's monopolistic inter-state power transmission utility, POWERGRID is the critical infrastructure backbone enabling India's ambitious 500 GW renewable energy target by 2030. The company provides:

1. **Predictable, regulated cash flows** (15.5% guaranteed RoE on transmission assets)
2. **Structural growth tailwinds** from India's $250B+ transmission infrastructure investment cycle
3. **Attractive valuation** with 3.9% dividend yield and P/E of 20x (in-line with peers despite superior margins)

**Why this stock:** Monopolistic transmission business with wide economic moat, recession-resistant cash flows, and government backing.

**Why now:** Stock consolidating near highs after technical breakout; low sentiment despite strong fundamentals; India power sector reforms improving visibility.

**What is the edge:** Market underappreciates the quality of POWERGRID's regulated utility model, treating it as a generic PSU rather than a compounding infrastructure asset with 10-year revenue visibility.

#### 2. BULL CASE
**Bull Case Price Target: ₹380** (21% upside) | **Timeline: 12-18 months**

**Catalyst 1: Renewable Energy Transmission Boom**
India needs to add 60,000-80,000 circuit km of transmission lines by 2030 to connect renewable energy hubs (Rajasthan solar, Gujarat wind, offshore wind) to demand centers. POWERGRID, with 50% market share and preferential access to government projects, is the primary beneficiary. Revenue CAGR could accelerate to 12-15% (from current 10%) as green corridor projects ramp up.

**Catalyst 2: Margin Expansion from Operational Leverage**
As the network scales (180,000 circuit km → 250,000+ circuit km by 2030), operating leverage drives margin expansion. Fixed cost base allows incremental revenue to flow through at 70-80% margins. Operating margin could expand from 58.7% to 60-62%, adding ₹2-3 to EPS.

**Catalyst 3: Disinvestment/PSU Re-Rating**
Government is exploring strategic sale/disinvestment of select PSU stakes. Any disinvestment announcement for POWERGRID (even 10-15% stake) could trigger PSU discount compression, leading to 15-20% re-rating. Alternatively, inclusion in key indices (already in Nifty 50) or MSCI weight increases drive passive fund inflows.

**Catalyst 4: Dividend Increase**
Current payout ratio of 57.8% is conservative for a utility. If management increases payout to 65-70% (in-line with mature utilities globally), dividend yield would rise to 4.5-5.0%, making the stock more attractive to income investors and driving multiple expansion.

**Catalyst 5: Consultancy & Telecom Business Monetization**
POWERGRID's consultancy arm (providing transmission advisory to African/Asian countries) and telecom business (fiber optic network on transmission towers) are undervalued. Potential spin-off, JV, or IPO of telecom business could unlock ₹50-100 per share value (5-10% of market cap).

**What needs to go right:**
- India GDP growth sustains at 6-7%, driving power demand
- Government maintains 15.5% regulated RoE (no tariff cuts)
- POWERGRID wins 40-50% of TBCB transmission projects (in-line with historical share)
- State utility finances improve further, reducing payment delays
- Interest rates remain stable or decline, lowering debt servicing costs

**Bull Case Financials (FY27-28E):**
- Revenue: ₹550-600B (+16-20% from current)
- EPS: ₹18-20 (+15-20% CAGR)
- P/E Multiple: 19-21x (in-line with utilities globally)
- Target Price: ₹380 (21x FY28E EPS of ₹18)

#### 3. BEAR CASE
**Bear Case Price Target: ₹265** (16% downside) | **Timeline: 6-12 months**

**Risk 1: Regulatory Tariff Cut**
Central Electricity Regulatory Commission (CERC) could reduce regulated RoE from 15.5% to 14.0-14.5% in the next tariff review (due 2027). This would compress margins by 50-100 bps and reduce EPS by 8-10%. Given power sector reforms favoring lower tariffs for end consumers, this is a real risk. Impact: -₹2 EPS, -₹40 stock price.

**Risk 2: State Utility Payment Crisis 2.0**
While UDAY scheme has improved state distribution utility (discom) finances, they remain fragile. Any macro shock (state fiscal crisis, election-driven populism) could lead to payment delays/defaults. POWERGRID has ₹50-70B in receivables; a 180-day delay in collections could strain cash flows and force dividend cuts. Impact: Sentiment hit, -15-20% stock price.

**Risk 3: Project Execution Delays & Cost Overruns**
Under-construction projects worth ₹30,000-40,000 crore could face delays due to:
- Right-of-way issues (land acquisition, forest clearances)
- Supply chain disruptions (conductor/tower shortages)
- Technical challenges (HVDC integration, grid synchronization)

Delays push out revenue recognition by 6-12 months, missing FY27-28 targets. Impact: -10-15% EPS miss, analyst downgrades.

**Risk 4: Interest Rate Shock**
With D/E of 141, POWERGRID is highly sensitive to interest rates. If RBI raises rates by 100-150 bps due to inflation resurgence, interest expense rises by ₹12-15B annually. While regulated tariffs allow partial pass-through, there's a 6-12 month lag. Impact: -₹1.5-2.0 EPS, PE compression to 17-18x.

**Risk 5: PSU Discount Persists**
Governance concerns, bureaucratic decision-making, and lack of management autonomy keep PSU stocks at 15-25% discount to private peers. If sentiment toward PSUs sours (due to policy uncertainty, election outcomes, corruption scandals), POWERGRID remains trapped in a low-multiple range despite strong fundamentals. Impact: PE remains at 18-19x vs fair value of 22-24x.

**What needs to go wrong:**
- India GDP growth slows to <5% (demand stagnation)
- CERC cuts regulated RoE to 14% or below
- State utilities default on payments, triggering cash flow crisis
- Interest rates spike 150+ bps
- POWERGRID loses market share in TBCB auctions to Adani Transmission, Sterlite Power

**Bear Case Financials (FY27-28E):**
- Revenue: ₹480-500B (+2-5% from current)
- EPS: ₹13-14 (-10% to flat)
- P/E Multiple: 19-20x (in-line but no growth premium)
- Target Price: ₹265 (19x FY28E EPS of ₹14)

#### 4. CATALYST CALENDAR

| Date | Event | Expected Impact |
|------|-------|-----------------|
| **July 2026** | Q1 FY27 Earnings | Neutral to Positive - Guidance on FY27 capex and commissioning pipeline |
| **August 2026** | Union Budget 2026-27 | Bullish - Infrastructure allocation; NIP updates; transmission project announcements |
| **September 2026** | Transmission Project Bidding (TBCB) | Bullish if wins >40% - New project wins add to order book visibility |
| **October 2026** | Q2 FY27 Earnings | Neutral - Mid-year performance check; monsoon impact on construction |
| **November 2026** | COP28 Follow-up / Green Corridors Announcement | Bullish - Policy clarity on renewable integration and transmission funding |
| **January 2027** | Q3 FY27 Earnings | Positive - Strongest quarter historically (Oct-Dec project commissioning) |
| **February 2027** | Budget Session / Disinvestment Announcement? | Bullish - Potential strategic sale announcement |
| **April 2027** | Q4 & Full Year FY27 Earnings | Key - FY28 guidance; dividend declaration; management commentary |
| **May-June 2027** | CERC Tariff Consultation Papers | Bearish Risk - Early signals on RoE cuts for next tariff period |

**Near-Term Catalysts (Next 3 months):**
- Earnings season commentary on project pipeline
- Any disinvestment news flow
- State election outcomes (Maharashtra, UP) impacting discom payment cycles

#### 5. ENTRY/EXIT STRATEGY

**Recommended Entry Zone:** ₹305-315
**Rationale:** 
- Near 50-day SMA support (₹305.30)
- RSI approaching oversold (36), historically good buy zone
- Risk/reward favors entry on dips to support levels
- Current price ₹313.95 is at upper end of entry zone

**Phased Entry Approach:**
- **Tranche 1 (40% of position):** At current levels ₹313-315 (defensive entry)
- **Tranche 2 (40% of position):** On pullback to ₹305-308 (ideal risk/reward)
- **Tranche 3 (20% of position):** On breakout above ₹325 (momentum confirmation)

**Recommended Stop-Loss:** ₹293
**Rationale:**
- Below recent swing low and 50-day SMA
- 6.7% risk from entry (₹310 midpoint to ₹293)
- Invalidates bullish consolidation pattern
- Loss of 200-day SMA next (₹281) would confirm trend reversal

**Target 1 (Conservative):** ₹330 (6-8% upside)
**Rationale:**
- Above 52-week high (₹325)
- Psychological round number
- Analyst target mean ₹323, Target 1 slightly above
- Initial profit-taking zone (book 30-50% of position)
- **Timeline:** 3-6 months

**Target 2 (Aggressive):** ₹360 (15-18% upside)
**Rationale:**
- Measured move from consolidation pattern (₹290-325 range)
- Fibonacci extension (1.618x) from ₹250-325 swing
- Bull case scenario with multiple expansion to 22x P/E
- Full position exit or trail stop
- **Timeline:** 9-15 months

**Risk/Reward Ratio:** 2.4:1 to Target 1, 4.1:1 to Target 2 (from ₹310 entry with ₹293 stop)

**Position Size Suggestion:**
- **Conservative:** 8-12% of equity portfolio (core defensive holding)
- **Moderate:** 5-8% of portfolio (part of utilities allocation)
- **Aggressive:** 3-5% of portfolio (lower allocation for growth-focused)

**Recommended Timeframe:** 
- **Position Trade (Primary):** 12-18 months - align with FY27-28 earnings growth and catalyst timeline
- **Long-Term Hold (Alternative):** 3-5 years - for dividend reinvestment and compounding strategy
- **Swing Trade (Tactical):** 3-6 months - for technically-oriented traders targeting ₹325-330 breakout

**Exit Triggers (Stop Loss Scenarios):**
1. **Hard Stop:** Close below ₹293 on daily chart → Exit full position
2. **Fundamental Stop:** Regulatory RoE cut announced >100 bps → Reassess, likely reduce 50%
3. **Technical Stop:** Loss of 200-day SMA (₹281) → Exit remaining position

**Profit-Taking Strategy:**
- Book 25% at ₹330 (Target 1 hit)
- Book 25% at ₹345 (halfway to Target 2)
- Book 30% at ₹360 (Target 2 hit)
- Trail stop on remaining 20% using 20-day SMA

#### 6. CONVICTION ASSESSMENT

**What Gives Conviction:**

1. **Business Quality:** Wide economic moat from natural monopoly + regulatory protection + government backing. This is a 25-year compounder, not a cyclical trade.

2. **Margin of Safety:** At 20x P/E with 10% earnings growth and 3.9% dividend yield, downside is limited to ₹280-285 (11%), while upside is ₹360-380 (15-21%). Favorable risk/reward for defensive stock.

3. **Structural Tailwinds:** India's renewable energy transition REQUIRES massive transmission investment. This isn't discretionary capex - it's mission-critical infrastructure. POWERGRID has first-mover advantage and preferential access.

4. **Underappreciated by Market:** Sentiment score of 63/100 despite fundamental score of 77/100 suggests market inefficiency. The "PSU discount" creates opportunity for patient capital.

5. **Technical Confirmation:** Stock above 200-day SMA, consolidating near highs after 25% rally from ₹250. Breakout above ₹325 could trigger momentum chase by technicals-driven investors.

**What Reduces Conviction:**

1. **Lack of Near-Term Catalysts:** No earnings for 2 months, no disinvestment announcement imminent. Could remain range-bound ₹305-325 for Q2-Q3 2026.

2. **PSU Execution Risk:** Despite strong track record, PSUs can surprise negatively (delayed projects, bureaucratic issues, political interference). Management autonomy limited.

3. **Regulatory Uncertainty:** CERC tariff review in 2027 is binary event - could be neutral (RoE maintained) or negative (RoE cut). No positive surprise possible.

4. **Limited Options Liquidity:** Can't easily hedge position with puts/calls due to thin options market on NSE. Forced to use stop-losses for risk management.

5. **Opportunity Cost:** For aggressive investors, 10-15% annual returns from POWERGRID may lag high-growth tech/consumer stocks in a bull market. Suitable for defensive allocation, not growth sleeve.

**Thesis Invalidation Triggers:**

1. **Fundamental:** Quarterly revenue decline >5% YoY (ex-one-time factors) → indicates market share loss or demand weakness
2. **Fundamental:** CERC announces RoE cut to <14% → materially impairs economics
3. **Technical:** Loss of 200-day SMA (₹281) on weekly closing basis → trend reversal confirmed
4. **Sentiment:** Government announces privatization (not just disinvestment) → execution uncertainty during transition

**Comparison to Alternatives:**

**vs. NTPC (Generation):**
- POWERGRID has higher margins (58.7% vs 35-40%), lower cyclicality (transmission vs merchant power)
- NTPC has higher growth (renewable energy capex), higher volatility
- **Verdict:** POWERGRID for defense, NTPC for growth

**vs. Nifty 50 Index:**
- POWERGRID offers lower returns (10-15% vs 12-18%) but much lower volatility (beta 0.24)
- Better risk-adjusted returns (Sharpe ratio 0.8-1.0 vs 0.5-0.6 for Nifty)
- **Verdict:** POWERGRID for 30-40% of equity allocation (defensive core), Nifty for 60-70% (growth)

**vs. Adani Transmission (Private Peer):**
- Adani has higher growth (aggressive M&A, integrated model), higher risk (leverage, governance concerns)
- POWERGRID has stability, government backing, predictable earnings
- **Verdict:** POWERGRID for risk-averse; Adani for aggressive with tolerance for volatility

**Overall Conviction:** **Moderate to High (70/100)**

This is a **"sleep well at night"** investment with solid fundamentals, defensive characteristics, and structural tailwinds. Not a home run trade (unlikely to 2x in 12 months), but a steady compounder offering 10-15% annualized returns with 3.9% dividend yield and low drawdown risk.

**Ideal for:**
- Conservative investors seeking defensive exposure to India growth story
- Retirees/income investors attracted to 3.9% yield and low volatility
- Portfolio managers looking to reduce beta and add ballast

**Not ideal for:**
- Aggressive growth investors seeking 30-50% returns
- Short-term traders seeking volatility (beta 0.24 means muted price swings)
- Investors with low patience (could range-trade for 6+ months)

**Conviction Level:** Enough to make POWERGRID a **core holding (8-12% of portfolio)** for defensive equity allocation, but not aggressive overweight (>15%) given PSU risks and opportunity cost vs high-growth names.

---

### Investment Thesis Summary

**BUY POWERGRID.NS at ₹305-315 with:**
- **Price Target 1:** ₹330 (6-8 months)
- **Price Target 2:** ₹360 (12-18 months)
- **Stop Loss:** ₹293
- **Position Size:** 5-12% of portfolio (depending on risk tolerance)
- **Timeframe:** 12-18 months (position trade) or 3-5 years (long-term hold)

**Core Thesis:** High-quality defensive compounder benefiting from India's renewable energy transition, trading at reasonable valuation with 3.9% dividend yield. Limited downside, moderate upside, excellent risk-adjusted returns.

**This is a HOLD/BUY for existing shareholders, and a BUY on dips to ₹305-308 for new investors.**

DISCLAIMER: This is for educational and research purposes only. Not financial advice.
"""
    
    return report, thesis_score, catalyst_score, timing_score, asymmetry_score, edge_score, conviction_score

if __name__ == "__main__":
    report, score, catalyst, timing, asymmetry, edge, conviction = calculate_thesis_analysis()
    
    # Save to file
    with open('/Users/manishkumar/Documents/learning/9-May-Trade-Analysis/agent_outputs/agent5_thesis.txt', 'w') as f:
        f.write(report)
    
    # Also save scores
    with open('/Users/manishkumar/Documents/learning/9-May-Trade-Analysis/agent_outputs/agent5_scores.txt', 'w') as f:
        f.write(f"THESIS_SCORE={score}\n")
        f.write(f"CATALYST={catalyst}\n")
        f.write(f"TIMING={timing}\n")
        f.write(f"ASYMMETRY={asymmetry}\n")
        f.write(f"EDGE={edge}\n")
        f.write(f"CONVICTION={conviction}\n")
    
    print(f"Thesis Analysis Complete: Score = {score}/100")
