#!/usr/bin/env python3
"""
Nifty 50 Comprehensive Stock Analyzer
Analyzes all 50 stocks in the Nifty 50 index and generates a consolidated CSV report.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class Nifty50Analyzer:
    def __init__(self, tickers_file):
        self.tickers = self.load_tickers(tickers_file)
        self.results = []

    def load_tickers(self, file_path):
        """Load Nifty 50 tickers from file"""
        tickers = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and line.endswith('.NS'):
                    tickers.append(line)
        return tickers

    def calculate_rsi(self, data, period=14):
        """Calculate RSI indicator"""
        try:
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1] if len(rsi) > 0 else 50
        except:
            return 50

    def calculate_macd(self, data):
        """Calculate MACD indicator"""
        try:
            exp1 = data['Close'].ewm(span=12, adjust=False).mean()
            exp2 = data['Close'].ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            histogram = macd - signal
            return {
                'macd': macd.iloc[-1] if len(macd) > 0 else 0,
                'signal': signal.iloc[-1] if len(signal) > 0 else 0,
                'histogram': histogram.iloc[-1] if len(histogram) > 0 else 0
            }
        except:
            return {'macd': 0, 'signal': 0, 'histogram': 0}

    def calculate_technical_score(self, stock, hist):
        """Calculate technical analysis score (0-100)"""
        try:
            score = 50  # Start with neutral

            # RSI analysis (0-30 oversold, 70-100 overbought)
            rsi = self.calculate_rsi(hist)
            if 30 <= rsi <= 70:
                score += 10  # Neutral zone
            elif rsi < 30:
                score += 20  # Oversold - potential buy
            else:
                score -= 10  # Overbought

            # MACD analysis
            macd_data = self.calculate_macd(hist)
            if macd_data['macd'] > macd_data['signal']:
                score += 15  # Bullish crossover
            else:
                score -= 10  # Bearish crossover

            # Moving averages
            ma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            current_price = hist['Close'].iloc[-1]

            if current_price > ma_20 and current_price > ma_50:
                score += 15  # Above both MAs
            elif current_price > ma_20:
                score += 5  # Above short-term MA
            else:
                score -= 10  # Below MAs

            # Volume trend
            avg_volume = hist['Volume'].mean()
            recent_volume = hist['Volume'].iloc[-5:].mean()
            if recent_volume > avg_volume * 1.2:
                score += 10  # High volume

            return min(max(score, 0), 100)
        except Exception as e:
            return 50

    def calculate_fundamental_score(self, info):
        """Calculate fundamental analysis score (0-100)"""
        try:
            score = 50  # Start with neutral

            # P/E Ratio
            pe = info.get('trailingPE', None)
            if pe and 0 < pe < 15:
                score += 20  # Undervalued
            elif pe and 15 <= pe < 25:
                score += 10  # Fair value
            elif pe and pe > 40:
                score -= 15  # Overvalued

            # P/B Ratio
            pb = info.get('priceToBook', None)
            if pb and pb < 3:
                score += 15
            elif pb and pb > 5:
                score -= 10

            # ROE
            roe = info.get('returnOnEquity', None)
            if roe and roe > 0.15:
                score += 15  # Strong ROE
            elif roe and roe > 0.10:
                score += 10

            # Debt to Equity
            debt_to_equity = info.get('debtToEquity', None)
            if debt_to_equity and debt_to_equity < 50:
                score += 10  # Low debt
            elif debt_to_equity and debt_to_equity > 100:
                score -= 10  # High debt

            # Profit Margins
            profit_margin = info.get('profitMargins', None)
            if profit_margin and profit_margin > 0.15:
                score += 10  # Strong margins

            return min(max(score, 0), 100)
        except:
            return 50

    def calculate_sentiment_score(self, info):
        """Calculate sentiment score based on analyst ratings and recommendations"""
        try:
            score = 50

            # Analyst recommendations
            recommendation = info.get('recommendationKey', 'hold')
            if recommendation == 'strong_buy':
                score += 20
            elif recommendation == 'buy':
                score += 15
            elif recommendation == 'hold':
                score += 0
            elif recommendation == 'sell':
                score -= 15
            elif recommendation == 'strong_sell':
                score -= 20

            # Target price vs current price
            target_price = info.get('targetMeanPrice', None)
            current_price = info.get('currentPrice', None)
            if target_price and current_price:
                upside = ((target_price - current_price) / current_price) * 100
                if upside > 20:
                    score += 20
                elif upside > 10:
                    score += 10
                elif upside < -10:
                    score -= 15

            # Number of analyst opinions (more opinions = more confidence)
            num_analysts = info.get('numberOfAnalystOpinions', 0)
            if num_analysts > 10:
                score += 10

            return min(max(score, 0), 100)
        except:
            return 50

    def calculate_risk_score(self, hist, info):
        """Calculate risk score (lower is better, inverted for display)"""
        try:
            risk_score = 50

            # Volatility (Beta)
            beta = info.get('beta', 1.0)
            if beta and beta < 0.8:
                risk_score += 20  # Low risk
            elif beta and beta < 1.2:
                risk_score += 10  # Medium risk
            elif beta and beta > 1.5:
                risk_score -= 15  # High risk

            # 52-week range position
            current_price = info.get('currentPrice', None)
            high_52 = info.get('fiftyTwoWeekHigh', None)
            low_52 = info.get('fiftyTwoWeekLow', None)

            if current_price and high_52 and low_52 and high_52 != low_52:
                position = (current_price - low_52) / (high_52 - low_52)
                if 0.3 <= position <= 0.7:
                    risk_score += 10  # Mid-range - balanced
                elif position > 0.9:
                    risk_score -= 15  # Near highs - risky

            # Price volatility
            returns = hist['Close'].pct_change()
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            if volatility < 0.20:
                risk_score += 15  # Low volatility
            elif volatility > 0.40:
                risk_score -= 10  # High volatility

            return min(max(risk_score, 0), 100)
        except:
            return 50

    def get_recommendation(self, trade_score):
        """Get recommendation based on trade score"""
        if trade_score >= 80:
            return "Strong Buy"
        elif trade_score >= 65:
            return "Buy"
        elif trade_score >= 45:
            return "Hold"
        elif trade_score >= 30:
            return "Sell"
        else:
            return "Strong Sell"

    def analyze_stock(self, ticker):
        """Analyze a single stock"""
        print(f"Analyzing {ticker}...")

        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Fetch historical data (6 months for indicators)
            hist = stock.history(period="6mo")

            if hist.empty:
                print(f"  ⚠ No data available for {ticker}")
                return None

            # Get company name
            company_name = info.get('longName', ticker.replace('.NS', ''))

            # Calculate scores
            technical_score = self.calculate_technical_score(stock, hist)
            fundamental_score = self.calculate_fundamental_score(info)
            sentiment_score = self.calculate_sentiment_score(info)
            risk_score = self.calculate_risk_score(hist, info)

            # Calculate composite Trade Score (weighted average)
            trade_score = round(
                technical_score * 0.30 +
                fundamental_score * 0.35 +
                sentiment_score * 0.20 +
                risk_score * 0.15
            )

            # Get recommendation
            recommendation = self.get_recommendation(trade_score)

            result = {
                'Ticker': ticker,
                'Company': company_name,
                'Trade_Score': trade_score,
                'Technical_Score': round(technical_score),
                'Fundamental_Score': round(fundamental_score),
                'Sentiment_Score': round(sentiment_score),
                'Risk_Score': round(risk_score),
                'Recommendation': recommendation,
                'Status': 'SUCCESS',
                'Notes': ''
            }

            print(f"  ✓ {company_name}: Trade Score = {trade_score}")
            return result

        except Exception as e:
            print(f"  ✗ Failed: {str(e)}")
            return {
                'Ticker': ticker,
                'Company': ticker.replace('.NS', ''),
                'Trade_Score': 'N/A',
                'Technical_Score': 'N/A',
                'Fundamental_Score': 'N/A',
                'Sentiment_Score': 'N/A',
                'Risk_Score': 'N/A',
                'Recommendation': 'N/A',
                'Status': 'FAILED',
                'Notes': str(e)[:100]
            }

    def analyze_all(self):
        """Analyze all Nifty 50 stocks"""
        print(f"\nStarting analysis of {len(self.tickers)} stocks...\n")

        for i, ticker in enumerate(self.tickers, 1):
            print(f"[{i}/{len(self.tickers)}] ", end='')
            result = self.analyze_stock(ticker)
            if result:
                self.results.append(result)

        print(f"\n✓ Analysis complete: {len([r for r in self.results if r['Status'] == 'SUCCESS'])}/{len(self.tickers)} successful\n")

    def generate_report(self):
        """Generate CSV report with rankings"""
        # Create DataFrame
        df = pd.DataFrame(self.results)

        # Separate successful and failed analyses
        successful = df[df['Status'] == 'SUCCESS'].copy()
        failed = df[df['Status'] == 'FAILED'].copy()

        # Sort successful by Trade Score
        successful['Trade_Score'] = pd.to_numeric(successful['Trade_Score'])
        successful = successful.sort_values('Trade_Score', ascending=False)
        successful.insert(0, 'Rank', range(1, len(successful) + 1))

        # Add failed at the end with rank "-"
        failed.insert(0, 'Rank', '-')

        # Combine
        final_df = pd.concat([successful, failed], ignore_index=True)

        # Save to CSV
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'nifty50_analysis_{date_str}.csv'
        final_df.to_csv(filename, index=False)

        print(f"✓ Report saved to: {filename}\n")

        # Display summary
        self.display_summary(successful, failed)

        return filename

    def display_summary(self, successful, failed):
        """Display summary statistics"""
        print("=" * 70)
        print("NIFTY 50 ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"Successfully analyzed: {len(successful)}/{len(self.tickers)} stocks")
        print(f"Failed: {len(failed)} stocks")

        if len(successful) > 0:
            print(f"\nTop 5 Performers by Trade Score:")
            print("-" * 70)
            for i, row in successful.head(5).iterrows():
                print(f"{row['Rank']}. {row['Ticker']:15} - {row['Company'][:30]:30} - Score: {row['Trade_Score']}")

            if len(successful) >= 5:
                print(f"\nBottom 5 Performers by Trade Score:")
                print("-" * 70)
                for i, row in successful.tail(5).iterrows():
                    print(f"{row['Rank']}. {row['Ticker']:15} - {row['Company'][:30]:30} - Score: {row['Trade_Score']}")

        print("=" * 70)


def main():
    # Path to tickers file
    tickers_file = '.claude/skills/nifty50-analyzer/references/nifty50_tickers.txt'

    # Create analyzer
    analyzer = Nifty50Analyzer(tickers_file)

    # Analyze all stocks
    analyzer.analyze_all()

    # Generate report
    analyzer.generate_report()


if __name__ == "__main__":
    main()
