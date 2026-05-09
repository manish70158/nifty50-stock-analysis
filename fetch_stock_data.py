#!/usr/bin/env python3
"""
Fetch stock data for Bharti Airtel (BHARTIARTL.NS)
"""

import json
import sys

# Since we're working with Indian stocks, let me provide known information about Bharti Airtel
# This is a major Indian telecommunications company

stock_data = {
    "ticker": "BHARTIARTL.NS",
    "company_name": "Bharti Airtel Limited",
    "exchange": "NSE (National Stock Exchange of India)",
    "sector": "Telecommunications",
    "industry": "Telecom Services",

    "company_overview": {
        "description": "Bharti Airtel Limited is India's leading telecommunications services provider with operations across 18 countries in South Asia and Africa. The company provides mobile services, fixed broadband, digital TV, and enterprise solutions.",
        "headquarters": "New Delhi, India",
        "founded": "1995",
        "ipo_year": "2002",
        "ceo": "Gopal Vittal (India & South Asia)",
        "employees": "Approximately 30,000+",
        "key_segments": [
            "Mobile Services (India)",
            "Airtel Business (Enterprise)",
            "Homes (Broadband & DTH)",
            "Digital Services",
            "Africa Operations"
        ]
    },

    "note": "This is a template. Agents will perform live web searches for current price, financials, and news."
}

print(json.dumps(stock_data, indent=2))
