import re
from typing import Optional, Tuple
from datetime import datetime

class FormatParser:
    """Parser for handling specific financial data formats"""

    def __init__(self):
        # Define regex patterns for different formats
        self.amount_patterns = {
            "USD": r'\$[\d,]+\.?\d*',
            "EUR": r'€[\d.,]+',
            "INR": r'₹[\d,]+\.?\d*',
            "Parentheses": r'\([\d,]+\.?\d*\)',
            "TrailingMinus": r'[\d,]+\.?\d*-',
            "ShortScale": r'[\d.]+[KMB]'
        }

        self.date_patterns = {
            "MM/DD/YYYY": r'\d{1,2}/\d{1,2}/\d{4}',
            "DD/MM/YYYY": r'\d{1,2}/\d{1,2}/\d{4}',
            "YYYY-MM-DD": r'\d{4}-\d{1,2}-\d{1,2}',
            "Quarter": r'Q[1-4]-\d{2,4}',
            "Month_YYYY": r'\w{3,9} \d{4}'
        }

    def parse_amount(self, value: str) -> Optional[float]:
        """Parse the financial amount string into a float"""
        # Remove commas and surrounding whitespace.
        cleaned = value.replace(',', '').strip()

        # Remove currency symbols for parsing.
        for pattern in self.amount_patterns.values():
            cleaned = re.sub(pattern, '', cleaned)

        # Handle negative formats like (amount) or amount-
        if '(' in value and ')' in value:
            cleaned = f'-{cleaned}';
        elif value.endswith('-'):
            cleaned = f'-{cleaned[:-1]}'

        try:
            return float(cleaned)
        except ValueError:
            return None

    def parse_date(self, value: str) -> Optional[datetime]:
        """Parse various date formats into a datetime object"""
        for pattern, date_format in self.date_patterns.items():
            if re.match(pattern, value):
                try:
                    # Map pattern to strptime format.
                    if "MM/DD/YYYY" in pattern:
                        fmt = '%m/%d/%Y'
                    elif "DD/MM/YYYY" in pattern:
                        fmt = '%d/%m/%Y'
                    elif "YYYY-MM-DD" in pattern:
                        fmt = '%Y-%m-%d'
                    elif "Quarter" in pattern:
                        return self._parse_quarter(value)
                    elif "Month_YYYY" in pattern:
                        fmt = '%b %Y'
                    else:
                        continue

                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        return None

    def _parse_quarter(self, value: str) -> Optional[datetime]:
        """Helper to parse quarters into datetime objects"""
        match = re.match(r'Q([1-4])-(\d{2,4})', value)
        if match:
            quarter, year = match.groups()
            month = int(quarter) * 3
            return datetime(year=int(year), month=month, day=1)
        return None

    def normalize_currency(self, value: str) -> str:
        """Normalize currencies by removing currency symbols and formatting them consistently"""
        for symbol in "€$₹£¥":
            value = value.replace(symbol, '').strip()
        return value

    def handle_special_formats(self, value: str) -> Tuple[str, ...]:
        """Handle special cases and return a tuple with normalized formats."""
        normalized_amount = self.normalize_currency(value)
        parsed_date = self.parse_date(value)
        return normalized_amount, str(parsed_date) if parsed_date else ""
