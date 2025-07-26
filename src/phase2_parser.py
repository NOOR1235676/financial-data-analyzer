#!/usr/bin/env python3
"""
Phase 2: Transaction Parsing & Data Extraction
Advanced parsing with intelligent column detection and data cleaning
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class ParsedTransaction:
    date: datetime
    description: str
    amount: float
    debit_credit: str
    balance: Optional[float] = None
    reference: str = ""
    account: str = ""
    counterparty: str = ""
    category: str = ""
    source_file: str = ""
    source_sheet: str = ""
    row_number: int = 0

class AdvancedTransactionParser:
    def __init__(self):
        self.date_patterns = [
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',  # YYYY-MM-DD or YYYY/MM/DD
            r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',  # MM-DD-YYYY or MM/DD/YYYY
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2}',  # MM-DD-YY or MM/DD/YY
            r'\d{1,2}\s+\w+\s+\d{4}',        # DD Month YYYY
        ]
        
        self.amount_patterns = [
            r'[-]?\d{1,3}(?:,\d{3})*(?:\.\d{2})?',  # 1,234.56 or -1,234.56
            r'[-]?\d+(?:\.\d{2})?',                  # 1234.56 or -1234.56
            r'\(\d{1,3}(?:,\d{3})*(?:\.\d{2})?\)',   # (1,234.56) for negatives
        ]
        
        self.currency_symbols = ['$', '€', '£', '¥', '₹', 'HUF', 'EUR', 'USD', 'GBP']
        
    def detect_column_types(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Intelligently detect column types based on content analysis"""
        column_types = {
            'date': [],
            'amount': [],
            'description': [],
            'reference': [],
            'account': [],
            'balance': []
        }
        
        for col in df.columns:
            col_lower = str(col).lower()
            sample_data = df[col].dropna().head(20)
            
            # Date column detection
            if self._is_date_column(col_lower, sample_data):
                column_types['date'].append(col)
            
            # Amount column detection
            elif self._is_amount_column(col_lower, sample_data):
                column_types['amount'].append(col)
            
            # Description column detection
            elif self._is_description_column(col_lower, sample_data):
                column_types['description'].append(col)
            
            # Reference column detection
            elif self._is_reference_column(col_lower, sample_data):
                column_types['reference'].append(col)
            
            # Account column detection
            elif self._is_account_column(col_lower, sample_data):
                column_types['account'].append(col)
            
            # Balance column detection
            elif self._is_balance_column(col_lower, sample_data):
                column_types['balance'].append(col)
        
        return column_types
    
    def _is_date_column(self, col_name: str, sample_data: pd.Series) -> bool:
        """Check if column contains dates"""
        date_keywords = ['date', 'time', 'posting', 'booking', 'value', 'created']
        
        # Check column name
        if any(keyword in col_name for keyword in date_keywords):
            return True
        
        # Check data content
        if len(sample_data) == 0:
            return False
        
        date_count = 0
        for value in sample_data:
            if pd.isna(value):
                continue
            
            # Try to parse as datetime
            try:
                pd.to_datetime(str(value))
                date_count += 1
            except:
                # Check against regex patterns
                if any(re.search(pattern, str(value)) for pattern in self.date_patterns):
                    date_count += 1
        
        return (date_count / len(sample_data)) > 0.6
    
    def _is_amount_column(self, col_name: str, sample_data: pd.Series) -> bool:
        """Check if column contains monetary amounts"""
        amount_keywords = ['amount', 'value', 'sum', 'total', 'balance', 'credit', 'debit']
        
        # Check column name
        if any(keyword in col_name for keyword in amount_keywords):
            # Additional check for numeric data
            numeric_count = 0
            for value in sample_data:
                if pd.isna(value):
                    continue
                try:
                    float(str(value).replace(',', '').replace('(', '').replace(')', ''))
                    numeric_count += 1
                except:
                    pass
            return (numeric_count / max(len(sample_data), 1)) > 0.5
        
        return False
    
    def _is_description_column(self, col_name: str, sample_data: pd.Series) -> bool:
        """Check if column contains transaction descriptions"""
        desc_keywords = ['description', 'details', 'memo', 'narrative', 'info', 'transaction']
        
        if any(keyword in col_name for keyword in desc_keywords):
            return True
        
        # Check for text content with reasonable length
        if len(sample_data) == 0:
            return False
        
        text_count = 0
        for value in sample_data:
            if pd.isna(value):
                continue
            if isinstance(value, str) and 5 <= len(value) <= 200:
                text_count += 1
        
        return (text_count / len(sample_data)) > 0.4
    
    def _is_reference_column(self, col_name: str, sample_data: pd.Series) -> bool:
        """Check if column contains reference numbers"""
        ref_keywords = ['reference', 'ref', 'id', 'number', 'doc', 'entry']
        return any(keyword in col_name for keyword in ref_keywords)
    
    def _is_account_column(self, col_name: str, sample_data: pd.Series) -> bool:
        """Check if column contains account information"""
        acc_keywords = ['account', 'iban', 'bank', 'customer']
        return any(keyword in col_name for keyword in acc_keywords)
    
    def _is_balance_column(self, col_name: str, sample_data: pd.Series) -> bool:
        """Check if column contains balance information"""
        bal_keywords = ['balance', 'remaining', 'outstanding']
        return any(keyword in col_name for keyword in bal_keywords)
    
    def clean_amount(self, amount_str) -> float:
        """Clean and convert amount string to float"""
        if pd.isna(amount_str):
            return 0.0
        
        if isinstance(amount_str, (int, float)):
            return float(amount_str)
        
        amount_str = str(amount_str).strip()
        
        # Remove currency symbols
        for symbol in self.currency_symbols:
            amount_str = amount_str.replace(symbol, '')
        
        # Handle parentheses (negative amounts)
        is_negative = False
        if '(' in amount_str and ')' in amount_str:
            is_negative = True
            amount_str = amount_str.replace('(', '').replace(')', '')
        
        # Remove other non-numeric characters except decimal points and commas
        amount_str = re.sub(r'[^\d.,\-]', '', amount_str)
        
        # Handle comma as thousand separator vs decimal separator
        if ',' in amount_str and '.' in amount_str:
            # Both comma and dot - comma is thousand separator
            amount_str = amount_str.replace(',', '')
        elif ',' in amount_str and amount_str.count(',') == 1:
            # Single comma - could be decimal separator (European format)
            parts = amount_str.split(',')
            if len(parts[1]) <= 2:  # Likely decimal separator
                amount_str = amount_str.replace(',', '.')
            else:  # Likely thousand separator
                amount_str = amount_str.replace(',', '')
        
        try:
            value = float(amount_str)
            return -value if is_negative else value
        except ValueError:
            return 0.0
    
    def clean_date(self, date_str) -> Optional[datetime]:
        """Clean and convert date string to datetime"""
        if pd.isna(date_str):
            return None
        
        try:
            return pd.to_datetime(date_str)
        except:
            # Try different formats
            date_formats = [
                '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
                '%m-%d-%Y', '%d-%m-%Y', '%d.%m.%Y', '%Y.%m.%d'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(str(date_str), fmt)
                except:
                    continue
            
            return None
    
    def parse_bank_statement(self, df: pd.DataFrame, sheet_name: str, file_name: str) -> List[ParsedTransaction]:
        """Parse bank statement transactions"""
        transactions = []
        
        # Detect column types
        column_types = self.detect_column_types(df)
        
        # Select best columns for each type
        date_col = column_types['date'][0] if column_types['date'] else None
        amount_col = column_types['amount'][0] if column_types['amount'] else None
        desc_col = column_types['description'][0] if column_types['description'] else None
        ref_col = column_types['reference'][0] if column_types['reference'] else None
        
        if not date_col or not amount_col:
            print(f"Warning: Could not find required columns in {file_name}")
            return transactions
        
        for idx, row in df.iterrows():
            try:
                # Parse date
                date_val = self.clean_date(row[date_col])
                if not date_val:
                    continue
                
                # Parse amount
                amount = self.clean_amount(row[amount_col])
                if amount == 0:
                    continue
                
                # Get description
                description = str(row[desc_col]) if desc_col and not pd.isna(row[desc_col]) else ""
                
                # Get reference
                reference = str(row[ref_col]) if ref_col and not pd.isna(row[ref_col]) else ""
                
                # Determine debit/credit
                debit_credit = "DEBIT" if amount < 0 else "CREDIT"
                
                transaction = ParsedTransaction(
                    date=date_val,
                    description=description,
                    amount=abs(amount),
                    debit_credit=debit_credit,
                    reference=reference,
                    source_file=file_name,
                    source_sheet=sheet_name,
                    row_number=idx + 1
                )
                
                transactions.append(transaction)
                
            except Exception as e:
                continue
        
        return transactions
    
    def parse_customer_ledger(self, df: pd.DataFrame, sheet_name: str, file_name: str) -> List[ParsedTransaction]:
        """Parse customer ledger transactions"""
        transactions = []
        
        # Detect column types
        column_types = self.detect_column_types(df)
        
        # Select best columns
        date_col = column_types['date'][0] if column_types['date'] else None
        amount_col = column_types['amount'][0] if column_types['amount'] else None
        desc_col = column_types['description'][0] if column_types['description'] else None
        
        if not date_col or not amount_col:
            print(f"Warning: Could not find required columns in {file_name}")
            return transactions
        
        for idx, row in df.iterrows():
            try:
                # Parse date
                date_val = self.clean_date(row[date_col])
                if not date_val:
                    continue
                
                # Parse amount
                amount = self.clean_amount(row[amount_col])
                if amount == 0:
                    continue
                
                # Get description
                description = str(row[desc_col]) if desc_col and not pd.isna(row[desc_col]) else ""
                
                # Get customer info if available
                customer_col = None
                for col in df.columns:
                    if 'customer' in str(col).lower() and 'name' in str(col).lower():
                        customer_col = col
                        break
                
                counterparty = str(row[customer_col]) if customer_col and not pd.isna(row[customer_col]) else ""
                
                # Determine debit/credit
                debit_credit = "DEBIT" if amount < 0 else "CREDIT"
                
                transaction = ParsedTransaction(
                    date=date_val,
                    description=description,
                    amount=abs(amount),
                    debit_credit=debit_credit,
                    counterparty=counterparty,
                    source_file=file_name,
                    source_sheet=sheet_name,
                    row_number=idx + 1
                )
                
                transactions.append(transaction)
                
            except Exception as e:
                continue
        
        return transactions
    
    def categorize_transactions(self, transactions: List[ParsedTransaction]) -> List[ParsedTransaction]:
        """Automatically categorize transactions based on description"""
        categories = {
            'Transfer': ['transfer', 'átutalás', 'átvezetés'],
            'Card Payment': ['card', 'kártya', 'pos'],
            'Fee': ['fee', 'charge', 'díj'],
            'Interest': ['interest', 'kamat'],
            'Salary': ['salary', 'fizetés', 'bér'],
            'Utilities': ['utilities', 'energy', 'water', 'gas'],
            'Other': []
        }
        
        for transaction in transactions:
            desc_lower = transaction.description.lower()
            category_found = False
            
            for category, keywords in categories.items():
                if category == 'Other':
                    continue
                    
                if any(keyword in desc_lower for keyword in keywords):
                    transaction.category = category
                    category_found = True
                    break
            
            if not category_found:
                transaction.category = 'Other'
        
        return transactions
