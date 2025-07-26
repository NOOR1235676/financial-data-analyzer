#!/usr/bin/env python3
"""
Financial Data Parser and Analyzer
Main script to analyze bank statements and customer ledger data
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from financial_analyzer import FinancialDataAnalyzer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text

def main():
    console = Console()
    
    # Display welcome banner
    banner = Text("🏦 FINANCIAL DATA PARSER & ANALYZER 💰", style="bold blue")
    console.print(Panel(banner, expand=False))
    console.print("Analyze bank statements and customer ledger data with automated reconciliation\n")
    
    # Initialize analyzer
    analyzer = FinancialDataAnalyzer()
    
    # Define file paths
    bank_file = Path("data/sample/KH_Bank.XLSX")
    ledger_file = Path("data/sample/Customer_Ledger_Entries_FULL.xlsx")
    
    # Check if files exist
    if not bank_file.exists():
        console.print(f"[red]❌ Bank statement file not found: {bank_file}[/red]")
        console.print("Please ensure the KH_Bank.XLSX file is in the data/sample/ directory")
        return
    
    if not ledger_file.exists():
        console.print(f"[red]❌ Customer ledger file not found: {ledger_file}[/red]")
        console.print("Please ensure the Customer_Ledger_Entries_FULL.xlsx file is in the data/sample/ directory")
        return
    
    console.print(f"[green]✅ Found bank statement: {bank_file}[/green]")
    console.print(f"[green]✅ Found customer ledger: {ledger_file}[/green]\n")
    
    while True:
        console.print("\n[cyan]═" * 60 + "[/cyan]")
        console.print("[bold yellow]FINANCIAL DATA ANALYZER MENU[/bold yellow]")
        console.print("[cyan]═" * 60 + "[/cyan]")
        
        menu_options = [
            "1. Load and analyze data structure",
            "2. Parse all transactions",
            "3. Generate summary statistics",
            "4. Find matching transactions (reconciliation)",
            "5. Generate reconciliation report",
            "6. Create data visualizations",
            "7. Export processed data to Excel",
            "8. Run complete analysis (all steps)",
            "9. Exit"
        ]
        
        for option in menu_options:
            console.print(f"  {option}")
        
        console.print("[cyan]═" * 60 + "[/cyan]")
        
        choice = Prompt.ask("Select an option", choices=[str(i) for i in range(1, 10)])
        
        try:
            if choice == "1":
                console.print("\n[yellow]🔍 LOADING AND ANALYZING DATA STRUCTURE[/yellow]")
                analyzer.load_bank_statement(str(bank_file))
                analyzer.load_customer_ledger(str(ledger_file))
                analyzer.analyze_data_structure()
                
            elif choice == "2":
                console.print("\n[yellow]📊 PARSING TRANSACTIONS[/yellow]")
                if not analyzer.bank_data and not analyzer.ledger_data:
                    analyzer.load_bank_statement(str(bank_file))
                    analyzer.load_customer_ledger(str(ledger_file))
                
                transactions = analyzer.parse_transactions()
                console.print(f"[green]Successfully parsed {len(transactions)} transactions[/green]")
                
            elif choice == "3":
                console.print("\n[yellow]📈 GENERATING SUMMARY STATISTICS[/yellow]")
                if not analyzer.transactions:
                    console.print("[yellow]No transactions loaded. Loading data first...[/yellow]")
                    analyzer.load_bank_statement(str(bank_file))
                    analyzer.load_customer_ledger(str(ledger_file))
                    analyzer.parse_transactions()
                
                analyzer.generate_summary_statistics()
                
            elif choice == "4":
                console.print("\n[yellow]🔍 FINDING MATCHING TRANSACTIONS[/yellow]")
                if not analyzer.transactions:
                    console.print("[yellow]No transactions loaded. Loading data first...[/yellow]")
                    analyzer.load_bank_statement(str(bank_file))
                    analyzer.load_customer_ledger(str(ledger_file))
                    analyzer.parse_transactions()
                
                # Get tolerance parameters
                days_tolerance = Prompt.ask("Enter date tolerance in days", default="3")
                amount_tolerance = Prompt.ask("Enter amount tolerance", default="0.01")
                
                try:
                    days_tolerance = int(days_tolerance)
                    amount_tolerance = float(amount_tolerance)
                except ValueError:
                    console.print("[red]Invalid tolerance values. Using defaults.[/red]")
                    days_tolerance = 3
                    amount_tolerance = 0.01
                
                analyzer.find_matching_transactions(days_tolerance, amount_tolerance)
                
            elif choice == "5":
                console.print("\n[yellow]📝 GENERATING RECONCILIATION REPORT[/yellow]")
                if not analyzer.reconciliation_results:
                    console.print("[yellow]No reconciliation results. Running reconciliation first...[/yellow]")
                    if not analyzer.transactions:
                        analyzer.load_bank_statement(str(bank_file))
                        analyzer.load_customer_ledger(str(ledger_file))
                        analyzer.parse_transactions()
                    analyzer.find_matching_transactions()
                
                report_name = Prompt.ask("Enter report filename", default="reconciliation_report.xlsx")
                analyzer.generate_reconciliation_report(report_name)
                
            elif choice == "6":
                console.print("\n[yellow]📊 CREATING VISUALIZATIONS[/yellow]")
                if not analyzer.transactions:
                    console.print("[yellow]No transactions loaded. Loading data first...[/yellow]")
                    analyzer.load_bank_statement(str(bank_file))
                    analyzer.load_customer_ledger(str(ledger_file))
                    analyzer.parse_transactions()
                
                viz_dir = Prompt.ask("Enter visualization directory", default="visualizations")
                analyzer.create_visualizations(viz_dir)
                
            elif choice == "7":
                console.print("\n[yellow]💾 EXPORTING PROCESSED DATA[/yellow]")
                if not analyzer.transactions:
                    console.print("[yellow]No transactions loaded. Loading data first...[/yellow]")
                    analyzer.load_bank_statement(str(bank_file))
                    analyzer.load_customer_ledger(str(ledger_file))
                    analyzer.parse_transactions()
                
                export_name = Prompt.ask("Enter export filename", default="processed_financial_data.xlsx")
                analyzer.export_processed_data(export_name)
                
            elif choice == "8":
                console.print("\n[yellow]🚀 RUNNING COMPLETE ANALYSIS[/yellow]")
                
                # Load data
                console.print("Step 1/7: Loading data...")
                analyzer.load_bank_statement(str(bank_file))
                analyzer.load_customer_ledger(str(ledger_file))
                
                # Analyze structure
                console.print("Step 2/7: Analyzing data structure...")
                analyzer.analyze_data_structure()
                
                # Parse transactions
                console.print("Step 3/7: Parsing transactions...")
                analyzer.parse_transactions()
                
                # Generate statistics
                console.print("Step 4/7: Generating summary statistics...")
                analyzer.generate_summary_statistics()
                
                # Find matches
                console.print("Step 5/7: Finding matching transactions...")
                analyzer.find_matching_transactions()
                
                # Generate reports
                console.print("Step 6/7: Generating reconciliation report...")
                analyzer.generate_reconciliation_report("complete_reconciliation_report.xlsx")
                
                # Create visualizations
                console.print("Step 7/7: Creating visualizations...")
                analyzer.create_visualizations("complete_analysis_charts")
                
                # Export data
                analyzer.export_processed_data("complete_processed_data.xlsx")
                
                console.print("\n[green]🎉 COMPLETE ANALYSIS FINISHED![/green]")
                console.print("Generated files:")
                console.print("  📊 complete_reconciliation_report.xlsx")
                console.print("  📈 complete_analysis_charts/ (directory)")
                console.print("  📋 complete_processed_data.xlsx")
                
            elif choice == "9":
                console.print("\n[green]👋 Thank you for using Financial Data Analyzer![/green]")
                break
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user[/yellow]")
            continue
        except Exception as e:
            console.print(f"\n[red]❌ Error: {e}[/red]")
            console.print("Please try again or contact support if the problem persists.")
            continue
        
        # Ask if user wants to continue
        if choice != "9":
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
