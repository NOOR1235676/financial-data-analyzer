import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from fuzzywuzzy import fuzz, process
from rich.console import Console
from rich.table import Table
from rich.progress import track
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Transaction:
    date: datetime
    description: str
    amount: float
    balance: Optional[float] = None
    transaction_type: str = ""
    category: str = ""
    reference: str = ""
    
@dataclass
class BankStatement:
    account_number: str
    account_name: str
    transactions: List[Transaction]
    opening_balance: float = 0.0
    closing_balance: float = 0.0

class FinancialDataAnalyzer:
    def __init__(self):
        self.console = Console()
        self.bank_data = {}
        self.ledger_data = {}
        self.transactions = []
        self.reconciliation_results = {}
        
    def load_bank_statement(self, file_path: str) -> Dict[str, Any]:
        """Load and parse bank statement Excel file"""
        self.console.print(f"[blue]Loading bank statement: {file_path}[/blue]")
        
        try:
            # Try to read the Excel file and detect sheets
            excel_file = pd.ExcelFile(file_path, engine='openpyxl')
            sheets_info = {}
            
            for sheet_name in excel_file.sheet_names:
                self.console.print(f"  📄 Found sheet: {sheet_name}")
                df = excel_file.parse(sheet_name)
                sheets_info[sheet_name] = {
                    'shape': df.shape,
                    'columns': df.columns.tolist(),
                    'data': df
                }
                
            self.bank_data = sheets_info
            return sheets_info
            
        except Exception as e:
            self.console.print(f"[red]Error loading bank statement: {e}[/red]")
            return {}
    
    def load_customer_ledger(self, file_path: str) -> Dict[str, Any]:
        """Load and parse customer ledger Excel file"""
        self.console.print(f"[blue]Loading customer ledger: {file_path}[/blue]")
        
        try:
            excel_file = pd.ExcelFile(file_path, engine='openpyxl')
            sheets_info = {}
            
            for sheet_name in excel_file.sheet_names:
                self.console.print(f"  📄 Found sheet: {sheet_name}")
                df = excel_file.parse(sheet_name)
                sheets_info[sheet_name] = {
                    'shape': df.shape,
                    'columns': df.columns.tolist(),
                    'data': df
                }
                
            self.ledger_data = sheets_info
            return sheets_info
            
        except Exception as e:
            self.console.print(f"[red]Error loading customer ledger: {e}[/red]")
            return {}
    
    def analyze_data_structure(self):
        """Analyze the structure of loaded data"""
        self.console.print("\n[green]📊 DATA STRUCTURE ANALYSIS[/green]")
        
        # Analyze bank data
        if self.bank_data:
            self.console.print("\n[yellow]🏦 BANK STATEMENT STRUCTURE[/yellow]")
            for sheet_name, info in self.bank_data.items():
                table = Table(title=f"Sheet: {sheet_name}")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="white")
                
                table.add_row("Rows", str(info['shape'][0]))
                table.add_row("Columns", str(info['shape'][1]))
                table.add_row("Column Names", ", ".join(info['columns'][:5]) + ("..." if len(info['columns']) > 5 else ""))
                
                self.console.print(table)
                
                # Show sample data
                if not info['data'].empty:
                    self.console.print(f"Sample data from {sheet_name}:")
                    self.console.print(info['data'].head().to_string())
        
        # Analyze ledger data
        if self.ledger_data:
            self.console.print("\n[yellow]📋 CUSTOMER LEDGER STRUCTURE[/yellow]")
            for sheet_name, info in self.ledger_data.items():
                table = Table(title=f"Sheet: {sheet_name}")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="white")
                
                table.add_row("Rows", str(info['shape'][0]))
                table.add_row("Columns", str(info['shape'][1]))
                table.add_row("Column Names", ", ".join(info['columns'][:5]) + ("..." if len(info['columns']) > 5 else ""))
                
                self.console.print(table)
                
                # Show sample data
                if not info['data'].empty:
                    self.console.print(f"Sample data from {sheet_name}:")
                    self.console.print(info['data'].head().to_string())
    
    def detect_date_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect columns that contain dates"""
        date_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if column contains date-like strings
                sample = df[col].dropna().head(10)
                date_count = 0
                for val in sample:
                    if isinstance(val, str):
                        # Common date patterns
                        date_patterns = [
                            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
                            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',
                            r'\d{1,2}\s+\w+\s+\d{4}'
                        ]
                        if any(re.search(pattern, val) for pattern in date_patterns):
                            date_count += 1
                if date_count >= len(sample) * 0.7:  # 70% of samples are dates
                    date_columns.append(col)
            elif 'datetime' in str(df[col].dtype).lower():
                date_columns.append(col)
        return date_columns
    
    def detect_amount_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect columns that contain monetary amounts"""
        amount_columns = []
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                # Check if values look like monetary amounts
                non_zero = df[col].dropna()
                non_zero = non_zero[non_zero != 0]
                if len(non_zero) > 0:
                    # Check for reasonable monetary ranges
                    if non_zero.abs().min() >= 0.01 and non_zero.abs().max() <= 1e8:
                        amount_columns.append(col)
            elif df[col].dtype == 'object':
                # Check for string amounts (with currency symbols, commas, etc.)
                sample = df[col].dropna().head(20)
                amount_count = 0
                for val in sample:
                    if isinstance(val, str):
                        # Remove common currency symbols and separators
                        cleaned = re.sub(r'[,$€£¥₹\s]', '', str(val))
                        try:
                            float(cleaned)
                            amount_count += 1
                        except ValueError:
                            pass
                if amount_count >= len(sample) * 0.7:
                    amount_columns.append(col)
        return amount_columns
    
    def clean_amount(self, amount_str):
        """Clean and convert amount string to float"""
        if pd.isna(amount_str):
            return 0.0
        
        if isinstance(amount_str, (int, float)):
            return float(amount_str)
        
        # Remove currency symbols and separators
        cleaned = re.sub(r'[,$€£¥₹\s()]', '', str(amount_str))
        
        # Handle negative amounts in parentheses
        if '(' in str(amount_str) and ')' in str(amount_str):
            cleaned = '-' + cleaned
        
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def parse_transactions(self) -> List[Transaction]:
        """Parse transactions from loaded data"""
        self.console.print("\n[green]🔍 PARSING TRANSACTIONS[/green]")
        transactions = []
        
        # Parse bank statement transactions
        for sheet_name, info in self.bank_data.items():
            df = info['data'].copy()
            if df.empty:
                continue
                
            self.console.print(f"Processing bank sheet: {sheet_name}")
            
            # Detect date and amount columns
            date_cols = self.detect_date_columns(df)
            amount_cols = self.detect_amount_columns(df)
            
            self.console.print(f"  Date columns: {date_cols}")
            self.console.print(f"  Amount columns: {amount_cols}")
            
            if date_cols and amount_cols:
                date_col = date_cols[0]
                amount_col = amount_cols[0]
                
                # Find description column (usually the longest text column)
                text_cols = [col for col in df.columns if df[col].dtype == 'object' and col not in date_cols]
                desc_col = None
                if text_cols:
                    # Choose the column with the longest average text
                    avg_lengths = {}
                    for col in text_cols:
                        avg_length = df[col].astype(str).str.len().mean()
                        avg_lengths[col] = avg_length
                    desc_col = max(avg_lengths, key=avg_lengths.get)
                
                # Parse each row
                for idx, row in df.iterrows():
                    try:
                        # Parse date
                        date_val = pd.to_datetime(row[date_col])
                        
                        # Parse amount
                        amount = self.clean_amount(row[amount_col])
                        
                        # Get description
                        description = str(row[desc_col]) if desc_col else f"Transaction {idx}"
                        
                        # Create transaction
                        transaction = Transaction(
                            date=date_val,
                            description=description,
                            amount=amount,
                            transaction_type="Bank Statement"
                        )
                        transactions.append(transaction)
                        
                    except Exception as e:
                        continue
        
        # Parse ledger transactions
        for sheet_name, info in self.ledger_data.items():
            df = info['data'].copy()
            if df.empty:
                continue
                
            self.console.print(f"Processing ledger sheet: {sheet_name}")
            
            # Similar parsing logic for ledger
            date_cols = self.detect_date_columns(df)
            amount_cols = self.detect_amount_columns(df)
            
            if date_cols and amount_cols:
                date_col = date_cols[0]
                amount_col = amount_cols[0]
                
                text_cols = [col for col in df.columns if df[col].dtype == 'object' and col not in date_cols]
                desc_col = None
                if text_cols:
                    avg_lengths = {}
                    for col in text_cols:
                        avg_length = df[col].astype(str).str.len().mean()
                        avg_lengths[col] = avg_length
                    desc_col = max(avg_lengths, key=avg_lengths.get)
                
                for idx, row in df.iterrows():
                    try:
                        date_val = pd.to_datetime(row[date_col])
                        amount = self.clean_amount(row[amount_col])
                        description = str(row[desc_col]) if desc_col else f"Ledger Entry {idx}"
                        
                        transaction = Transaction(
                            date=date_val,
                            description=description,
                            amount=amount,
                            transaction_type="Customer Ledger"
                        )
                        transactions.append(transaction)
                        
                    except Exception as e:
                        continue
        
        self.transactions = transactions
        self.console.print(f"[green]✅ Parsed {len(transactions)} transactions[/green]")
        return transactions
    
    def generate_summary_statistics(self):
        """Generate summary statistics for the financial data"""
        if not self.transactions:
            self.console.print("[red]No transactions to analyze[/red]")
            return
        
        self.console.print("\n[green]📈 FINANCIAL SUMMARY STATISTICS[/green]")
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([
            {
                'date': t.date,
                'description': t.description,
                'amount': t.amount,
                'type': t.transaction_type
            }
            for t in self.transactions
        ])
        
        # Overall statistics
        table = Table(title="Overall Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Total Transactions", str(len(df)))
        table.add_row("Date Range", f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        table.add_row("Total Amount", f"${df['amount'].sum():,.2f}")
        table.add_row("Average Transaction", f"${df['amount'].mean():,.2f}")
        table.add_row("Largest Credit", f"${df['amount'].max():,.2f}")
        table.add_row("Largest Debit", f"${df['amount'].min():,.2f}")
        
        self.console.print(table)
        
        # By transaction type
        if 'type' in df.columns:
            type_summary = df.groupby('type').agg({
                'amount': ['count', 'sum', 'mean']
            }).round(2)
            
            self.console.print("\n[yellow]By Transaction Type:[/yellow]")
            self.console.print(type_summary.to_string())
        
        # Monthly summary
        df['month'] = df['date'].dt.to_period('M')
        monthly_summary = df.groupby('month').agg({
            'amount': ['count', 'sum', 'mean']
        }).round(2)
        
        self.console.print("\n[yellow]Monthly Summary:[/yellow]")
        self.console.print(monthly_summary.to_string())
    
    def find_matching_transactions(self, tolerance_days: int = 3, amount_tolerance: float = 0.01):
        """Find potentially matching transactions between bank and ledger"""
        self.console.print(f"\n[green]🔍 FINDING MATCHING TRANSACTIONS[/green]")
        
        bank_transactions = [t for t in self.transactions if t.transaction_type == "Bank Statement"]
        ledger_transactions = [t for t in self.transactions if t.transaction_type == "Customer Ledger"]
        
        matches = []
        unmatched_bank = []
        unmatched_ledger = []
        
        for bank_trans in bank_transactions:
            best_match = None
            best_score = 0
            
            for ledger_trans in ledger_transactions:
                # Check date proximity
                date_diff = abs((bank_trans.date - ledger_trans.date).days)
                if date_diff <= tolerance_days:
                    # Check amount similarity
                    amount_diff = abs(bank_trans.amount - ledger_trans.amount)
                    if amount_diff <= amount_tolerance:
                        # Use fuzzy matching for description
                        desc_score = fuzz.partial_ratio(bank_trans.description, ledger_trans.description)
                        
                        # Combined score
                        score = desc_score - (date_diff * 10) - (amount_diff * 100)
                        
                        if score > best_score and score > 50:  # Minimum threshold
                            best_score = score
                            best_match = ledger_trans
            
            if best_match:
                matches.append((bank_trans, best_match, best_score))
                if best_match in ledger_transactions:
                    ledger_transactions.remove(best_match)
            else:
                unmatched_bank.append(bank_trans)
        
        unmatched_ledger = ledger_transactions
        
        # Display results
        self.console.print(f"[green]✅ Found {len(matches)} potential matches[/green]")
        self.console.print(f"[yellow]⚠️  {len(unmatched_bank)} unmatched bank transactions[/yellow]")
        self.console.print(f"[yellow]⚠️  {len(unmatched_ledger)} unmatched ledger transactions[/yellow]")
        
        # Show sample matches
        if matches:
            self.console.print("\n[blue]Sample Matches:[/blue]")
            for i, (bank, ledger, score) in enumerate(matches[:5]):
                self.console.print(f"{i+1}. Score: {score:.1f}")
                self.console.print(f"   Bank: {bank.date.strftime('%Y-%m-%d')} | ${bank.amount:,.2f} | {bank.description[:50]}...")
                self.console.print(f"   Ledger: {ledger.date.strftime('%Y-%m-%d')} | ${ledger.amount:,.2f} | {ledger.description[:50]}...")
                self.console.print()
        
        self.reconciliation_results = {
            'matches': matches,
            'unmatched_bank': unmatched_bank,
            'unmatched_ledger': unmatched_ledger
        }
        
        return self.reconciliation_results
    
    def generate_reconciliation_report(self, output_file: str = "reconciliation_report.xlsx"):
        """Generate a detailed reconciliation report"""
        if not self.reconciliation_results:
            self.console.print("[red]No reconciliation results available. Run find_matching_transactions first.[/red]")
            return
        
        self.console.print(f"\n[green]📝 GENERATING RECONCILIATION REPORT[/green]")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Matches sheet
            if self.reconciliation_results['matches']:
                matches_data = []
                for bank, ledger, score in self.reconciliation_results['matches']:
                    matches_data.append({
                        'Match_Score': score,
                        'Bank_Date': bank.date,
                        'Bank_Amount': bank.amount,
                        'Bank_Description': bank.description,
                        'Ledger_Date': ledger.date,
                        'Ledger_Amount': ledger.amount,
                        'Ledger_Description': ledger.description,
                        'Date_Difference_Days': (bank.date - ledger.date).days,
                        'Amount_Difference': bank.amount - ledger.amount
                    })
                
                matches_df = pd.DataFrame(matches_data)
                matches_df.to_excel(writer, sheet_name='Matches', index=False)
            
            # Unmatched bank transactions
            if self.reconciliation_results['unmatched_bank']:
                unmatched_bank_data = [{
                    'Date': t.date,
                    'Amount': t.amount,
                    'Description': t.description
                } for t in self.reconciliation_results['unmatched_bank']]
                
                unmatched_bank_df = pd.DataFrame(unmatched_bank_data)
                unmatched_bank_df.to_excel(writer, sheet_name='Unmatched_Bank', index=False)
            
            # Unmatched ledger transactions
            if self.reconciliation_results['unmatched_ledger']:
                unmatched_ledger_data = [{
                    'Date': t.date,
                    'Amount': t.amount,
                    'Description': t.description
                } for t in self.reconciliation_results['unmatched_ledger']]
                
                unmatched_ledger_df = pd.DataFrame(unmatched_ledger_data)
                unmatched_ledger_df.to_excel(writer, sheet_name='Unmatched_Ledger', index=False)
        
        self.console.print(f"[green]✅ Reconciliation report saved to: {output_file}[/green]")
    
    def create_visualizations(self, output_dir: str = "visualizations"):
        """Create financial data visualizations"""
        if not self.transactions:
            self.console.print("[red]No transactions to visualize[/red]")
            return
        
        self.console.print(f"\n[green]📊 CREATING VISUALIZATIONS[/green]")
        
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'date': t.date,
                'amount': t.amount,
                'type': t.transaction_type
            }
            for t in self.transactions
        ])
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # 1. Transaction amounts over time
        plt.figure(figsize=(12, 6))
        for trans_type in df['type'].unique():
            subset = df[df['type'] == trans_type]
            plt.scatter(subset['date'], subset['amount'], label=trans_type, alpha=0.6)
        plt.title('Transaction Amounts Over Time')
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/transactions_over_time.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Monthly transaction volume
        df['month'] = df['date'].dt.to_period('M')
        monthly_counts = df.groupby(['month', 'type']).size().unstack(fill_value=0)
        
        plt.figure(figsize=(12, 6))
        monthly_counts.plot(kind='bar', stacked=True)
        plt.title('Monthly Transaction Volume')
        plt.xlabel('Month')
        plt.ylabel('Number of Transactions')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/monthly_volume.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Amount distribution
        plt.figure(figsize=(12, 6))
        for trans_type in df['type'].unique():
            subset = df[df['type'] == trans_type]['amount']
            plt.hist(subset, bins=50, alpha=0.7, label=trans_type)
        plt.title('Transaction Amount Distribution')
        plt.xlabel('Amount ($)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{output_dir}/amount_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        self.console.print(f"[green]✅ Visualizations saved to: {output_dir}/[/green]")
    
    def export_processed_data(self, output_file: str = "processed_financial_data.xlsx"):
        """Export all processed data to Excel"""
        if not self.transactions:
            self.console.print("[red]No data to export[/red]")
            return
        
        self.console.print(f"\n[green]💾 EXPORTING PROCESSED DATA[/green]")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # All transactions
            transactions_data = [{
                'Date': t.date,
                'Description': t.description,
                'Amount': t.amount,
                'Type': t.transaction_type,
                'Category': t.category,
                'Reference': t.reference
            } for t in self.transactions]
            
            transactions_df = pd.DataFrame(transactions_data)
            transactions_df.to_excel(writer, sheet_name='All_Transactions', index=False)
            
            # Summary statistics
            summary_data = []
            df = pd.DataFrame(transactions_data)
            
            summary_data.append(['Total Transactions', len(df)])
            summary_data.append(['Date Range Start', df['Date'].min()])
            summary_data.append(['Date Range End', df['Date'].max()])
            summary_data.append(['Total Amount', df['Amount'].sum()])
            summary_data.append(['Average Transaction', df['Amount'].mean()])
            summary_data.append(['Largest Credit', df['Amount'].max()])
            summary_data.append(['Largest Debit', df['Amount'].min()])
            
            summary_df = pd.DataFrame(summary_data, columns=['Metric', 'Value'])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        self.console.print(f"[green]✅ Data exported to: {output_file}[/green]")
