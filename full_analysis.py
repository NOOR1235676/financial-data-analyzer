#!/usr/bin/env python3
"""
Complete Financial Data Analysis Tool
Integration of transaction parsing, reconciliation, and reporting
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from phase2_parser import AdvancedTransactionParser
from phase3_reconciler import DataReconciler
from financial_analyzer import FinancialDataAnalyzer  # Assuming it includes further functions to aid complete Phase 4

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Confirm, Prompt


def comprehensive_analysis():
    console = Console()
    console.print(Panel(Text("🚀 COMPLETE FINANCIAL ANALYSIS TOOL 🏦", style="bold blue"), expand=False))
    
    # File paths
    bank_file = Path("data/sample/KH_Bank.XLSX")
    ledger_file = Path("data/sample/Customer_Ledger_Entries_FULL.xlsx")

    # Initialize Analyzer and Parser
    analyzer = FinancialDataAnalyzer()
    parser = AdvancedTransactionParser()
    reconciler = DataReconciler()

    # Step 1: Parse files
    console.print("\n[cyan]Step 1: Parse bank statements and ledger files[/cyan]")
    bank_data = analyzer.load_bank_statement(str(bank_file))
    ledger_data = analyzer.load_customer_ledger(str(ledger_file))
    
    bank_transactions = []
    ledger_transactions = []

    # Parse all sheets in bank statement
    for sheet_name, info in bank_data.items():
        bank_transactions.extend(parser.parse_bank_statement(info['data'], sheet_name, str(bank_file)))

    # Parse all sheets in customer ledger
    for sheet_name, info in ledger_data.items():
        ledger_transactions.extend(parser.parse_customer_ledger(info['data'], sheet_name, str(ledger_file)))

    # Step 2: Categorize transactions
    console.print("\n[cyan]Step 2: Categorize transactions[/cyan]")
    bank_transactions = parser.categorize_transactions(bank_transactions)

    # Step 3: Reconcile transactions
    console.print("\n[cyan]Step 3: Reconcile transactions between bank and ledger[/cyan]")
    matches = reconciler.reconcile_transactions(bank_transactions, ledger_transactions)

    # Display reconciliation results
    console.print(f"[green]Found {len(matches)} potential matches[/green]")

    # Step 4: Generate reports
    console.print("\n[cyan]Step 4: Report generation[/cyan]")
    console.print("Generating reconciliation report...")
    analyzer.generate_reconciliation_report("full_reconciliation_report.xlsx")

    console.print("Generating visualizations...")
    analyzer.create_visualizations("full_analysis_charts")

    analyzer.export_processed_data("full_processed_data.xlsx")

    console.print("\n[green]🎉 The complete financial analysis has been concluded![/green]")

if __name__ == "__main__":
    comprehensive_analysis()
