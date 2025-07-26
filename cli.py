#!/usr/bin/env python3
"""
Command-line interface for flexible phase execution
"""

import argparse
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from financial_analyzer import FinancialDataAnalyzer
from phase2_parser import AdvancedTransactionParser
from phase3_reconciler import DataReconciler
from report_generator import ReportGenerator

def parse_arguments():
    parser = argparse.ArgumentParser(description="Financial Data Parser CLI")
    parser.add_argument('--phase', type=int, choices=[1, 2, 3, 4], help="Phase to execute (1-4)")
    parser.add_argument('--report', action='store_true', help="Generate comprehensive report")
    parser.add_argument('--bank-file', default="data/sample/KH_Bank.XLSX", help="Bank statement file path")
    parser.add_argument('--ledger-file', default="data/sample/Customer_Ledger_Entries_FULL.xlsx", help="Customer ledger file path")
    return parser.parse_args()

def run_phase1(bank_file, ledger_file):
    """Phase 1: Basic Excel Processing"""
    print("Phase 1: Basic Excel Processing")
    print("-" * 40)
    
    analyzer = FinancialDataAnalyzer()
    
    # Load data
    print(f"Loading bank statement: {bank_file}")
    bank_data = analyzer.load_bank_statement(bank_file)
    
    print(f"Loading customer ledger: {ledger_file}")
    ledger_data = analyzer.load_customer_ledger(ledger_file)
    
    # Analyze structure
    print("Analyzing data structure...")
    analyzer.analyze_data_structure()
    
    print("Phase 1 completed successfully!")
    return analyzer, bank_data, ledger_data

def run_phase2(analyzer):
    """Phase 2: Advanced Transaction Parsing"""
    print("\nPhase 2: Advanced Transaction Parsing")
    print("-" * 40)
    
    # Parse transactions
    print("Parsing transactions...")
    transactions = analyzer.parse_transactions()
    
    print(f"Phase 2 completed! Parsed {len(transactions)} transactions.")
    return transactions

def run_phase3(analyzer):
    """Phase 3: Data Reconciliation"""
    print("\nPhase 3: Data Reconciliation")
    print("-" * 40)
    
    # Find matching transactions
    print("Finding matching transactions...")
    reconciliation_results = analyzer.find_matching_transactions(tolerance_days=3, amount_tolerance=0.01)
    
    matches = reconciliation_results.get('matches', [])
    unmatched_bank = reconciliation_results.get('unmatched_bank', [])
    unmatched_ledger = reconciliation_results.get('unmatched_ledger', [])
    
    print(f"Found {len(matches)} potential matches")
    print(f"Unmatched bank transactions: {len(unmatched_bank)}")
    print(f"Unmatched ledger transactions: {len(unmatched_ledger)}")
    
    print("Phase 3 completed successfully!")
    return reconciliation_results

def run_phase4(analyzer, generate_report=False):
    """Phase 4: Complete Analysis with Reporting"""
    print("\nPhase 4: Complete Analysis")
    print("-" * 40)
    
    # Generate summary statistics
    print("Generating summary statistics...")
    analyzer.generate_summary_statistics()
    
    # Create visualizations
    print("Creating visualizations...")
    try:
        analyzer.create_visualizations("cli_charts")
        print("Visualizations saved to cli_charts/")
    except Exception as e:
        print(f"Warning: Visualization creation failed: {e}")
    
    # Export processed data
    print("Exporting processed data...")
    analyzer.export_processed_data("cli_processed_data.xlsx")
    print("Data exported to cli_processed_data.xlsx")
    
    if generate_report:
        print("Generating comprehensive reports...")
        try:
            # Generate reports using the report generator
            report_gen = ReportGenerator()
            
            # Prepare data for reports
            data = {
                'bank_transactions': [],
                'ledger_transactions': [],
                'matches': []
            }
            
            # Generate PDF report
            pdf_file = report_gen.generate_pdf_report(data, "cli_financial_report.pdf")
            print(f"PDF report generated: {pdf_file}")
            
            # Generate Excel report
            excel_file = report_gen.generate_excel_report(data, "cli_financial_report.xlsx")
            print(f"Excel report generated: {excel_file}")
            
        except Exception as e:
            print(f"Warning: Report generation failed: {e}")
    
    print("Phase 4 completed successfully!")

def phase_execution(phase, generate_report, bank_file, ledger_file):
    """Execute the specified phase"""
    try:
        if phase == 1:
            run_phase1(bank_file, ledger_file)
            
        elif phase == 2:
            analyzer, _, _ = run_phase1(bank_file, ledger_file)
            run_phase2(analyzer)
            
        elif phase == 3:
            analyzer, _, _ = run_phase1(bank_file, ledger_file)
            run_phase2(analyzer)
            run_phase3(analyzer)
            
        elif phase == 4:
            analyzer, _, _ = run_phase1(bank_file, ledger_file)
            run_phase2(analyzer)
            run_phase3(analyzer)
            run_phase4(analyzer, generate_report)
            
        else:
            print("Please specify a phase (1-4) using --phase argument")
            print("Example: python cli.py --phase 4 --report")
            
    except Exception as e:
        print(f"Error during phase execution: {e}")
        return False
    
    return True

def main():
    print("FINANCIAL DATA PARSER CLI")
    print("=" * 50)
    
    args = parse_arguments()
    
    success = phase_execution(args.phase, args.report, args.bank_file, args.ledger_file)
    
    if success:
        print("\nCLI execution completed successfully!")
    else:
        print("\nCLI execution failed. Please check the errors above.")

if __name__ == '__main__':
    main()
