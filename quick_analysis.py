#!/usr/bin/env python3
"""
Quick Financial Data Analysis
Demonstrates the capabilities of the financial data parser
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from financial_analyzer import FinancialDataAnalyzer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def main():
    console = Console()
    
    # Display banner
    banner = Text("🚀 QUICK FINANCIAL DATA ANALYSIS 📊", style="bold green")
    console.print(Panel(banner, expand=False))
    
    # Initialize analyzer
    analyzer = FinancialDataAnalyzer()
    
    # Define file paths
    bank_file = Path("data/sample/KH_Bank.XLSX")
    ledger_file = Path("data/sample/Customer_Ledger_Entries_FULL.xlsx")
    
    # Check if files exist
    if not bank_file.exists():
        console.print(f"[red]❌ Bank statement file not found: {bank_file}[/red]")
        return
    
    if not ledger_file.exists():
        console.print(f"[red]❌ Customer ledger file not found: {ledger_file}[/red]")
        return
    
    console.print(f"[green]✅ Found both files![/green]")
    console.print(f"Bank Statement: {bank_file}")
    console.print(f"Customer Ledger: {ledger_file}")
    
    console.print("\n" + "="*60)
    console.print("RUNNING AUTOMATED ANALYSIS...")
    console.print("="*60)
    
    try:
        # Step 1: Load data
        console.print("\n[yellow]📂 Step 1: Loading Excel files...[/yellow]")
        bank_info = analyzer.load_bank_statement(str(bank_file))
        ledger_info = analyzer.load_customer_ledger(str(ledger_file))
        
        # Step 2: Analyze structure
        console.print("\n[yellow]🔍 Step 2: Analyzing data structure...[/yellow]")
        analyzer.analyze_data_structure()
        
        # Step 3: Parse transactions
        console.print("\n[yellow]⚡ Step 3: Parsing transactions...[/yellow]")
        transactions = analyzer.parse_transactions()
        
        if len(transactions) == 0:
            console.print("[red]❌ No transactions were parsed. Please check your Excel files.[/red]")
            return
        
        # Step 4: Generate statistics
        console.print("\n[yellow]📈 Step 4: Generating summary statistics...[/yellow]")
        analyzer.generate_summary_statistics()
        
        # Step 5: Find matches
        console.print("\n[yellow]🔍 Step 5: Finding matching transactions...[/yellow]")
        results = analyzer.find_matching_transactions(tolerance_days=3, amount_tolerance=0.01)
        
        # Step 6: Generate reports
        console.print("\n[yellow]📄 Step 6: Generating reports...[/yellow]")
        analyzer.generate_reconciliation_report("quick_reconciliation_report.xlsx")
        analyzer.export_processed_data("quick_processed_data.xlsx")
        
        # Step 7: Create visualizations
        console.print("\n[yellow]📊 Step 7: Creating visualizations...[/yellow]")
        try:
            analyzer.create_visualizations("quick_charts")
            console.print("[green]✅ Visualizations created successfully![/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️ Visualization creation skipped: {e}[/yellow]")
        
        # Summary
        console.print("\n" + "="*60)
        console.print("[bold green]🎉 ANALYSIS COMPLETE! 🎉[/bold green]")
        console.print("="*60)
        
        console.print("\n[cyan]📋 Generated Files:[/cyan]")
        console.print("  📊 quick_reconciliation_report.xlsx - Detailed reconciliation")
        console.print("  📈 quick_processed_data.xlsx - All processed transactions")
        console.print("  📉 quick_charts/ - Visualization charts (if matplotlib available)")
        
        console.print(f"\n[green]✅ Successfully processed {len(transactions)} transactions![/green]")
        
        if results:
            matches = results.get('matches', [])
            unmatched_bank = results.get('unmatched_bank', [])
            unmatched_ledger = results.get('unmatched_ledger', [])
            
            console.print(f"[blue]🔗 Found {len(matches)} potential matches[/blue]")
            console.print(f"[yellow]⚠️ {len(unmatched_bank)} unmatched bank transactions[/yellow]")
            console.print(f"[yellow]⚠️ {len(unmatched_ledger)} unmatched ledger transactions[/yellow]")
        
        console.print("\n[green]You can now:")
        console.print("- Open the Excel reports to review the detailed analysis")
        console.print("- View the charts folder for visual insights")
        console.print("- Run 'python main.py' for the full interactive menu")
        
    except Exception as e:
        console.print(f"\n[red]❌ Error during analysis: {e}[/red]")
        console.print("\nPlease ensure:")
        console.print("1. Excel files are not open in another program")
        console.print("2. Files contain valid financial data")
        console.print("3. All dependencies are installed correctly")

if __name__ == "__main__":
    main()
