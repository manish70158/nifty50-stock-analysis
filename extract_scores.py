#!/usr/bin/env python3
"""
Extract trade scores from all TRADE-ANALYSIS files and generate CSV report
"""

import re
import os
from pathlib import Path
from datetime import datetime

def extract_score_from_file(filepath):
    """Extract key metrics from a trade analysis file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract ticker from filename
        filename = os.path.basename(filepath)
        ticker_match = re.search(r'TRADE-ANALYSIS-([A-Z&]+\.NS)', filename)
        if not ticker_match:
            return None
        ticker = ticker_match.group(1)

        # Skip OLD files - prefer the latest
        if '-OLD-' in filename:
            return None

        # Extract company name
        company_match = re.search(r'##\s+([^\n]+?)\s+\(', content)
        company = company_match.group(1).strip() if company_match else ticker.replace('.NS', '')

        # Extract composite/trade score - try multiple patterns
        score_patterns = [
            r'(?:Composite\s+Trade\s+Score|Trade\s+Score|COMPOSITE\s+TRADE\s+SCORE):\s*\*?\*?(\d+(?:\.\d+)?)/100',
            r'##\s+(?:Composite\s+Trade\s+Score|Trade\s+Score):\s*\*?\*?(\d+(?:\.\d+)?)/100',
            r'Score:\s*\*?\*?(\d+(?:\.\d+)?)/100',
        ]
        trade_score = None
        for pattern in score_patterns:
            score_match = re.search(pattern, content, re.IGNORECASE)
            if score_match:
                trade_score = float(score_match.group(1))
                break

        if trade_score is None:
            print(f"Warning: Could not find trade score in {filename}")
            return None

        # Extract dimension scores
        technical = extract_dimension_score(content, 'Technical')
        fundamental = extract_dimension_score(content, 'Fundamental')
        sentiment = extract_dimension_score(content, 'Sentiment')
        risk = extract_dimension_score(content, 'Risk')

        # Extract recommendation
        rec_patterns = [
            r'Signal:\s*\*?\*?([A-Z /]+)',
            r'Recommendation:\s*\*?\*?([A-Z /]+)',
            r'Signal:\s*\*?\*?(Strong\s+Buy|Buy|Hold|Sell|Strong\s+Sell|Accumulate|Avoid)',
        ]
        recommendation = "N/A"
        for pattern in rec_patterns:
            rec_match = re.search(pattern, content, re.IGNORECASE)
            if rec_match:
                recommendation = rec_match.group(1).strip().title()
                break

        return {
            'ticker': ticker,
            'company': company,
            'trade_score': trade_score,
            'technical_score': technical,
            'fundamental_score': fundamental,
            'sentiment_score': sentiment,
            'risk_score': risk,
            'recommendation': recommendation,
            'status': 'SUCCESS'
        }
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def extract_dimension_score(content, dimension):
    """Extract a specific dimension score"""
    patterns = [
        rf'{dimension}\s+(?:Analysis|Strength|Quality|Assessment|Profile):\s*\*?\*?(\d+(?:\.\d+)?)/100',
        rf'{dimension}:\s*\*?\*?(\d+(?:\.\d+)?)/100',
        rf'-\s+\*?\*?{dimension}[^:]*:\s*\*?\*?(\d+(?:\.\d+)?)/100',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return 'N/A'

def main():
    # Find all analysis files
    analysis_dir = Path('/Users/manishkumar/Documents/learning/9-May-Trade-Analysis')
    pattern = 'TRADE-ANALYSIS-*.md'

    files = list(analysis_dir.glob(pattern))
    print(f"Found {len(files)} analysis files")

    # Extract scores from all files
    results = []
    seen_tickers = set()

    # Sort by modification time, newest first, to prefer latest versions
    files_sorted = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)

    for filepath in files_sorted:
        data = extract_score_from_file(filepath)
        if data and data['ticker'] not in seen_tickers:
            results.append(data)
            seen_tickers.add(data['ticker'])
            print(f"✓ {data['ticker']}: {data['trade_score']}/100")

    # Sort by trade score descending
    results.sort(key=lambda x: x['trade_score'], reverse=True)

    # Assign ranks
    for i, result in enumerate(results, 1):
        result['rank'] = i

    # Add ULTRACEMCO.NS as failed
    results.append({
        'rank': '-',
        'ticker': 'ULTRACEMCO.NS',
        'company': 'UltraTech Cement',
        'trade_score': 'N/A',
        'technical_score': 'N/A',
        'fundamental_score': 'N/A',
        'sentiment_score': 'N/A',
        'risk_score': 'N/A',
        'recommendation': 'N/A',
        'status': 'FAILED',
        'notes': 'Data access limitations'
    })

    # Generate CSV
    today = datetime.now().strftime('%Y-%m-%d')
    csv_filename = f'nifty50_analysis_{today}.csv'
    csv_path = analysis_dir / csv_filename

    with open(csv_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write('Rank,Ticker,Company,Trade_Score,Technical_Score,Fundamental_Score,Sentiment_Score,Risk_Score,Recommendation,Status,Notes\n')

        # Write data rows
        for result in results:
            notes = result.get('notes', '')
            f.write(f"{result['rank']},{result['ticker']},{result['company']},{result['trade_score']},"
                   f"{result['technical_score']},{result['fundamental_score']},{result['sentiment_score']},"
                   f"{result['risk_score']},{result['recommendation']},{result['status']},{notes}\n")

    print(f"\n✅ CSV Report Generated: {csv_filename}")
    print(f"Total stocks analyzed: {len(results)-1}/50 (excluding failed)")
    print(f"Successfully analyzed: {len([r for r in results if r['status'] == 'SUCCESS'])}")
    print(f"Failed: {len([r for r in results if r['status'] == 'FAILED'])}")

    return csv_path

if __name__ == '__main__':
    csv_path = main()
    print(f"\nFull path: {csv_path}")
