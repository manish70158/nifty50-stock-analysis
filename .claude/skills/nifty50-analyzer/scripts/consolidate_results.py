#!/usr/bin/env python3
"""
Consolidate Nifty 50 analysis results into a ranked CSV report.

Usage:
    python consolidate_results.py <results_dir> <output_csv>

The script expects a results directory containing analysis output files,
one per stock. It extracts scores and recommendations, then generates
a sorted CSV report.
"""

import os
import sys
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def extract_score(text: str, score_name: str) -> Optional[float]:
    """
    Extract a score from analysis text.
    Looks for patterns like "Technical Score: 85" or "Technical: 85/100"
    """
    patterns = [
        rf"{score_name}\s*Score\s*[:\-]\s*(\d+(?:\.\d+)?)",
        rf"{score_name}\s*[:\-]\s*(\d+(?:\.\d+)?)\s*/\s*100",
        rf"{score_name}\s*[:\-]\s*(\d+(?:\.\d+)?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))

    return None


def extract_recommendation(text: str) -> str:
    """
    Extract trading recommendation from analysis text.
    """
    recommendations = [
        "Strong Buy",
        "Buy",
        "Hold",
        "Sell",
        "Strong Sell",
    ]

    text_lower = text.lower()
    for rec in recommendations:
        if rec.lower() in text_lower:
            return rec

    return "N/A"


def extract_company_name(text: str, ticker: str) -> str:
    """
    Extract company name from analysis text.
    Falls back to ticker if not found.
    """
    # Look for patterns like "Company: XYZ Ltd" or "XYZ Limited"
    patterns = [
        r"Company\s*[:\-]\s*([A-Za-z\s&]+(?:Ltd|Limited|Inc|Corporation)?)",
        r"^([A-Z][A-Za-z\s&]+(?:Ltd|Limited|Inc|Corporation)?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            name = match.group(1).strip()
            if len(name) > 3 and name.lower() not in ['the', 'and', 'company']:
                return name

    # Fallback: clean up ticker
    return ticker.replace('.NS', '').replace('-', ' ').title()


def parse_analysis_file(file_path: Path) -> Dict:
    """
    Parse a single analysis result file and extract key information.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        ticker = file_path.stem  # Filename without extension

        result = {
            'ticker': ticker,
            'company': extract_company_name(content, ticker),
            'technical_score': extract_score(content, 'Technical'),
            'fundamental_score': extract_score(content, 'Fundamental'),
            'sentiment_score': extract_score(content, 'Sentiment'),
            'risk_score': extract_score(content, 'Risk'),
            'trade_score': extract_score(content, 'Trade'),
            'recommendation': extract_recommendation(content),
            'status': 'SUCCESS',
            'notes': ''
        }

        # Validate that we extracted at least some scores
        if all(v is None for v in [result['technical_score'],
                                     result['fundamental_score'],
                                     result['sentiment_score'],
                                     result['trade_score']]):
            result['status'] = 'FAILED'
            result['notes'] = 'Could not extract scores from analysis'

        return result

    except Exception as e:
        return {
            'ticker': file_path.stem,
            'company': file_path.stem.replace('.NS', ''),
            'technical_score': None,
            'fundamental_score': None,
            'sentiment_score': None,
            'risk_score': None,
            'trade_score': None,
            'recommendation': 'N/A',
            'status': 'FAILED',
            'notes': f'Error: {str(e)}'
        }


def format_score(score: Optional[float]) -> str:
    """Format score for CSV output."""
    return f"{score:.1f}" if score is not None else "N/A"


def generate_csv_report(results: List[Dict], output_path: Path):
    """
    Generate ranked CSV report from analysis results.
    """
    # Separate successful and failed analyses
    successful = [r for r in results if r['status'] == 'SUCCESS' and r['trade_score'] is not None]
    failed = [r for r in results if r['status'] == 'FAILED' or r['trade_score'] is None]

    # Sort successful results by trade score (descending)
    successful.sort(key=lambda x: x['trade_score'], reverse=True)

    # Assign ranks
    for i, result in enumerate(successful, start=1):
        result['rank'] = i

    for result in failed:
        result['rank'] = '-'

    # Combine: successful first, then failed
    all_results = successful + failed

    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'Rank', 'Ticker', 'Company', 'Trade_Score',
            'Technical_Score', 'Fundamental_Score',
            'Sentiment_Score', 'Risk_Score',
            'Recommendation', 'Status', 'Notes'
        ])

        # Data rows
        for result in all_results:
            writer.writerow([
                result['rank'],
                result['ticker'],
                result['company'],
                format_score(result['trade_score']),
                format_score(result['technical_score']),
                format_score(result['fundamental_score']),
                format_score(result['sentiment_score']),
                format_score(result['risk_score']),
                result['recommendation'],
                result['status'],
                result['notes']
            ])

    return len(successful), len(failed)


def print_summary(results: List[Dict], output_path: Path):
    """Print summary statistics."""
    successful = [r for r in results if r['status'] == 'SUCCESS' and r['trade_score'] is not None]
    failed = [r for r in results if r['status'] == 'FAILED' or r['trade_score'] is None]

    successful.sort(key=lambda x: x['trade_score'], reverse=True)

    print("\n" + "="*50)
    print("Nifty 50 Analysis Complete")
    print("="*50)
    print(f"Successfully analyzed: {len(successful)}/{len(results)} stocks")
    print(f"Failed: {len(failed)} stocks (see CSV for details)")
    print()

    if successful:
        print("Top 5 Performers by Trade Score:")
        for i, result in enumerate(successful[:5], start=1):
            print(f"{i}. {result['ticker']} - {result['company']} - Score: {result['trade_score']:.1f}")
        print()

        if len(successful) >= 5:
            print("Bottom 5 Performers by Trade Score:")
            bottom_start = len(successful) - 5
            for i, result in enumerate(successful[bottom_start:], start=bottom_start+1):
                print(f"{i}. {result['ticker']} - {result['company']} - Score: {result['trade_score']:.1f}")
            print()

    print(f"CSV saved to: {output_path}")
    print("="*50)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    results_dir = Path(sys.argv[1])
    output_csv = Path(sys.argv[2])

    if not results_dir.exists():
        print(f"Error: Results directory not found: {results_dir}")
        sys.exit(1)

    # Find all result files (txt, md, or no extension)
    result_files = list(results_dir.glob('*.txt')) + \
                   list(results_dir.glob('*.md')) + \
                   [f for f in results_dir.glob('*') if f.is_file() and not f.suffix]

    if not result_files:
        print(f"Error: No result files found in {results_dir}")
        sys.exit(1)

    print(f"Processing {len(result_files)} result files...")

    # Parse all result files
    results = []
    for file_path in result_files:
        result = parse_analysis_file(file_path)
        results.append(result)

    # Generate CSV
    success_count, failed_count = generate_csv_report(results, output_csv)

    # Print summary
    print_summary(results, output_csv)


if __name__ == '__main__':
    main()
